"""Anthropic model implementation."""

from __future__ import annotations as _annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, cast, overload, Union, Literal, Sequence
from json import loads, dumps
from typing_extensions import assert_never

from pydantic_ai import result
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models import ModelSettings, EitherStreamedResponse, Model, AgentModel, check_allow_model_requests
from pydantic_ai.usage import Usage

import logging

logger = logging.getLogger(__name__)

try:
    from anthropic.types import (
        ContentBlock,
        ContentBlockDeltaEvent,
        Message,
        MessageDeltaEvent,
        MessageParam,
        MessageStartEvent,
        MessageStreamEvent,
    )
except ImportError as _import_error:
    raise ImportError(
        'To use the Anthropic model, you need to install the anthropic package. '
        'You can install it with: pip install "pydanticai-genai-hub[anthropic]"'
    ) from _import_error


AnthropicModelName = Union[str]
"""
Using this more broad type for the model name instead of a strict definition
allows this model to be used more easily with other model types
"""


@dataclass(init=False)
class AnthropicModel(Model):
    """A model that uses the Anthropic API.

    Apart from `__init__`, all methods are private or match those of the base class.
    """

    model_name: AnthropicModelName
    client: Any = field(repr=False)

    def __init__(
        self,
        model_name: str,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        """Initialize the Anthropic model.

        Args:
            model_name: The name of the model to use
            api_key: Optional API key. If not provided, will look for ANTHROPIC_API_KEY env var
            base_url: Optional base URL for the API
        """
        try:
            import anthropic
        except ImportError as e:
            raise ImportError(
                'Please install anthropic to use this model: '
                'pip install "pydanticai-genai-hub[anthropic]"'
            ) from e

        self.client = anthropic.Anthropic(
            api_key=api_key,
            base_url=base_url,
        )
        self.model_name = model_name
