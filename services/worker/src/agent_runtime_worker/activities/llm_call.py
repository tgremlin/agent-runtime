"""LLM call activity - makes calls to language models."""

from dataclasses import dataclass

from temporalio import activity


@dataclass
class LLMCallInput:
    """Input for the LLM call activity."""

    prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int | None = None


@dataclass
class LLMCallOutput:
    """Output from the LLM call activity."""

    content: str
    model: str
    usage: dict | None = None


@activity.defn
async def call_llm(input: LLMCallInput) -> LLMCallOutput:
    """
    Execute an LLM call.

    This activity handles:
    - Model selection (OpenAI, local via vLLM/Ollama, etc.)
    - LangFuse tracing
    - Token counting and limits
    """
    activity.logger.info(f"Calling LLM: {input.model}")

    # TODO: Implement actual LLM call
    # This is a placeholder that should be replaced with:
    # - PydanticAI agent call
    # - Direct OpenAI/Anthropic API call
    # - Local model via vLLM/Ollama

    # Placeholder response
    return LLMCallOutput(
        content=f"[Placeholder response for: {input.prompt[:50]}...]",
        model=input.model,
        usage={"prompt_tokens": 0, "completion_tokens": 0},
    )
