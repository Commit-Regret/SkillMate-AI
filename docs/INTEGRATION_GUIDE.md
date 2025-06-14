# SkillMate AI Integration Guide

This guide provides step-by-step instructions for integrating the SkillMate AI system with Flask backend and PostgreSQL database.

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [API Endpoints](#api-endpoints)
5. [Flask Backend Integration](#flask-backend-integration)
6. [PostgreSQL Setup](#postgresql-setup)
7. [Frontend Integration](#frontend-integration)
8. [Configuration](#configuration)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

## System Overview

SkillMate AI provides multiple specialized agents through a unified API:

- **General Assistant**: For general user queries
- **Roadmap Generator**: Creates project roadmaps
- **Project Planner**: Develops detailed project plans
- **Smart Matcher**: Matches skills to projects
- **Team Assistant**: Provides assistance in team chats

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Flask 2.0+
- API keys for OpenAI and/or Google Gemini

## Installation

1. Install SkillMate package:
```bash
pip install -r requirements.txt
```

2. Set up API keys:
```bash
# Create a .env file with your API keys
echo "OPENAI_API_KEY=your_openai_key" > .env
echo "GEMINI_API_KEY=your_gemini_key" >> .env
```

## API Endpoints

### General Assistant

```
POST /api/assistant/chat
```

**Request:**
```json
{
  "user_id": "user123",
  "message": "Hello, how can you help me?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "I can help with project planning, roadmap creation, and more...",
  "user_id": "user123"
}
```

### Roadmap Generator

```
POST /api/roadmap/generate
```

**Request:**
```json
{
  "user_id": "user123",
  "project_name": "E-commerce Platform",
  "project_description": "Build a modern e-commerce platform with payment processing",
  "timeline_months": 6,
  "team_size": 5,
  "tech_stack": ["Python", "React", "PostgreSQL"]
}
```

**Response:**
```json
{
  "success": true,
  "roadmap": {
    "phases": [
      {
        "name": "Phase 1: Planning",
        "duration": "2 weeks",
        "tasks": ["Requirement gathering", "Architecture design"]
      },
      {
        "name": "Phase 2: Development",
        "duration": "3 months",
        "tasks": ["Backend API", "Frontend UI", "Database setup"]
      },
      {
        "name": "Phase 3: Testing",
        "duration": "1 month",
        "tasks": ["Unit testing", "Integration testing", "User acceptance testing"]
      },
      {
        "name": "Phase 4: Deployment",
        "duration": "2 weeks",
        "tasks": ["Server setup", "CI/CD pipeline", "Production deployment"]
      },
      {
        "name": "Phase 5: Maintenance",
        "duration": "1 month",
        "tasks": ["Bug fixes", "Performance optimization", "Feature enhancements"]
      }
    ],
    "milestones": [
      {
        "name": "Project kickoff",
        "date": "Week 1",
        "deliverables": ["Project charter", "Initial requirements"]
      },
      {
        "name": "MVP release",
        "date": "Month 3",
        "deliverables": ["Core functionality", "Basic UI"]
      },
      {
        "name": "Final release",
        "date": "Month 5",
        "deliverables": ["Complete platform", "Documentation", "Training materials"]
      }
    ]
  }
}
```

### Project Planner

```
POST /api/planner/plan
```

**Request:**
```json
{
  "user_id": "user123",
  "project_name": "E-commerce Platform",
  "project_description": "Build a modern e-commerce platform with payment processing",
  "team_members": [
    {"name": "John", "role": "Backend Developer", "skills": ["Python", "Flask", "PostgreSQL"]},
    {"name": "Sarah", "role": "Frontend Developer", "skills": ["React", "JavaScript", "CSS"]}
  ],
  "deadline": "2023-12-31",
  "requirements": ["User authentication", "Product catalog", "Shopping cart", "Payment processing"]
}
```

**Response:**
```json
{
  "success": true,
  "plan": {
    "sprints": [
      {
        "name": "Sprint 1",
        "duration": "2 weeks",
        "goals": ["Setup project infrastructure", "Implement user authentication"],
        "tasks": [
          {
            "name": "Setup Flask project structure",
            "assignee": "John",
            "duration": "2 days",
            "dependencies": []
          },
          {
            "name": "Setup PostgreSQL database",
            "assignee": "John",
            "duration": "1 day",
            "dependencies": ["Setup Flask project structure"]
          },
          {
            "name": "Implement user authentication API",
            "assignee": "John",
            "duration": "3 days",
            "dependencies": ["Setup PostgreSQL database"]
          },
          {
            "name": "Create React project structure",
            "assignee": "Sarah",
            "duration": "2 days",
            "dependencies": []
          },
          {
            "name": "Implement login/signup UI",
            "assignee": "Sarah",
            "duration": "3 days",
            "dependencies": ["Create React project structure"]
          }
        ]
      }
    ]
  }
}
```

### Smart Matcher

```
POST /api/matcher/match
```

**Request:**
```json
{
  "user_id": "user123",
  "candidates": [
    {
      "name": "John",
      "skills": ["Python", "Flask", "PostgreSQL"],
      "experience": "5 years",
      "preferences": ["Remote", "Full-time"]
    },
    {
      "name": "Sarah",
      "skills": ["React", "JavaScript", "CSS"],
      "experience": "3 years",
      "preferences": ["On-site", "Full-time"]
    }
  ],
  "requirements": {
    "skills": ["Python", "Flask", "React"],
    "experience_level": "Mid-senior",
    "team_fit": ["Collaborative", "Self-motivated"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "matches": [
    {
      "candidate": "John",
      "match_score": 0.85,
      "matching_skills": ["Python", "Flask"],
      "missing_skills": ["React"],
      "recommendations": "John is a strong match for backend development"
    },
    {
      "candidate": "Sarah",
      "match_score": 0.70,
      "matching_skills": ["React"],
      "missing_skills": ["Python", "Flask"],
      "recommendations": "Sarah is a good match for frontend development"
    }
  ]
}
```

### Team Assistant

```
POST /api/team/chat
```

**Request:**
```json
{
  "team_id": "team123",
  "message": "We need to plan the next sprint",
  "team_info": {
    "name": "Development Team",
    "project_goal": "Build an e-commerce platform",
    "members": ["John", "Sarah"],
    "tech_stack": ["Python", "Flask", "React", "PostgreSQL"],
    "current_sprint": "Sprint 2: Product Catalog"
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "Based on your current sprint and project goals, I recommend focusing on implementing the product catalog API and UI components in the next sprint. Here's a suggested breakdown of tasks...",
  "team_id": "team123",
  "workflow_analysis": {
    "needs_planning": true,
    "needs_technical_help": false,
    "needs_coordination": true,
    "action_items": ["Define product catalog schema", "Create API endpoints", "Design UI components"]
  }
}
```

## Flask Backend Integration

### 1. Create Flask Application Structure

```
skillmate_app/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── assistant_routes.py
│   │   ├── roadmap_routes.py
│   │   ├── planner_routes.py
│   │   ├── matcher_routes.py
│   │   └── team_routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── conversation.py
│   └── services/
│       ├── __init__.py
│       └── skillmate_service.py
├── config.py
├── requirements.txt
└── run.py
```

### 2. Install Dependencies

```bash
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv skillmate
```

### 3. Create Flask App

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.routes import assistant_bp, roadmap_bp, planner_bp, matcher_bp, team_bp
    app.register_blueprint(assistant_bp, url_prefix='/api/assistant')
    app.register_blueprint(roadmap_bp, url_prefix='/api/roadmap')
    app.register_blueprint(planner_bp, url_prefix='/api/planner')
    app.register_blueprint(matcher_bp, url_prefix='/api/matcher')
    app.register_blueprint(team_bp, url_prefix='/api/team')
    
    return app
```

### 4. Configure Database

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/skillmate'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    MODEL_PROVIDER = os.environ.get('MODEL_PROVIDER') or 'gemini'
```

### 5. Create Database Models

```python
# app/models/conversation.py
from app import db
from datetime import datetime

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(64), index=True)
    sender_id = db.Column(db.String(64), index=True)
    role = db.Column(db.String(20))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
```

### 6. Create SkillMate Service

```python
# app/services/skillmate_service.py
from skillmate.ai.agents.general_assistant import GeneralAssistantAgent
from skillmate.ai.agents.roadmap_generator import RoadmapGeneratorAgent
from skillmate.ai.agents.project_planner import ProjectPlannerAgent
from skillmate.ai.agents.smart_matcher import SmartMatcherAgent
from skillmate.ai.agents.team_assistant import TeamAssistantAgent
from skillmate.ai.memory.conversation_memory import ConversationMemoryManager
from app.models import Conversation
from app import db

class SkillMateService:
    def __init__(self):
        self.memory_manager = ConversationMemoryManager()
        self.general_assistant = GeneralAssistantAgent(self.memory_manager)
        self.roadmap_generator = RoadmapGeneratorAgent()
        self.project_planner = ProjectPlannerAgent()
        self.smart_matcher = SmartMatcherAgent()
        self.team_assistant = TeamAssistantAgent(self.memory_manager)
        
    def generate_assistant_response(self, user_id, message):
        response = self.general_assistant.generate_response(user_id, message)
        
        # Save to database
        user_message = Conversation(
            conversation_id=user_id,
            sender_id=user_id,
            role='user',
            content=message
        )
        
        assistant_message = Conversation(
            conversation_id=user_id,
            sender_id='assistant',
            role='assistant',
            content=response
        )
        
        db.session.add(user_message)
        db.session.add(assistant_message)
        db.session.commit()
        
        return {
            'success': True,
            'response': response,
            'user_id': user_id
        }
    
    def generate_roadmap(self, project_details):
        return self.roadmap_generator.generate_roadmap(project_details)
    
    def create_plan(self, project_details):
        return self.project_planner.create_plan(project_details)
    
    def match_candidates(self, matching_request):
        return self.smart_matcher.match_candidates(matching_request)
    
    def process_team_message(self, team_id, message, team_info):
        return self.team_assistant.process_team_message(team_id, message, team_info)
```

### 7. Create API Routes

```python
# app/routes/assistant_routes.py
from flask import Blueprint, request, jsonify
from app.services.skillmate_service import SkillMateService

assistant_bp = Blueprint('assistant', __name__)
skillmate_service = SkillMateService()

@assistant_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'message' not in data:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    user_id = data['user_id']
    message = data['message']
    
    response = skillmate_service.generate_assistant_response(user_id, message)
    return jsonify(response)
```

```python
# app/routes/roadmap_routes.py
from flask import Blueprint, request, jsonify
from app.services.skillmate_service import SkillMateService

roadmap_bp = Blueprint('roadmap', __name__)
skillmate_service = SkillMateService()

@roadmap_bp.route('/generate', methods=['POST'])
def generate_roadmap():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Missing request data'}), 400
    
    response = skillmate_service.generate_roadmap(data)
    return jsonify(response)
```

```python
# app/routes/planner_routes.py
from flask import Blueprint, request, jsonify
from app.services.skillmate_service import SkillMateService

planner_bp = Blueprint('planner', __name__)
skillmate_service = SkillMateService()

@planner_bp.route('/plan', methods=['POST'])
def create_plan():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Missing request data'}), 400
    
    response = skillmate_service.create_plan(data)
    return jsonify(response)
```

```python
# app/routes/matcher_routes.py
from flask import Blueprint, request, jsonify
from app.services.skillmate_service import SkillMateService

matcher_bp = Blueprint('matcher', __name__)
skillmate_service = SkillMateService()

@matcher_bp.route('/match', methods=['POST'])
def match_candidates():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Missing request data'}), 400
    
    response = skillmate_service.match_candidates(data)
    return jsonify(response)
```

```python
# app/routes/team_routes.py
from flask import Blueprint, request, jsonify
from app.services.skillmate_service import SkillMateService

team_bp = Blueprint('team', __name__)
skillmate_service = SkillMateService()

@team_bp.route('/chat', methods=['POST'])
def team_chat():
    data = request.get_json()
    
    if not data or 'team_id' not in data or 'message' not in data or 'team_info' not in data:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    team_id = data['team_id']
    message = data['message']
    team_info = data['team_info']
    
    response = skillmate_service.process_team_message(team_id, message, team_info)
    return jsonify(response)
```

### 8. Create Run Script

```python
# run.py
from app import create_app, db

app = create_app()

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

## PostgreSQL Setup

### 1. Install PostgreSQL

```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# For macOS with Homebrew
brew install postgresql
```

### 2. Create Database and User

```bash
# Log in to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE skillmate;
CREATE USER skillmate_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE skillmate TO skillmate_user;
\q
```

### 3. Configure Database URL

```bash
# Add to .env file
DATABASE_URL=postgresql://skillmate_user:your_password@localhost/skillmate
```

### 4. Initialize Database

```bash
# Run Flask application to create tables
python run.py
```

## Frontend Integration

### Simple HTML/JavaScript Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>SkillMate AI Chat</title>
    <style>
        .chat-container {
            width: 500px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .messages {
            height: 300px;
            overflow-y: auto;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #eee;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .user {
            background-color: #e6f7ff;
            text-align: right;
        }
        .assistant {
            background-color: #f2f2f2;
        }
        input {
            width: 80%;
            padding: 8px;
        }
        button {
            width: 18%;
            padding: 8px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>SkillMate AI Chat</h1>
        <div class="messages" id="messages"></div>
        <div>
            <input type="text" id="message" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const userId = 'user_' + Math.random().toString(36).substring(2, 9);
        const messagesContainer = document.getElementById('messages');
        const messageInput = document.getElementById('message');

        function addMessage(content, role) {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${role}`;
            messageElement.textContent = content;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            // Add user message to chat
            addMessage(message, 'user');
            messageInput.value = '';

            try {
                // Send request to backend
                const response = await fetch('http://localhost:5000/api/assistant/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        message: message
                    }),
                });

                const data = await response.json();
                
                if (data.success) {
                    // Add assistant response to chat
                    addMessage(data.response, 'assistant');
                } else {
                    addMessage('Error: ' + (data.error || 'Unknown error'), 'assistant');
                }
            } catch (error) {
                addMessage('Error: ' + error.message, 'assistant');
            }
        }

        // Handle Enter key
        messageInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```
# API Keys
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key

# Database
DATABASE_URL=postgresql://skillmate_user:your_password@localhost/skillmate

# Application
SECRET_KEY=your_secret_key
MODEL_PROVIDER=gemini  # or "openai"
```

### Memory Configuration

To configure memory persistence with PostgreSQL:

```python
# app/services/db_memory_manager.py
from skillmate.ai.memory.conversation_memory import ConversationMemoryManager
from app.models import Conversation
from app import db
from skillmate.ai.schemas.message_schemas import MessageSchema
from datetime import datetime

class DBMemoryManager(ConversationMemoryManager):
    def add_message(self, conversation_id, message):
        # Save to in-memory store (parent implementation)
        super().add_message(conversation_id, message)
        
        # Save to database
        db_message = Conversation(
            conversation_id=conversation_id,
            sender_id=message.sender_id,
            role=message.role,
            content=message.content
        )
        
        db.session.add(db_message)
        db.session.commit()
    
    def get_messages(self, conversation_id):
        # Try to load from database first
        db_messages = Conversation.query.filter_by(conversation_id=conversation_id).order_by(Conversation.timestamp).all()
        
        if db_messages:
            # Convert to MessageSchema objects
            messages = [
                MessageSchema(
                    content=msg.content,
                    sender_id=msg.sender_id,
                    role=msg.role,
                    timestamp=msg.timestamp
                )
                for msg in db_messages
            ]
            
            # Update in-memory store
            self.conversations[conversation_id] = messages
            
            return messages
        
        # Fall back to in-memory store
        return super().get_messages(conversation_id)
```

## Testing

### 1. Test API Endpoints

```bash
# Test General Assistant
curl -X POST http://localhost:5000/api/assistant/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Hello, how can you help me?"}'

# Test Roadmap Generator
curl -X POST http://localhost:5000/api/roadmap/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "project_name": "E-commerce Platform", "project_description": "Build a modern e-commerce platform", "timeline_months": 6, "team_size": 5, "tech_stack": ["Python", "Flask", "React", "PostgreSQL"]}'
```

### 2. Run Integration Tests

Create a test script:

```python
# tests/test_api.py
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_assistant():
    response = requests.post(
        f'{BASE_URL}/assistant/chat',
        json={
            'user_id': 'test_user',
            'message': 'Hello, how can you help me?'
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data['success'] == True
    assert 'response' in data
    print('Assistant test passed!')

def test_roadmap():
    response = requests.post(
        f'{BASE_URL}/roadmap/generate',
        json={
            'user_id': 'test_user',
            'project_name': 'E-commerce Platform',
            'project_description': 'Build a modern e-commerce platform',
            'timeline_months': 6,
            'team_size': 5,
            'tech_stack': ['Python', 'Flask', 'React', 'PostgreSQL']
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data['success'] == True
    assert 'roadmap' in data
    print('Roadmap test passed!')

if __name__ == '__main__':
    test_assistant()
    test_roadmap()
```

Run the tests:

```bash
python tests/test_api.py
```

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Check that your API keys are correctly set in the `.env` file
   - Verify the API keys are valid and have sufficient quota

2. **Database Connection Issues**:
   - Ensure PostgreSQL is running: `sudo service postgresql status`
   - Verify database credentials in the `.env` file
   - Check database permissions: `\l` in psql to list databases and permissions

3. **Memory Issues**:
   - If conversations aren't persisting, check the database connection
   - Verify that the `Conversation` model has the correct fields

4. **CORS Issues**:
   - If frontend can't connect to backend, install Flask-CORS:
     ```python
     from flask_cors import CORS
     
     def create_app(config_class=Config):
         app = Flask(__name__)
         CORS(app)  # Enable CORS for all routes
         # ...
     ```

### Logging

Enable detailed logging for troubleshooting:

```python
# config.py
import logging

class Config:
    # ...
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

# app/__init__.py
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    # ...
    
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/skillmate.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('SkillMate startup')
    
    return app
```
