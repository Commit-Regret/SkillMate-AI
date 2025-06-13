# SkillMate AI Setup Guide

This guide provides detailed instructions for setting up the SkillMate AI system.

## Prerequisites

- Python 3.10+ (recommended: Python 3.13)
- pip (package manager)
- Virtual environment (optional but recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Commit-Regret/SkillMate-AI.git
cd SkillMate-AI
```

### 2. Create and Activate Virtual Environment (Optional)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Installation Script

```bash
python install.py
```

This script will:
- Verify all dependencies are installed
- Set up necessary directories
- Initialize configuration files

### 5. Set Up API Keys

You have several options for setting up API keys:

#### Option 1: Use the API Key Setup Script

```bash
python setup_api_keys.py
```

This interactive script will guide you through the process of adding API keys.

#### Option 2: Manually Create API Keys File

Create a file at `skillmate/ai/api_keys.txt` with your API keys:

```
sk-your-openai-api-key-1
sk-your-openai-api-key-2
sk-your-gemini-api-key-1
sk-your-gemini-api-key-2
```

#### Option 3: Set Environment Variables

```bash
# Windows
set OPENAI_API_KEY=your-api-key
set GEMINI_API_KEY=your-api-key

# macOS/Linux
export OPENAI_API_KEY=your-api-key
export GEMINI_API_KEY=your-api-key
```

## API Key Rotation System

SkillMate AI includes an API key rotation system that automatically switches between multiple API keys to avoid rate limits and reduce costs.

The system will:
1. Load all API keys from the `api_keys.txt` file
2. Use keys in sequence, rotating to the next key when needed
3. Track usage to avoid exceeding rate limits
4. Fall back to alternative model providers if all keys are exhausted

## Verifying Installation

Run the following command to verify that the installation was successful:

```bash
python -m tests.test_skillmate_system
```

If everything is set up correctly, you should see all tests passing.

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'langchain'**
   - Solution: Ensure you've installed all dependencies with `pip install -r requirements.txt`

2. **API Key Errors**
   - Solution: Verify your API keys are correctly formatted in `api_keys.txt`

3. **Test Failures**
   - Solution: Ensure you're running tests from the project root directory using the module format: `python -m tests.test_name`

For additional help, refer to the documentation in the `docs/` directory. 