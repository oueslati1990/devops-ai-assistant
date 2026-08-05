from prometheus_client import Counter, Histogram

llm_latency = Histogram(
    "llm_call_duration_seconds",
    "Time spent waiting for the LLM to respond",
    buckets=[0.5, 1, 2, 5, 10, 30, 60, 120],
)

llm_token_prompt = Counter(
    "llm_token_prompt_total",
    "Total prompt tokens sent to the LLM",
)

llm_tokens_completion = Counter(
    "llm_tokens_completion_total",
    "Total completion tokens received from the LLM",
)

tool_iterations = Histogram(
    "agent_tool_iterations",
    "Number of tool call iterations per chat request ",
    buckets=[1, 2, 3, 4, 5, 6, 7, 8],
)
