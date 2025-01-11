from openai import OpenAI

from lego.lego_types import EmbedModel
from lego.settings import LLMProvider


class OpenAIEmbedModel(EmbedModel):
    """OpenAI embedding model."""

    def __init__(
        self,
        provider: LLMProvider,
        model_subtype: str = "text-embedding-3-small",
    ):
        self.client = OpenAI(
            api_key=provider.api_key, base_url=provider.base_url
        )
        self.model_name = model_subtype
        self.embed_dim = self.inspect_embed_dim()

    def __call__(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts."""
        return [
            x.embedding
            for x in self.client.embeddings.create(
                input=texts, model=self.model_name
            ).data
        ]

    def inspect_embed_dim(self) -> int:
        """Check if the provided embed_dim matches the model."""
        return len(
            self.client.embeddings.create(
                input=["test"], model=self.model_name
            ).data[0]
        )
