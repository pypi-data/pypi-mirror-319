import logging
from pathlib import Path
from typing import Dict, List, Set, Union

from pydantic import BaseModel

from teleclass.classifiers.similarity_classifier import SimilarityClassifier
from teleclass.core.cache import TELEClassCache
from teleclass.core.document_loader import (
    DocumentLoader,
    JSONDocumentLoader,
    ModelDocumentLoader,
)
from teleclass.core.embeddings import EmbeddingService
from teleclass.core.models.enrichment_models import (
    CorpusEnrichmentResult,
    EnrichedClass,
    LLMEnrichmentResult,
)
from teleclass.core.models.models import DocumentMeta
from teleclass.core.taxonomy_manager import TaxonomyManager
from teleclass.enrichers.corpus_enricher import CorpusEnricher
from teleclass.enrichers.llm_enricher import LLMEnricher

logger = logging.getLogger(__name__)


class TELEClass:
    """Main class for taxonomy-enhanced text classification"""

    def __init__(
        self,
        taxonomy_manager: TaxonomyManager,
        embedding_service: EmbeddingService,
        llm_enricher: LLMEnricher,
        corpus_enricher: CorpusEnricher,
        use_cache: bool = True
    ):
        # Initialize components
        self.taxonomy_manager = taxonomy_manager
        self.embedding_service = embedding_service
        # Initialize enrichers
        self.llm_enricher = llm_enricher
        self.corpus_enricher = corpus_enricher

        # initialize empty set of terms for all classes
        self.enriched_classes = {
            class_name: EnrichedClass(class_name=class_name, terms=set()) for class_name in self.taxonomy_manager.get_all_classes()
        }
        # Initialize cache
        self.use_cache = use_cache
        if use_cache:
            self.cache = TELEClassCache()

    def _load_documents(self, source: Union[str, Path, List[BaseModel]]) -> List[DocumentMeta]:
        """Load documents from either a JSON file path or a list of pydantic models."""
        loader: DocumentLoader = JSONDocumentLoader(source) if isinstance(
            source, (str, Path)) else ModelDocumentLoader(source)
        return loader.load()

    def run(self, doc_path: str, sample_size: int = 20) -> None:
        """
        Main training process with clear stages

        Args:
            sample_size: Number of documents to use for initial training
        """
        logger.info("Starting training process")
        documents = self._load_documents(doc_path)

        documents = documents[:sample_size]

        logger.info("Training with %d documents", len(documents))

        try:
            # Stage 1: LLM-Enhanced Core Class Annotation
            llm_enriched_classes = None

            llm_enrichment_result = self._perform_llm_enrichment(
                collection=documents)

            llm_enriched_classes, documents = llm_enrichment_result.result

            logger.info(
                "Finished assignments with LLM enrichment step")

            # Stage 2: Corpus-Based Enrichment

            corpus_enrichment_result = self._perform_corpus_enrichment(
                documents)

            corpus_enriched_classes = corpus_enrichment_result.result

            logger.info("Finished corpus-based enrichment step")

            self.enriched_classes = self._combine_enriched_classes(
                llm_enriched_classes, corpus_enriched_classes)

            # Add new step: Classifier Training
            logger.info("Step 4: Initialize Classifier")

            # Initialize classifier manager
            self.classifier_manager = SimilarityClassifier(
                taxonomy_manager=self.taxonomy_manager,
                embedding_service=self.embedding_service,
                enriched_classes=self.enriched_classes
            )

        except Exception as e:
            logger.error("Training failed: %s", e)
            raise

    def _perform_llm_enrichment(self, collection: List[DocumentMeta]) -> LLMEnrichmentResult:
        """Perform LLM-based taxonomy enrichment"""
        logger.info("Performing LLM enrichment")
        if not self.use_cache:
            return self.llm_enricher.process(collection=collection)

        # try loading from cache
        llm_class_terms = self.cache.load_class_terms()
        assignments = self.cache.load_assignments()

        if llm_class_terms and assignments:
            return LLMEnrichmentResult(
                ClassEnrichment=llm_class_terms,
                DocumentCoreClasses=assignments
            )
        # if class terms exist but no assignments, use them to generate assignments
        if llm_class_terms:
            assignments = self.llm_enricher.assign_classes_to_docs(
                collection=collection,
                enriched_classes=llm_class_terms
            )
            self.cache.save_assignments(assignments)
            return LLMEnrichmentResult(
                ClassEnrichment=llm_class_terms,
                DocumentCoreClasses=assignments
            )

        # nothing in cache, run full process
        llm_class_terms = self.llm_enricher.enrich_classes_with_terms()
        self.cache.save_class_terms(llm_class_terms)

        assignments = self.llm_enricher.assign_classes_to_docs(
            collection=collection, enriched_classes=llm_class_terms)
        self.cache.save_assignments(assignments)

        return LLMEnrichmentResult(
            ClassEnrichment=llm_class_terms,
            DocumentCoreClasses=assignments
        )

    def _perform_corpus_enrichment(
        self,
        collection: List[DocumentMeta],
    ) -> CorpusEnrichmentResult:
        """Perform corpus-based enrichment"""
        logger.info("Performing corpus-based enrichment")
        corpus_enrichment_result = self.corpus_enricher.enrich(
            collection=collection)
        if self.use_cache:
            self.cache.save_class_terms(
                corpus_enrichment_result.ClassEnrichment)
        return self.corpus_enricher.enrich(collection=collection)

    def _combine_enriched_classes(
        self,
        llm_enriched_classes: Dict[str, EnrichedClass],
        corpus_enriched_classes: Dict[str, EnrichedClass],
    ) -> Dict[str, EnrichedClass]:
        """Combine enriched classes from LLM and corpus enrichers"""
        for class_name in self.taxonomy_manager.get_all_classes():
            # Add LLM terms if they exist
            if class_name in llm_enriched_classes:
                self.enriched_classes[class_name].terms.update(
                    llm_enriched_classes[class_name].terms
                )

            # Add corpus terms if they exist
            if class_name in corpus_enriched_classes:
                self.enriched_classes[class_name].terms.update(
                    corpus_enriched_classes[class_name].terms
                )

        if self.use_cache:
            self.cache.save_class_terms(self.enriched_classes)
        return self.enriched_classes

    def predict(self, text: str, model_class: BaseModel) -> Set[str]:
        """Predict classes for a given text"""
        if not hasattr(self, "classifier_manager"):
            raise RuntimeError("Classifier must be trained before prediction")

        return self.classifier_manager.predict(text, model_class)
