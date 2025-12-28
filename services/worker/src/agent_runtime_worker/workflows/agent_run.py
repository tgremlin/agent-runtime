"""Agent Run Workflow - durable execution of an agent."""

from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from uuid import UUID

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from ..activities.llm_call import call_llm, LLMCallInput, LLMCallOutput
    from ..activities.tool_exec import execute_tool, ToolExecInput, ToolExecOutput


@dataclass
class AgentRunInput:
    """Input for the AgentRunWorkflow."""

    run_id: str
    tenant_id: str
    agent_id: str
    agent_version_id: str
    config: dict[str, Any]
    input: dict[str, Any]


@dataclass
class AgentRunOutput:
    """Output from the AgentRunWorkflow."""

    run_id: str
    status: str
    output: dict[str, Any] | None = None
    error: str | None = None


@workflow.defn
class AgentRunWorkflow:
    """
    Durable workflow for executing an agent run.

    This workflow orchestrates the execution of an agent, handling:
    - LLM calls
    - Tool execution
    - State persistence
    - Pause/resume via signals
    - Retry logic with backoff
    """

    def __init__(self) -> None:
        self._is_paused = False
        self._should_cancel = False

    @workflow.run
    async def run(self, input: AgentRunInput) -> AgentRunOutput:
        """Execute the agent run workflow."""
        workflow.logger.info(f"Starting agent run: {input.run_id}")

        try:
            # Wait if paused
            await workflow.wait_condition(lambda: not self._is_paused)

            if self._should_cancel:
                return AgentRunOutput(
                    run_id=input.run_id,
                    status="cancelled",
                )

            # Example: Simple agent loop
            # In practice, this would be driven by agent config/type
            llm_result = await workflow.execute_activity(
                call_llm,
                LLMCallInput(
                    prompt=str(input.input.get("prompt", "Hello")),
                    model=input.config.get("model", "gpt-4"),
                ),
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=workflow.RetryPolicy(
                    maximum_attempts=3,
                    initial_interval=timedelta(seconds=1),
                    backoff_coefficient=2.0,
                ),
            )

            # Check for pause/cancel between steps
            await workflow.wait_condition(lambda: not self._is_paused)
            if self._should_cancel:
                return AgentRunOutput(run_id=input.run_id, status="cancelled")

            # Return successful result
            return AgentRunOutput(
                run_id=input.run_id,
                status="completed",
                output={"response": llm_result.content},
            )

        except Exception as e:
            workflow.logger.error(f"Agent run failed: {e}")
            return AgentRunOutput(
                run_id=input.run_id,
                status="failed",
                error=str(e),
            )

    @workflow.signal
    async def pause(self) -> None:
        """Signal to pause the workflow."""
        workflow.logger.info("Received pause signal")
        self._is_paused = True

    @workflow.signal
    async def resume(self) -> None:
        """Signal to resume the workflow."""
        workflow.logger.info("Received resume signal")
        self._is_paused = False

    @workflow.signal
    async def cancel(self) -> None:
        """Signal to cancel the workflow."""
        workflow.logger.info("Received cancel signal")
        self._should_cancel = True
        self._is_paused = False  # Unblock if paused

    @workflow.query
    def is_paused(self) -> bool:
        """Query whether the workflow is paused."""
        return self._is_paused
