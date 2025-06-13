# SkillMate AI System

SkillMate AI is an intelligent system designed to help developers find project partners, plan projects, and improve their skills.

## Features

- **General AI Assistant**: Chat with an AI assistant for general help and guidance
- **Roadmap Generator**: Generate learning roadmaps for different skills and technologies
- **Project Planner**: Get detailed project plans based on your team's goals
- **Smart Matching**: Find project partners based on complementary skills
- **Team Chat AI**: Get AI assistance for your team's discussions

## Model Provider Support

SkillMate AI supports multiple model providers:

- **OpenAI**: Using GPT models via the OpenAI API
- **Gemini**: Using Google's Gemini models via the Google AI API

You can easily switch between these providers based on your needs and API quotas.

## Setup

### Prerequisites

- Python 3.9+ (3.11+ recommended)
- pip (latest version)
- API keys for OpenAI and/or Google Gemini

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/skillmate.git
   cd skillmate/ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:
   ```bash
   python setup_api_keys.py
   ```
   
   This will guide you through setting up API keys for both OpenAI and Gemini.

### Configuration

You can configure the system using environment variables:

```bash
# Set the model provider (openai or gemini)
export MODEL_PROVIDER=openai

# OpenAI model configuration
export GENERAL_ASSISTANT_MODEL=gpt-3.5-turbo
export TEAM_ASSISTANT_MODEL=gpt-3.5-turbo
export PLANNER_MODEL=gpt-3.5-turbo
export MATCHER_MODEL=gpt-3.5-turbo

# Gemini model configuration
export GEMINI_GENERAL_MODEL=gemini-1.5-flash
export GEMINI_TEAM_MODEL=gemini-1.5-flash
export GEMINI_PLANNER_MODEL=gemini-1.5-flash
export GEMINI_MATCHER_MODEL=gemini-1.5-flash
```

For more configuration options, see `config/settings.py`.

## Usage

### Running Tests

To test the system:

```bash
# Test with OpenAI (default)
python run_tests.py

# Test with Gemini
python run_tests.py --provider gemini

# Run specific tests
python run_tests.py --tests general roadmap planning
```

### API Usage

You can use the system programmatically:

```python
from main import SkillMateAI

# Initialize the system
skillmate = SkillMateAI()

# Use general AI assistant
response = skillmate.general_ai_response("user123", "How do I learn React?")

# Generate a roadmap
roadmap = skillmate.get_roadmap("Python", "intermediate", "10 hours per week")

# Plan a project
plan = skillmate.suggest_project_plan(
    "team123",
    "Build a real-time chat application",
    team_size=3,
    duration="4 weeks",
    tech_preferences=["React", "Node.js", "Socket.io"]
)

# Find matches
matches = skillmate.suggest_matches("user123", limit=5)

# Use team chat AI
team_response = skillmate.team_chat_ai(
    "team123",
    "How should we structure our database?",
    user_id="user123"
)
```

## Model Provider Guide

For detailed information on using different model providers, see [MODEL_PROVIDER_GUIDE.md](MODEL_PROVIDER_GUIDE.md).

## Testing Guide

For detailed information on testing the system, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

## Setup Guide

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Complete LangGraph Multi-Agent Workflow Implementation

### Overview
The SkillMate AI system is now a comprehensive multi-agent platform built with LangChain and LangGraph, featuring sophisticated workflows for team collaboration, skill matching, roadmap generation, and project planning.

## 🎯 Key Features

### 1. Multi-Agent Architecture
- **5 Specialized Agents** with distinct LangGraph workflows
- **State-based Processing** using Pydantic models
- **Workflow Orchestration** with conditional routing
- **Comprehensive Error Handling** and fallback mechanisms

### 2. LangGraph StateGraph Workflows

#### **GeneralAssistantAgent**
- Basic conversational AI with ConversationBufferMemory
- Context-aware responses with conversation history
- Flask-compatible API endpoint: `/api/ai/general`

#### **TeamAssistantAgent** 
- **Multi-node LangGraph workflow** with 5 specialized nodes:
  - `analyzer`: Analyzes message intent and type
  - `planner`: Handles planning and sprint-related queries
  - `technical_advisor`: Provides technical guidance
  - `coordinator`: Manages team coordination
  - `responder`: Generates final responses
- **Conditional routing** based on keyword analysis
- **TeamState** Pydantic model for workflow state management
- Flask-compatible API endpoint: `/api/ai/team-chat/{teamId}`

#### **SmartMatcherAgent**
- **4-step matching workflow**:
  - `skill_analyzer`: Analyzes user skills and preferences
  - `interest_matcher`: Matches based on interests and goals
  - `compatibility_assessor`: AI-powered compatibility scoring
  - `final_ranker`: Ranks and selects top matches
- **MatchingState** for comprehensive user matching
- Flask-compatible API endpoint: `/api/ai/smart-match/{userId}`

#### **RoadmapGeneratorAgent**
- **6-step comprehensive roadmap generation**:
  - `skill_analyzer`: Analyzes skill complexity and domain
  - `prerequisite_finder`: Identifies learning prerequisites
  - `phase_planner`: Creates structured learning phases
  - `resource_curator`: Curates learning resources
  - `project_suggester`: Suggests hands-on projects
  - `roadmap_composer`: Compiles final roadmap
- **RoadmapState** for structured learning path creation
- Flask-compatible API endpoint: `/api/ai/roadmap/{skill}`

