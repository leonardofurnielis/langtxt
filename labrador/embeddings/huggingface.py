from typing import Any, List, Literal

from pydantic.v1 import BaseModel, PrivateAttr

from labrador.core.document import Document
from labrador.core.embeddings import BaseEmbedding, Embedding


class HuggingFaceEmbedding(BaseModel, BaseEmbedding):
    """HuggingFace sentence_transformers embedding models.

    Args:
        model_name (str): Hugging Face model to be used. Defaults to ``sentence-transformers/all-MiniLM-L6-v2``.
        device (str, optional): Device to run the model on. Currently supports "cpu" and "cuda". Defaults to ``cpu``.

    **Example**

    .. code-block:: python

        from labrador.embeddings import HuggingFaceEmbedding

        embedding_engine = HuggingFaceEmbedding()
    """

    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: Literal["cpu", "cuda"] = "cpu"

    _client: Any = PrivateAttr()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        from sentence_transformers import SentenceTransformer

        self._client = SentenceTransformer(self.model_name, device=self.device)

    def get_query_embedding(self, query: str) -> Embedding:
        """Compute embedding for a text.

        Args:
            query (str): Input query to compute embedding.

        **Example**

        .. code-block:: python

            embedded_query = embedding_engine.get_query_embedding("Labrador is a data framework to build context-aware AI applications")
        """
        return self.get_texts_embedding([query])[0]

    def get_texts_embedding(self, texts: List[str]) -> List[Embedding]:
        """Compute embeddings for list of texts.

        Args:
            texts (List[str]): List of text to compute embeddings.
        """
        return self._client.encode(texts).tolist()

    def get_documents_embedding(self, documents: List[Document]) -> List[Embedding]:
        """Compute embeddings for a list of documents.

        Args:
            documents (List[Document]): List of `Document` objects to compute embeddings.
        """
        texts = [document.get_content() for document in documents]

        return self.get_texts_embedding(texts)
