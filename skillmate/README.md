# SkillMate AI System

A comprehensive AI-powered system for team formation, collaboration, and project management built for the Intra-CCS Hackathon 2025 at IIT Indore.

## 🚀 Overview

SkillMate AI is a modular, production-ready AI system that powers the SkillMate platform. It provides intelligent features for:

- **General AI Assistant**: Context-aware conversational AI with memory
- **Resume Q&A**: Document embedding and intelligent querying
- **Project Planning**: Automated sprint planning and roadmap generation  
- **Smart Matching**: AI-driven teammate suggestions based on skills and compatibility
- **Team Collaboration**: Specialized team AI assistant for project guidance

## 🏗️ Architecture

The system is built using:

- **LangChain**: For LLM orchestration and chains
- **LangGraph**: For multi-agent workflows and control flow
- **OpenAI GPT-4/3.5 or Gemini**: For language models (supports both providers)
- **FAISS/Chroma**: For vector storage and similarity search
- **ConversationBufferMemory**: For maintaining chat context

## 📁 Project Structure

```
skillmate/ai/
├── __init__.py
├── main.py                     # Main API functions (Flask-compatible)
├── config/
│   ├── __init__.py
│   ├── settings.py             # Configuration and environment variables
│   └── model_provider.py       # Unified model provider for OpenAI/Gemini
├── agents/
│   ├── __init__.py
│   ├── general_assistant.py   # General AI assistant
│   ├── team_assistant.py      # Team-specific AI assistant
│   ├── roadmap_generator.py   # Learning roadmap generation
│   ├── project_planner.py     # Sprint and project planning
│   └── smart_matcher.py       # User matching and compatibility
├── memory/
│   ├── __init__.py
│   └── conversation_memory.py # Conversation history management
├── embeddings/
│   ├── __init__.py
│   ├── vector_store.py        # FAISS/Chroma vector store management
│   └── embedding_service.py   # Document processing and embedding
├── prompts/
│   ├── __init__.py
│   ├── assistant_prompts.py   # General assistant prompts
│   ├── team_prompts.py        # Team collaboration prompts
│   ├── planning_prompts.py    # Project planning prompts
│   └── matching_prompts.py    # User matching prompts
├── schemas/
│   ├── __init__.py
│   ├── message_schemas.py     # Message and conversation schemas
│   ├── user_schemas.py        # User profile schemas
│   └── team_schemas.py        # Team and project schemas
├── docs/
│   └── model_provider_guide.md # Guide for using the model provider system
└── tools/
    ├── __init__.py
    ├── resume_tools.py         # Resume analysis tools
    ├── planning_tools.py       # Project planning tools
    └── matching_tools.py       # User matching tools
```

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   cd skillmate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   # Choose model provider: "openai" or "gemini"
   MODEL_PROVIDER=openai
   
   # OpenAI configuration
   OPENAI_API_KEY=your_openai_api_key_here
   GENERAL_ASSISTANT_MODEL=gpt-3.5-turbo
   TEAM_ASSISTANT_MODEL=gpt-4
   PLANNER_MODEL=gpt-4
   
   # Gemini configuration (optional, default keys are provided)
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_GENERAL_MODEL=gemini-1.5-flash
   GEMINI_TEAM_MODEL=gemini-1.5-flash
   GEMINI_PLANNER_MODEL=gemini-1.5-flash
   
   # Vector database configuration
   VECTOR_DB_TYPE=faiss
   VECTOR_DB_PATH=./vector_db
   EMBEDDING_MODEL=text-embedding-3-small
   
   # Memory and document processing
   MEMORY_TOKEN_LIMIT=4000
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   ```

## 🚀 Usage

### Basic Setup

```python
from skillmate.ai.main import (
    general_ai_response,
    upload_and_query_resume,
    get_roadmap,
    suggest_project_plan,
    suggest_matches,
    team_chat_ai
)
```

### API Functions

#### 1. General AI Assistant

```python
response = general_ai_response(
    user_id="user123",
    message="How do I learn React?"
)
print(response["response"])
```

#### 2. Resume Q&A

```python
with open("resume.pdf", "rb") as file:
    result = upload_and_query_resume(
        user_id="user123",
        file_stream=file,
        filename="resume.pdf",
        query="What are my strongest technical skills?"
    )
    print(result["answer"])
```

#### 3. Learning Roadmap Generation

```python
roadmap = get_roadmap(skill="Machine Learning")
print(roadmap["roadmap"])
```

#### 4. Project Planning

```python
plan = suggest_project_plan(
    team_id="team456",
    goal="Build a social media analytics dashboard",
    team_size=4,
    duration="2 weeks"
)
print(plan["project_plan"])
```

#### 5. Smart Matching

```python
user_profile = {
    "name": "Alice",
    "skills": ["Python", "React", "MongoDB"],
    "interests": ["Web Development", "AI"],
    "bio": "Full-stack developer interested in AI applications"
}

candidate_profiles = [
    {
        "name": "Bob",
        "skills": ["Node.js", "Express", "PostgreSQL"],
        "interests": ["Backend Development", "APIs"],
        "bio": "Backend specialist with 3 years experience"
    }
]

matches = suggest_matches(
    user_id="user123",
    user_profile=user_profile,
    candidate_profiles=candidate_profiles
)
print(matches["matches"])
```

#### 6. Team AI Assistant

```python
team_info = {
    "name": "Team Alpha",
    "project_goal": "Build a task management app",
    "members": ["Alice", "Bob", "Charlie"]
}

