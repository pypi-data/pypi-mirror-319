"""Tool management for LLMling agents."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

from llmling import BaseRegistry, LLMCallableTool, ToolError
from psygnal import Signal

from llmling_agent.log import get_logger
from llmling_agent.tools.base import ToolInfo


if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from llmling_agent.agent import AnyAgent
    from llmling_agent.common_types import ToolSource, ToolType


logger = get_logger(__name__)


class ToolManager(BaseRegistry[str, ToolInfo]):
    """Manages tool registration, enabling/disabling and access.

    Inherits from BaseRegistry providing:
    - Dict-like access: manager["tool_name"] -> ToolInfo
    - Async startup/shutdown: await manager.startup()
    - Event observation: manager.add_observer(observer)
    - Registration: manager.register("tool_name", tool)
    - Listing: manager.list_items()
    - State check: manager.is_empty, manager.has_item()
    - Async iteration: async for name, tool in manager: ...
    """

    @dataclass(frozen=True)
    class ToolStateReset:
        """Emitted when tool states are reset."""

        previous_tools: dict[str, bool]
        new_tools: dict[str, bool]
        timestamp: datetime = field(default_factory=datetime.now)

    tool_states_reset = Signal(ToolStateReset)

    def __init__(
        self,
        tools: Sequence[ToolInfo | ToolType | dict[str, Any]] | None = None,
        tool_choice: bool | str | list[str] = True,
    ):
        """Initialize tool manager.

        Args:
            tools: Initial tools to register
            tool_choice: Control tool usage:
                - True: Allow all tools
                - False: No tools
                - str: Use specific tool
                - list[str]: Allow specific tools
        """
        super().__init__()
        self.tool_choice = tool_choice

        # Register initial tools
        for tool in tools or []:
            t = self._validate_item(tool)
            self.register(t.name, t)

    def __prompt__(self) -> str:
        enabled_tools = [t.name for t in self.values() if t.enabled]
        if not enabled_tools:
            return "No tools available"
        return f"Available tools: {', '.join(enabled_tools)}"

    def reset_states(self):
        """Reset all tools to their default enabled states."""
        for info in self.values():
            info.enabled = True

    @property
    def _error_class(self) -> type[ToolError]:
        """Error class for tool operations."""
        return ToolError

    def _validate_item(self, item: ToolInfo | ToolType | dict[str, Any]) -> ToolInfo:
        """Validate and convert items before registration."""
        match item:
            case ToolInfo():
                return item
            case LLMCallableTool():
                return ToolInfo(callable=item)
            case str():
                item = LLMCallableTool.from_callable(item)
                return ToolInfo(callable=item)
            case _ if callable(item):
                tool = LLMCallableTool.from_callable(item)
                return ToolInfo(callable=tool)
            case {"callable": callable_item, **config} if callable(
                callable_item
            ) or isinstance(callable_item, LLMCallableTool):
                # First convert callable to LLMCallableTool if needed
                tool = (
                    callable_item
                    if isinstance(callable_item, LLMCallableTool)
                    else LLMCallableTool.from_callable(callable_item)
                )

                # Get valid fields from ToolInfo dataclass (excluding 'callable')
                valid_keys = {f.name for f in fields(ToolInfo)} - {"callable"}
                tool_config = {k: v for k, v in config.items() if k in valid_keys}

                return ToolInfo(callable=tool, **tool_config)  # type: ignore

            case _:
                typ = type(item)
                msg = f"Item must be ToolInfo, LLMCallableTool, or callable. Got {typ}"
                raise ToolError(msg)

    def enable_tool(self, tool_name: str):
        """Enable a previously disabled tool."""
        if tool_name not in self:
            msg = f"Tool not found: {tool_name}"
            raise ToolError(msg)
        tool_info = self[tool_name]
        tool_info.enabled = True
        self.events.changed(tool_name, tool_info)
        logger.debug("Enabled tool: %s", tool_name)

    def disable_tool(self, tool_name: str):
        """Disable a tool."""
        if tool_name not in self:
            msg = f"Tool not found: {tool_name}"
            raise ToolError(msg)
        tool_info = self[tool_name]
        tool_info.enabled = False
        self.events.changed(tool_name, tool_info)
        logger.debug("Disabled tool: %s", tool_name)

    def is_tool_enabled(self, tool_name: str) -> bool:
        """Check if a tool is currently enabled."""
        return self[tool_name].enabled if tool_name in self else False

    def list_tools(self) -> dict[str, bool]:
        """Get a mapping of all tools and their enabled status."""
        return {name: info.enabled for name, info in self.items()}

    def get_tools(
        self,
        state: Literal["all", "enabled", "disabled"] = "all",
        names: list[str] | None = None,
    ) -> list[LLMCallableTool]:
        """Get tool objects based on filters."""
        filtered_tools = [
            info.callable
            for info in self.values()
            if info.matches_filter(state) and (names is None or info.name in names)
        ]

        # Sort by priority (if any have non-default priority)
        if any(self[t.name].priority != 100 for t in filtered_tools):  # noqa: PLR2004
            filtered_tools.sort(key=lambda t: self[t.name].priority)

        return filtered_tools

    def get_tool_names(
        self, state: Literal["all", "enabled", "disabled"] = "all"
    ) -> set[str]:
        """Get tool names based on state."""
        return {name for name, info in self.items() if info.matches_filter(state)}

    def register_tool(
        self,
        tool: LLMCallableTool | Callable[..., Any],
        *,
        name_override: str | None = None,
        description_override: str | None = None,
        enabled: bool = True,
        source: ToolSource = "runtime",
        priority: int = 100,
        requires_confirmation: bool = False,
        requires_capability: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> ToolInfo:
        """Register a new tool with custom settings.

        Args:
            tool: Tool to register (callable, LLMCallableTool, or config dict)
            enabled: Whether tool is initially enabled
            name_override: Optional name override for the tool
            description_override: Optional description override for the tool
            source: Tool source (runtime/agent/builtin/dynamic)
            priority: Execution priority (lower = higher priority)
            requires_confirmation: Whether tool needs confirmation
            requires_capability: Optional capability needed to use tool
            metadata: Additional tool metadata

        Returns:
            Created ToolInfo instance
        """
        # First convert to basic ToolInfo
        if not isinstance(tool, LLMCallableTool):
            llm_tool = LLMCallableTool.from_callable(
                tool,
                name_override=name_override,
                description_override=description_override,
            )
        else:
            llm_tool = tool
            llm_tool.name = name_override or llm_tool.name
            llm_tool.description = description_override or llm_tool.description

        tool_info = ToolInfo(
            llm_tool,
            enabled=enabled,
            source=source,
            priority=priority,
            requires_confirmation=requires_confirmation,
            requires_capability=requires_capability,
            metadata=metadata or {},
        )
        # Register the tool
        self.register(tool_info.name, tool_info)
        return tool_info

    def register_worker(
        self,
        worker: AnyAgent[Any, Any],
        *,
        name: str | None = None,
        reset_history_on_run: bool = True,
        pass_message_history: bool = False,
        share_context: bool = False,
        parent: AnyAgent[Any, Any] | None = None,
    ) -> ToolInfo:
        """Register an agent as a worker tool.

        Args:
            worker: Agent to register as worker
            name: Optional name override for the worker tool
            reset_history_on_run: Whether to clear history before each run
            pass_message_history: Whether to pass parent's message history
            share_context: Whether to pass parent's context/deps
            parent: Optional parent agent for history/context sharing
        """
        tool = worker.to_agent_tool(
            parent=parent,
            name=name,
            reset_history_on_run=reset_history_on_run,
            pass_message_history=pass_message_history,
            share_context=share_context,
        )
        msg = "Registering worker %s as tool %s"
        logger.debug(msg, worker.name, tool.name)
        return self.register_tool(tool, source="agent", metadata={"agent": worker.name})

    def reset(self):
        """Reset tool states."""
        old_tools = self.list_tools()
        self.reset_states()
        new_tools = self.list_tools()

        event = self.ToolStateReset(old_tools, new_tools)
        self.tool_states_reset.emit(event)
