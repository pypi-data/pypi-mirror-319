from typing import Dict, List, Optional, Set, Tuple

import numpy as np
from pydantic import BaseModel, ConfigDict, computed_field

from teleclass.core.models.models import DocumentMeta


class TermScore(BaseModel):
    """Store terms and scores for a candidate term, used in enrichment process"""
    term: str
    popularity: Optional[float] = None
    distinctiveness: Optional[float] = None
    semantic_similarity: Optional[float] = None

    @property
    def affinity_score(self) -> float:
        """Calculate geometric mean of scores"""

        if self.popularity is None or self.distinctiveness is None or self.semantic_similarity is None:
            raise ValueError(
                "Values are not available before corpus enrichment")

        return np.cbrt(self.popularity * self.distinctiveness * self.semantic_similarity)

    def __hash__(self) -> int:
        """Make hashable based on term"""
        return hash(self.term)

    def __eq__(self, other: object) -> bool:
        """Check equality based on term"""
        if not isinstance(other, TermScore):
            return NotImplemented
        return self.term == other.term


class EnrichedClass(BaseModel):
    """Represents an enriched class with metadata and assigned terms"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    class_name: str
    terms: Set[TermScore]
    embeddings: Optional[np.ndarray] = None


class EnrichmentResult(BaseModel):
    """Container for enrichment results"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ClassEnrichment: Dict[str, EnrichedClass]


class LLMEnrichmentResult(EnrichmentResult):
    # Stores LLM enrichment results, such as classes with its relevant terms, and each document's core classes
    DocumentCoreClasses: List[DocumentMeta]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def result(self) -> Tuple[Dict[str, EnrichedClass], List[DocumentMeta]]:
        return self.ClassEnrichment, self.DocumentCoreClasses


class CorpusEnrichmentResult(EnrichmentResult):
    # Stores Corpus enrichment results, such as enriched classes with relevant terms
    @computed_field  # type: ignore[prop-decorator]
    @property
    def result(self) -> Dict[str, EnrichedClass]:
        return self.ClassEnrichment
