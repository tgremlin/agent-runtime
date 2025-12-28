"""Temporal worker entry point."""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from agent_runtime_core.utils import get_settings

from .workflows.agent_run import AgentRunWorkflow
from .activities.llm_call import call_llm
from .activities.tool_exec import execute_tool


async def main() -> None:
    """Start the Temporal worker."""
    settings = get_settings()

    print(f"Connecting to Temporal at {settings.temporal_address}")
    client = await Client.connect(settings.temporal_address)

    # Create worker with registered workflows and activities
    worker = Worker(
        client,
        task_queue="agent-runtime",
        workflows=[AgentRunWorkflow],
        activities=[call_llm, execute_tool],
    )

    print("Starting worker, listening on task queue: agent-runtime")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