response = team_chat_ai(
    team_id="team456",
    message="We're having trouble with user authentication",
    team_info=team_info
)
print(response["response"])
```

## 🔄 Model Provider System

SkillMate AI supports both OpenAI and Gemini models through a unified model provider system.

### Switching Between Providers

You can switch between providers by setting the `MODEL_PROVIDER` environment variable:

```bash
# Use OpenAI models (default)
export MODEL_PROVIDER=openai

# Use Gemini models
export MODEL_PROVIDER=gemini
```

Or programmatically:

```python
from skillmate.ai.config.model_provider import model_provider

# Switch to Gemini
model_provider.set_provider("gemini")
```

### API Key Management

API keys are stored in a single JSON file (`api_keys.json`) and automatically rotated when quota limits are reached.

```python
from skillmate.ai.config.model_provider import key_manager

# Add a new API key
key_manager.add_openai_key("sk-abc123...")
key_manager.add_gemini_key("AIzaSyB...")
```

### Fallback Behavior

The system includes intelligent fallback mechanisms:

1. If OpenAI keys are exhausted, it falls back to Gemini
2. If no API keys are available for embeddings, it uses DummyEmbeddings
3. Default Gemini API keys are provided to ensure the system works out of the box

For more details, see the [Model Provider Guide](ai/docs/model_provider_guide.md).

## 🔗 Flask Integration

The system is designed to be Flask-compatible. Here's an example integration:

```python
from flask import Flask, request, jsonify
from skillmate.ai.main import general_ai_response, upload_and_query_resume

app = Flask(__name__)

@app.route('/api/ai/general', methods=['POST'])
def api_general_assistant():
    data = request.json
    result = general_ai_response(
        user_id=data['user_id'],
        message=data['message']
    )
    return jsonify(result)

@app.route('/api/ai/upload-resume', methods=['POST'])
def api_resume_upload():
    file = request.files['file']
    user_id = request.form['user_id']
    query = request.form['query']
    
    result = upload_and_query_resume(
        user_id=user_id,
        file_stream=file.stream,
        filename=file.filename,
        query=query
    )
    return jsonify(result)
```

## 🧠 Key Features

### Memory Management
- Persistent conversation history
- Context-aware responses
- User-specific memory isolation

### Document Processing
- Support for PDF, DOCX, TXT, CSV, HTML
- Intelligent chunking and embedding
- Semantic search capabilities

### Smart Matching
- Skill compatibility analysis
- Interest-based recommendations
- Project context consideration

### Team Collaboration
- Team-specific AI assistants
- Sprint planning automation
- Project roadmap generation

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PROVIDER` | Model provider to use ("openai" or "gemini") | "openai" |
| `OPENAI_API_KEY` | OpenAI API key | Required for OpenAI |
| `GEMINI_API_KEY` | Gemini API key | Optional (defaults provided) |
| `VECTOR_DB_TYPE` | Vector database type ("faiss" or "chroma") | "faiss" |
| `VECTOR_DB_PATH` | Path to store vector databases | "./vector_db" |
| `EMBEDDING_MODEL` | OpenAI embedding model | "text-embedding-3-small" |
| `GENERAL_ASSISTANT_MODEL` | Model for general assistant | "gpt-3.5-turbo" |
| `TEAM_ASSISTANT_MODEL` | Model for team assistant | "gpt-4" |
| `MEMORY_TOKEN_LIMIT` | Maximum tokens in memory | 4000 |
| `CHUNK_SIZE` | Document chunk size | 1000 |
| `CHUNK_OVERLAP` | Chunk overlap size | 200 |

### Feature Flags

```bash
ENABLE_ROADMAP_GENERATOR=True
ENABLE_PROJECT_PLANNER=True
ENABLE_RESUME_QA=True
ENABLE_SMART_MATCHING=True
```

## 📊 Backend API Endpoints

The system is designed to integrate with these backend endpoints:

- `/api/ai/general` - General GPT assistant
- `/api/ai/team-chat/{teamId}` - Group AI chat
- `/api/ai/personal/{userA}/{userB}` - AI in 1-on-1 chat
- `/api/ai/upload-resume` - Upload doc, parse, embed
- `/api/ai/query-resume/{userId}` - Resume Q&A
- `/api/ai/smart-match/{userId}` - AI-based people suggestions

## 🎯 Production Considerations

### Performance
- Caching of conversation chains
- Efficient vector store operations
- Batched embedding processing

### Security
- User data isolation
- Secure file handling
- API key protection

### Scalability
- Modular architecture
- Stateless design (except for memory)
- Database-agnostic vector storage

## 🚨 Error Handling

The system includes comprehensive error handling:

```python
{
    "success": False,
    "error": "Error message",
    "timestamp": "2024-01-15T10:30:00",
    "user_id": "user123"
}
```

## 🤝 Contributing

1. Follow the modular architecture
2. Add comprehensive docstrings
3. Include error handling
4. Write tests for new features
5. Update this README for new functionality

## 📝 License

This project is part of the SkillMate platform for the Intra-CCS Hackathon 2025.

## 🎉 Features Implemented

✅ General AI Assistant with Memory  
✅ Resume Q&A with Vector Embeddings  
✅ Learning Roadmap Generation  
✅ Project Planning and Sprint Management  
✅ Smart User Matching  
✅ Team AI Assistant  
✅ Flask-Compatible API Functions  
✅ Comprehensive Error Handling  
✅ Modular Architecture  
✅ Production-Ready Configuration  
✅ Multi-Provider Support (OpenAI & Gemini)  
✅ Automatic API Key Rotation  

---

Built with ❤️ for the Intra-CCS Hackathon 2025 at IIT Indore 