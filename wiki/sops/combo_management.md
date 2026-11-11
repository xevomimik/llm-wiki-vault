# SOP: Combo Management & Testing

## Context
Ensuring reliability across the 9 primary combos.

## Active Combos
`FLAGSHIP`, `ROUND-ROBIN`, `NVIDIA`, `GOOGLE`, `OPENROUTER`, `CEREBRAS`, `CODING`, `VISION-MULTIMODAL`, `PS5LM PLUS`.

## Procedure
1. **Model Selection**: Only add models that have passed the *Individual Model Testing* SOP.
2. **Order/Strategy**:
   - `Priority`: Use for tiered fallback (e.g., FLAGSHIP).
   - `Round Robin`: Use for high-throughput/free-tier rotation (e.g., ROUND-ROBIN).
3. **Validation**:
   - Send a "ping" or "hello" through the Hermes chat.
   - Verify reply from the expected provider.
4. **PS5 Fallback**: Every cloud-heavy combo (FLAGSHIP, CODING, etc.) should have `PS5LM PLUS` as the final priority fallback.
