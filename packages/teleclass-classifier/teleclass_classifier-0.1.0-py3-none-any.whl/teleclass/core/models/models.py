from typing import Optional, Set

import numpy as np
from pydantic import BaseModel, ConfigDict


class DocumentMeta(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    id: str
    embeddings: Optional[np.ndarray] = None
    content: str
    # Core classes set after LLM enrichment
    initial_core_classes: Optional[Set[str]] = None
