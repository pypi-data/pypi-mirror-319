import json
from pathlib import Path
from typing import List, Protocol, Union

from pydantic import BaseModel

from teleclass.core.models.models import DocumentMeta


class DocumentLoader(Protocol):
    def load(self) -> List[DocumentMeta]:
        pass


class JSONDocumentLoader(DocumentLoader):
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    def load(self) -> List[DocumentMeta]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")

        with open(self.file_path, 'r') as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of documents")

        return [DocumentMeta(
            id=str(idx),
            content=json.dumps(doc),
        ) for idx, doc in enumerate(data)]


class ModelDocumentLoader(DocumentLoader):
    def __init__(self, documents: List[BaseModel]):
        if not isinstance(documents, list) or not all(isinstance(doc, BaseModel) for doc in documents):
            raise TypeError(
                "documents must be a list of pydantic BaseModel instances")
        self.documents = documents

    def load(self) -> List[DocumentMeta]:
        return [
            DocumentMeta(
                id=str(i),
                content=doc.model_dump_json(),
            )
            for i, doc in enumerate(self.documents)
        ]
