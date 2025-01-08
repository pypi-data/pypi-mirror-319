"""Provider configuration models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


if TYPE_CHECKING:
    from pydantic_ai.agent import EndStrategy

    from llmling_agent.agent.conversation import ConversationManager
    from llmling_agent.agent.providers.base import AgentProvider
    from llmling_agent.models.context import AgentContext
    from llmling_agent.tools.manager import ToolManager


class BaseProviderConfig(BaseModel):
    """Base configuration for agent providers.

    Common settings that apply to all provider types, regardless of their
    specific implementation. Provides basic identification and configuration
    options that every provider should have.
    """

    type: str = Field(init=False)
    """Type discriminator for provider configs."""

    name: str | None = None
    """Optional name for the provider instance."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)


class AIProviderConfig(BaseProviderConfig):
    """Configuration for PydanticAI-based provider.

    This provider uses PydanticAI for handling model interactions, tool calls,
    and structured outputs. It provides fine-grained control over model behavior
    and validation.
    """

    type: Literal["ai"] = Field("ai", init=False)
    """Type discriminator for AI provider."""

    end_strategy: EndStrategy = "early"
    """How to handle tool calls when final result found:
    - early: Stop when valid result found
    - complete: Run all requested tools
    - confirm: Ask user what to do
    """

    result_retries: int | None = None
    """Maximum retries for result validation.
    None means use the global retry setting.
    """

    defer_model_check: bool = False
    """Whether to defer model evaluation until first run.
    True can speed up initialization but might fail later.
    """

    model_settings: dict[str, Any] = Field(default_factory=dict)
    """Additional model-specific settings passed to PydanticAI."""

    validation_enabled: bool = True
    """Whether to validate model outputs against schemas."""

    allow_text_fallback: bool = True
    """Whether to accept plain text when structured output fails."""

    def get_provider(
        self,
        *,
        context: AgentContext[Any],
        tools: ToolManager,
        conversation: ConversationManager,
    ) -> AgentProvider:
        """Create PydanticAI provider instance."""
        from llmling_agent.agent.providers.pydanticai import PydanticAIProvider

        return PydanticAIProvider(
            context=context,
            tools=tools,
            conversation=conversation,
            name=self.name or "ai-agent",
            end_strategy=self.end_strategy,
            result_retries=self.result_retries,
            defer_model_check=self.defer_model_check,
            model_settings=self.model_settings,
        )


class HumanProviderConfig(BaseProviderConfig):
    """Configuration for human-in-the-loop provider.

    This provider enables direct human interaction for responses and decisions.
    Useful for testing, training, and oversight of agent operations.
    """

    type: Literal["human"] = Field("human", init=False)
    """Type discriminator for human provider."""

    timeout: int | None = None
    """Timeout in seconds for human response. None means wait indefinitely."""

    show_context: bool = True
    """Whether to show conversation context to human."""

    def get_provider(
        self,
        *,
        context: AgentContext[Any],
        tools: ToolManager,
        conversation: ConversationManager,
    ) -> AgentProvider:
        """Create human provider instance."""
        from llmling_agent.agent.providers.human import HumanProvider

        return HumanProvider(
            context=context,
            tools=tools,
            conversation=conversation,
            name=self.name or "human-agent",
            timeout=self.timeout,
            show_context=self.show_context,
        )


# The union type used in AgentConfig
ProviderConfig = Annotated[
    AIProviderConfig | HumanProviderConfig,
    Field(discriminator="type"),
]

__all__ = [
    "AIProviderConfig",
    "BaseProviderConfig",
    "HumanProviderConfig",
    "ProviderConfig",
]
