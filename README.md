# SkillMate AI

SkillMate is an AI-powered team assistant platform that helps teams collaborate more effectively by providing intelligent assistance for project planning, technical discussions, and team coordination.

## Features

- **Team Assistant**: AI-powered assistant that remembers context and provides specialized help for technical discussions, planning, and coordination.
- **General Assistant**: Provides general AI assistance for any question or task.
- **Roadmap Generator**: Creates personalized learning roadmaps for various skills and technologies.
- **Project Planner**: Generates comprehensive project plans with requirements, architecture, and sprint planning.
- **Smart Matcher**: Matches users based on skills, interests, and project goals.
- **Resume Analysis**: Uploads and queries resumes to extract relevant information.

## Quick Start

1. Clone this repository:
```bash
git clone https://github.com/Commit-Regret/SkillMate-AI.git
cd SkillMate-AI
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the installation script:
```bash
python install.py
```

4. Set up your API keys:
```bash
python setup_api_keys.py
```

5. For detailed setup instructions, refer to [SETUP.md](SETUP.md)

## API Key Management

SkillMate AI supports multiple API key management methods:

### 1. API Key Setup Script

The `setup_api_keys.py` script helps you set up API keys interactively:

```bash
python setup_api_keys.py
```

### 2. Manual API Key Configuration

Create an `api_keys.txt` file in the `skillmate/ai/` directory with your API keys:

```
sk-your-openai-api-key-1
sk-your-openai-api-key-2
sk-your-gemini-api-key-1
sk-your-gemini-api-key-2
```

### 3. Environment Variables

You can set API keys as environment variables:
```bash
export OPENAI_API_KEY=your-api-key
export GEMINI_API_KEY=your-api-key
```

### 4. API Key Rotation

SkillMate AI includes an API key rotation system that automatically switches between multiple API keys to:
- Avoid rate limits
- Reduce costs
- Provide fallback options if a key becomes invalid

The system will automatically use the next available key when needed.

## Usage

### Running the System

```python
from skillmate.ai.main import SkillMateAI

# Initialize the system
skillmate = SkillMateAI()

# General AI chat
response = skillmate.general_ai_response("user_id", "What is a binary search tree?")

# Team assistant
response = skillmate.team_chat_ai("team_id", "user_id", "How should we structure our sprint planning?")

# Generate a learning roadmap
response = skillmate.get_roadmap("Python", "beginner", "moderate")

# Generate a project plan
response = skillmate.suggest_project_plan("team_id", "Build a real-time chat application")

# Find matching users
response = skillmate.suggest_matches("user_id")
```

### Running Tests

Note: Tests must be run from the project root directory:

```bash
# Run all tests
python -m tests.test_skillmate_system

# Test memory functionality
python -m tests.test_memory_context

# Test team memory
python -m tests.test_team_memory
```

## Project Structure

```
SkillMate-AI/
├── docs/                  # Documentation files
├── tests/                 # Test scripts and examples
├── skillmate/             # Main package
│   ├── ai/                # AI system
│   │   ├── agents/        # Agent implementations
│   │   ├── config/        # Configuration and API key management
│   │   ├── embeddings/    # Embedding services
│   │   ├── memory/        # Memory management
│   │   ├── prompts/       # Prompt templates
│   │   ├── schemas/       # Data schemas
│   │   ├── tools/         # AI tools
│   │   └── main.py        # Main entry point
├── install.py             # Installation script
├── setup_api_keys.py      # API key setup script
├── SETUP.md               # Detailed setup instructions
└── requirements.txt       # Dependencies
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 