# Production Readiness

- **Guardrails**: Step budget, repeated-error early stop, and strict action parsing reduce loop risk.
- **Security**: Keep API keys in environment variables, redact secrets in logs, and avoid serializing credentials into reports.
- **Scaling**: Add stronger runtime validation for activation, capture metrics with `summarize()` / `export_to_json()`, and move toward asynchronous execution if more tools are added.
- **Provider Switching**: Compare OpenAI, Gemini, and local fallback on the same prompt set before choosing a default for production.
