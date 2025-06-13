# SkillMate AI Model Provider Guide

This guide explains how to use the SkillMate AI system with different model providers.

## Overview

SkillMate AI supports multiple model providers:

- **OpenAI**: Using GPT models via the OpenAI API
- **Gemini**: Using Google's Gemini models via the Google AI API

You can easily switch between these providers and manage API keys for both.

## API Key Management

### Setting Up API Keys

The system uses a unified API key management system that supports multiple keys for each provider with automatic rotation when quota limits are reached.

To set up API keys:

```bash
# Run the interactive setup
python setup_api_keys.py

# Add a key for a specific provider
python setup_api_keys.py --add openai sk-your-openai-key
python setup_api_keys.py --add gemini your-gemini-key

# List all keys
python setup_api_keys.py --list

# Initialize default Gemini keys
python setup_api_keys.py --init-default
```

API keys are stored in `api_keys.json` in the following format:

```json
{
  "openai_keys": ["sk-key1", "sk-key2"],
  "gemini_keys": ["key1", "key2", "key3"]
}
```

### Environment Variables

You can also set API keys using environment variables:

```bash
# For OpenAI
export OPENAI_API_KEY=sk-your-openai-key

# For Gemini
export GEMINI_API_KEY=your-gemini-key
```

## Switching Between Providers

To switch between providers, set the `MODEL_PROVIDER` environment variable:

```bash
# Use OpenAI
export MODEL_PROVIDER=openai

# Use Gemini
export MODEL_PROVIDER=gemini
```

You can also switch providers programmatically:

```python
from config.model_provider import model_provider

# Switch to Gemini
model_provider.set_provider("gemini")

# Switch to OpenAI
model_provider.set_provider("openai")

# Get current provider
current_provider = model_provider.get_provider()
```

## Running Tests

The unified test script supports testing with both providers:

```bash
# Test with OpenAI (default)
python run_tests.py

# Test with Gemini
python run_tests.py --provider gemini

# Run specific tests with OpenAI
python run_tests.py --tests general roadmap planning

# Run specific tests with Gemini
python run_tests.py --provider gemini --tests general roadmap
```

Available test types:
- `general`: General AI response
- `roadmap`: Roadmap generation
- `planning`: Project planning
- `matching`: Smart matching
- `team`: Team chat AI
- `error`: Error handling

## Model Configuration

Model names for each provider are configured in `config/model_provider.py`. You can override these using environment variables:

### OpenAI Models

```bash
export GENERAL_ASSISTANT_MODEL=gpt-4
export TEAM_ASSISTANT_MODEL=gpt-4
export PLANNER_MODEL=gpt-4
export MATCHER_MODEL=gpt-4
```

### Gemini Models

```bash
export GEMINI_GENERAL_MODEL=gemini-1.5-pro
export GEMINI_TEAM_MODEL=gemini-1.5-pro
export GEMINI_PLANNER_MODEL=gemini-1.5-pro
export GEMINI_MATCHER_MODEL=gemini-1.5-pro
```

## API Key Rotation

The system automatically rotates API keys when quota limits are reached. This happens transparently to your code.

When an API quota error occurs:
1. The current key is marked as exhausted
2. The system rotates to the next available key
3. The operation is retried automatically

If all keys are exhausted, the system will wait briefly and then retry with a random key.

## Troubleshooting

### API Key Issues

If you're experiencing API key issues:

1. Check that you have valid API keys:
   ```bash
   python setup_api_keys.py --list
   ```

2. Try adding a new key:
   ```bash
   python setup_api_keys.py --add openai sk-your-new-key
   ```

3. Check environment variables:
   ```bash
   echo $OPENAI_API_KEY
   echo $GEMINI_API_KEY
   ```

### Model Provider Issues

If switching between providers isn't working:

1. Verify the current provider:
   ```python
   from config.model_provider import model_provider
   print(model_provider.get_provider())
   ```

2. Explicitly set the provider:
   ```python
   model_provider.set_provider("openai")  # or "gemini"
   ```

3. Check that you have valid API keys for the provider you're trying to use.

## Best Practices

1. **Multiple API Keys**: Add multiple API keys for each provider to handle quota limits gracefully.

2. **Testing**: Test your application with both providers to ensure compatibility.

3. **Fallback Strategy**: Implement a fallback strategy in your application to switch providers if one fails.

4. **Key Management**: Regularly rotate your API keys for security and to avoid quota issues.

5. **Environment Variables**: Use environment variables for production deployments rather than hardcoding API keys. 