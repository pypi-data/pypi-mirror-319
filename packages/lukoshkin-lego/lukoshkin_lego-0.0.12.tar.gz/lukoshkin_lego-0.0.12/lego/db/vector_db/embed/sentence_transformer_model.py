from sentence_transformers import SentenceTransformer

from lego.lego_types import EmbedModel


class SentenceTransformerModel(EmbedModel):
    """SentenceTransformer embedding model."""

    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embed_dim = self.inspect_embed_dim()

    def __call__(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts."""
        return self.model.encode(texts).tolist()

    def inspect_embed_dim(self) -> int:
        """Check if the provided embed_dim matches the model."""
        return len(self.model.encode(["test"])[0])
