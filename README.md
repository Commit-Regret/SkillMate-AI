# SkillMate AI

SkillMate is an AI-powered team assistant platform that helps teams collaborate more effectively by providing intelligent assistance for project planning, technical discussions, and team coordination.

## Features

- **Team Assistant**: AI-powered assistant that remembers context and provides specialized help for technical discussions, planning, and coordination.
- **General Assistant**: Provides general AI assistance for any question or task.
- **Roadmap Generator**: Creates personalized learning roadmaps for various skills and technologies.
- **Project Planner**: Generates comprehensive project plans with requirements, architecture, and sprint planning.
- **Smart Matcher**: Matches users based on skills, interests, and project goals.
- **Resume Analysis**: Uploads and queries resumes to extract relevant information.

## Technical Architecture

- Built with Python and LangGraph for workflow-based AI agents
- Uses LangChain for LLM integration and memory management
- Supports both OpenAI and Google Gemini models
- Implements conversation memory for context-aware responses
- Features API key rotation for cost management

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up API keys in `skillmate/ai/examples/api_keys.json`
4. Run tests: `python skillmate/ai/test_skillmate_system.py`

## Testing

The system includes comprehensive tests for all components:
- Memory and context handling
- Team chat functionality
- Error handling
- General assistant capabilities
- Specialized agents (roadmap, project planning, etc.)

## Contributors

- Team SkillMate

## License

MIT License 