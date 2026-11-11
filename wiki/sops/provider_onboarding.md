# SOP: Provider Onboarding (Video Workflow)

## Context
Standardized process for adding free-tier providers to OmniRoute as demonstrated in the [Claude Code Free Setup Video](https://www.youtube.com/watch?v=1GWGCjrgppI).

## Steps
1. **API Key Retrieval**: Obtain free-tier API key from provider (OpenRouter, NVIDIA, etc.).
2. **Key Storage**: Add key to OmniRoute encrypted environment:
   `omniroute providers set-key <provider> <key>`
3. **Individual Model Testing**:
   - Go to `localhost:20128/models`.
   - Run the "Test" button for EACH specific model individually.
   - **Constraint**: Do not batch import or add to combos before an individual live test passes.
4. **Activation**: Enable only the specific models that passed the live test.
5. **Persistence**: Ensure keys are retained even if models are temporarily deactivated due to transient errors (e.g., credit exhaustion).
