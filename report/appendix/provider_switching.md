# Provider Switching

| Provider | Strength | Trade-off |
| :--- | :--- | :--- |
| OpenAI | Strong reasoning quality | Higher cost and often higher latency |
| Gemini | Good fallback quality | Output style can differ from OpenAI |
| Local | Zero API cost | Lower quality and slower CPU inference |

Recommended benchmark fields:
- latency
- answer quality
- tool-call reliability
- total cost