#### **ProjectPlannerAgent**
- **6-step project planning workflow**:
  - `requirements_analyzer`: Analyzes project scope and requirements
  - `architecture_designer`: Designs technical architecture
  - `sprint_planner`: Creates sprint plans and timelines
  - `risk_assessor`: Identifies risks and mitigation strategies
  - `resource_allocator`: Allocates team resources and roles
  - `plan_composer`: Compiles comprehensive project plan
- **PlanningState** for complete project planning
- Flask-compatible API endpoint: `/api/ai/project-plan`

## 🔧 Technical Implementation

### State Management
```python
# Example: TeamState for team collaboration workflow
class TeamState(BaseModel):
    message: str
    team_id: str
    message_type: str = "general"
    context: Dict[str, Any] = {}
    suggestions: List[str] = []
    response: str = ""
    processing_complete: bool = False
```

### Workflow Definition
```python
# Example: TeamAssistant LangGraph workflow
def _create_workflow(self) -> StateGraph:
    workflow = StateGraph(TeamState)
    
    # Add specialized nodes
    workflow.add_node("analyzer", self._analyze_message)
    workflow.add_node("planner", self._handle_planning)
    workflow.add_node("technical_advisor", self._provide_technical_advice)
    workflow.add_node("coordinator", self._coordinate_team)
    workflow.add_node("responder", self._generate_response)
    
    # Define conditional routing
    workflow.set_entry_point("analyzer")
    workflow.add_conditional_edges(
        "analyzer",
        self._route_message,
        {
            "planning": "planner",
            "technical": "technical_advisor", 
            "coordination": "coordinator",
            "general": "responder"
        }
    )
    
    return workflow.compile()
```

## 📊 Workflow Metadata

Each agent returns comprehensive metadata:
```python
{
    "success": True,
    "workflow_metadata": {
        "agent_type": "team_assistant_workflow",
        "workflow_complete": True,
        "processing_node": "technical_advisor",
        "workflow_steps": 5
    }
}
```

## 🚀 Flask Integration

### API Functions
All agents are accessible via Flask-compatible functions:

```python
# General AI Assistant
def general_ai_response(user_id: str, message: str) -> Dict[str, Any]

# Team Collaboration AI
def team_chat_ai(team_id: str, message: str, user_id: str = None, 
                context: Dict[str, Any] = None) -> Dict[str, Any]

# Smart User Matching
def suggest_matches(user_id: str, limit: int = 10) -> Dict[str, Any]

# Learning Roadmaps
def get_roadmap(skill: str, user_level: str = "beginner", 
               time_commitment: str = "moderate") -> Dict[str, Any]

# Project Planning
def suggest_project_plan(team_id: str, goal: str, team_size: int = 4,
                        duration: str = "4 weeks", 
                        tech_preferences: List[str] = None) -> Dict[str, Any]

# Resume Analysis
def upload_and_query_resume(user_id: str, file_stream: BinaryIO, 
                           filename: str, query: str) -> Dict[str, Any]
```

## 🎭 Agent Specializations

### Team Collaboration Features
- **Sprint Planning**: Automated sprint creation and task breakdown
- **Technical Guidance**: Architecture and implementation advice
- **Team Coordination**: Communication and workflow optimization
- **Progress Tracking**: Milestone and blocker management

### Smart Matching Features
- **Skill Compatibility**: Multi-factor skill overlap analysis
- **Interest Alignment**: Goal and project preference matching
- **Experience Balancing**: Team composition optimization
- **AI-Powered Scoring**: Comprehensive compatibility assessment

### Roadmap Generation Features
- **Skill Analysis**: Domain classification and complexity assessment
- **Prerequisites**: Foundational knowledge identification
- **Phase Planning**: Structured learning progression
- **Resource Curation**: Learning materials and practice platforms
- **Project Suggestions**: Hands-on learning projects

### Project Planning Features
- **Requirements Analysis**: Feature breakdown and scope definition
- **Architecture Design**: Technology stack and system design
- **Sprint Planning**: Timeline and milestone creation
- **Risk Assessment**: Risk identification and mitigation strategies
- **Resource Allocation**: Team roles and responsibility distribution

## 🔮 Advanced Features

### Memory Management
- **Persistent Conversations**: Disk-based conversation storage
- **Context Preservation**: Multi-turn conversation handling
- **Team Memory**: Shared team conversation history

### Vector Embeddings
- **Resume Processing**: Document embedding and similarity search
- **Skill Matching**: Vector-based skill compatibility
- **Content Retrieval**: Semantic search for relevant information

### Configuration Management
- **Environment-based Settings**: Flexible configuration
- **Model Selection**: Multiple LLM model support
- **API Key Management**: Secure credential handling

## 🚀 Deployment Ready

The system is production-ready with:
- **Error Handling**: Comprehensive try-catch blocks with fallbacks
- **Logging**: Structured logging for debugging and monitoring
- **Type Safety**: Pydantic models for data validation
- **Modular Design**: Clean separation of concerns
- **Scalable Architecture**: Easy to extend and maintain

## 🎉 Hackathon Ready

Perfect for **Intra-CCS Hackathon 2025** with:
- **Complete AI Backend**: All required functionality implemented
- **Flask Integration**: Ready for immediate backend integration
- **Multi-Agent Workflows**: Sophisticated LangGraph implementation
- **Production Quality**: Comprehensive error handling and logging
- **Extensible Design**: Easy to add new features and agents

---

**SkillMate AI System** - *Where AI Meets Collaboration* 🤝🚀 