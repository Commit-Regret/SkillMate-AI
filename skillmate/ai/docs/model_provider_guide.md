# SkillMate AI Model Provider Guide

This guide explains how to use the unified model provider system in SkillMate AI, which supports both OpenAI and Gemini models.

## Overview

The model provider system allows seamless switching between OpenAI and Gemini models for both language model (LLM) operations and embeddings. It includes automatic API key rotation when quota limits are reached.

## Key Components

1. **ModelProvider**: Factory class for creating LLM and embedding instances
2. **APIKeyManager**: Handles API key storage, retrieval, and rotation
3. **DummyEmbeddings**: Fallback when no API keys are available

## Configuration

### Setting the Model Provider

You can set the model provider using the `MODEL_PROVIDER` environment variable:

```bash
# For OpenAI (default)
export MODEL_PROVIDER=openai

# For Gemini
export MODEL_PROVIDER=gemini
```

Alternatively, you can set it programmatically:

```python
from skillmate.ai.config.model_provider import model_provider

# Set provider to Gemini
model_provider.set_provider("gemini")

# Get current provider
current_provider = model_provider.get_provider()
```

### API Key Management

API keys are stored in a single JSON file (`api_keys.json` by default) with the following structure:

```json
{
  "openai_keys": [
    "sk-abc123...",
    "sk-def456..."
  ],
  "gemini_keys": [
    "AIzaSyB...",
    "AIzaSyC..."
  ]
}
```

You can also set keys via environment variables:
- `OPENAI_API_KEY` for OpenAI
- `GEMINI_API_KEY` for Gemini

#### Adding or Removing API Keys

```python
from skillmate.ai.config.model_provider import key_manager

# Add keys
key_manager.add_openai_key("sk-abc123...")
key_manager.add_gemini_key("AIzaSyB...")

# Remove keys
key_manager.remove_openai_key("sk-abc123...")
key_manager.remove_gemini_key("AIzaSyB...")
```

## Usage

### Creating LLM Instances

```python
from skillmate.ai.config.model_provider import model_provider

# Create LLM for general assistant
llm = model_provider.create_llm(
    model_type="general_assistant",
    temperature=0.7
)

# Available model types:
# - "general_assistant"
# - "team_assistant"
# - "planner"
# - "matcher"

# The appropriate model will be selected based on the current provider
```

### Creating Embedding Models

```python
from skillmate.ai.config.model_provider import model_provider

# Create embeddings model
embeddings = model_provider.create_embeddings()

# This will return:
# - OpenAIEmbeddings if provider is "openai" and keys are available
# - GoogleGenerativeAIEmbeddings if provider is "gemini" and keys are available
# - DummyEmbeddings if no keys are available
```

### Error Handling and API Key Rotation

The system includes a decorator for automatic API key rotation when quota limits are reached:

```python
from skillmate.ai.config.model_provider import with_api_key_rotation

@with_api_key_rotation(max_retries=3, retry_delay=1.0)
def my_llm_function(user_id, message):
    # If this function encounters a quota error,
    # it will automatically rotate to the next API key
    # and retry up to max_retries times
    response = llm.predict(message)
    return response
```

## Model Mappings

### OpenAI Models

The default OpenAI models are:

- `general_assistant`: `gpt-3.5-turbo` (configurable via `GENERAL_ASSISTANT_MODEL`)
- `team_assistant`: `gpt-3.5-turbo` (configurable via `TEAM_ASSISTANT_MODEL`)
- `planner`: `gpt-3.5-turbo` (configurable via `PLANNER_MODEL`)
- `matcher`: `gpt-3.5-turbo` (configurable via `MATCHER_MODEL`)

### Gemini Models

The default Gemini models are:

- `general_assistant`: `gemini-1.5-flash` (configurable via `GEMINI_GENERAL_MODEL`)
- `team_assistant`: `gemini-1.5-flash` (configurable via `GEMINI_TEAM_MODEL`)
- `planner`: `gemini-1.5-flash` (configurable via `GEMINI_PLANNER_MODEL`)
- `matcher`: `gemini-1.5-flash` (configurable via `GEMINI_MATCHER_MODEL`)

## Fallback Behavior

1. If no OpenAI keys are available when using the OpenAI provider, the system will fall back to Gemini.
2. If no Gemini keys are available when using the Gemini provider, the system will attempt to use default Gemini keys.
3. For embeddings, if no keys are available for either provider, the system will use DummyEmbeddings.

## Example: Complete Usage

```python
import os
from skillmate.ai.config.model_provider import model_provider, with_api_key_rotation

# Set provider based on environment or configuration
provider = os.getenv("MODEL_PROVIDER", "openai")
model_provider.set_provider(provider)

# Create LLM
llm = model_provider.create_llm(
    model_type="general_assistant",
    temperature=0.7
)

# Create embeddings
embeddings = model_provider.create_embeddings()

# Use with automatic key rotation
@with_api_key_rotation(max_retries=3)
def generate_response(prompt):
    return llm.predict(prompt)

# Generate response
response = generate_response("Tell me about SkillMate AI")
print(response)
```

## Best Practices

1. Always use the model provider factory instead of directly instantiating models
2. Use the `with_api_key_rotation` decorator for functions that make API calls
3. Provide multiple API keys for each provider to enable rotation
4. Check the current provider before making provider-specific operations
5. Handle potential exceptions when no API keys are available

## Troubleshooting

### Common Issues

1. **No API keys available**: Ensure you have added API keys to the `api_keys.json` file or set the appropriate environment variables.

2. **API quota exceeded**: If you see quota errors even with rotation, you may need to add more API keys or wait for quota reset.

3. **Invalid model**: Check that the model names in your environment variables are valid for the respective providers.

4. **DummyEmbeddings being used**: This indicates that no valid API keys are available for embeddings. Check your API key configuration. 