"""Types common to all lego submodules."""

from typing import (
    Any,
    DefaultDict,
    NewType,
    Protocol,
    TypeAlias,
    TypedDict,
    TypeVar,
)

from openai.types.chat.chat_completion import ChatCompletion

T = TypeVar("T")
# -- mypy contradicts with pyright here?
OneOrMany = T | list[T]  # type: ignore[misc]

JSONDict: TypeAlias = dict[str, Any]  # type: ignore[misc]
FlatParamConfig: TypeAlias = dict[str, str | int | float | bool]

UseProfiler = NewType("UseProfiler", bool)
ProfilerSessions = NewType(
    "ProfilerSessions", DefaultDict[str, dict[str, float]]
)

Messages: TypeAlias = list[dict[str, str]]


class EmbedModel(Protocol):
    """Embedding model protocol."""

    embed_dim: int
    model_name: str

    def __call__(self, texts: list[str]) -> list[list[float]]:
        """Return embeddings for the input texts."""


class LegoLLMRouter(Protocol):
    """Protocol for LLM routers available in Lego."""

    def __call__(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,  # type: ignore[misc]
    ) -> Any:
        """Make a ChatCompletion request."""


class _Delta(TypedDict, total=False):
    content: str
    role: str


class _Choice(TypedDict, total=False):
    delta: _Delta
    index: int
    finish_reason: str | None


class StreamChunk(TypedDict, total=False):
    """The protocol for a stream chunk from OpenAI's ChatCompletion."""

    choices: list[_Choice]
