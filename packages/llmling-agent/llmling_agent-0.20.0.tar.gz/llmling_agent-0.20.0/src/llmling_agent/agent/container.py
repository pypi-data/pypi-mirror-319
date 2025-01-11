from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import TypeVar

from llmling_agent.log import get_logger


if TYPE_CHECKING:
    from llmling_agent.agent import AnyAgent
    from llmling_agent.agent.conversation import ConversationManager
    from llmling_agent.delegation.pool import AgentPool
    from llmling_agent.models.context import AgentContext
    from llmling_agent.tools.manager import ToolManager
    from llmling_agent_providers.base import AgentProvider


logger = get_logger(__name__)

TDeps = TypeVar("TDeps")


class AgentContainer[TDeps]:
    """Base class for agent wrappers/delegates.

    Provides consistent interface for accessing agent components.
    """

    def __init__(self, agent: AnyAgent[TDeps, Any]):
        self.agent = agent
        assert self.agent.context, "Agent must have a context!"

    @property
    def tools(self) -> ToolManager:
        """Access to tool management."""
        return self.agent.tools

    @property
    def conversation(self) -> ConversationManager:
        """Access to conversation management."""
        return self.agent.conversation

    @property
    def provider(self) -> AgentProvider[TDeps]:
        """Access to the underlying provider."""
        return self.agent._provider

    @property
    def pool(self) -> AgentPool | None:
        """Get agent's pool from context."""
        return self.agent.context.pool if self.agent.context else None

    @property
    def model_name(self) -> str | None:
        """Get current model name."""
        return self.agent.model_name

    @property
    def context(self) -> AgentContext[TDeps]:
        """Access to agent context."""
        return self.agent.context
