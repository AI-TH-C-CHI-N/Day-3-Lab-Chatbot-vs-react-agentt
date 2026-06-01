# UC06 - Provider Switching

| Field | Value |
| :--- | :--- |
| Input | Run the same prompt under OpenAI and Gemini to compare latency and quality. |
| Path | User -> Provider Factory -> OpenAIProvider / GeminiProvider -> ReActAgent |
| Expected Result | Both providers work through the same agent interface with different performance profiles. |
| Insight | Provider switching makes the system flexible without rewriting the agent loop. |
