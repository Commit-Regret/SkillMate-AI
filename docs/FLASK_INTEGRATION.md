# SkillMate AI Flask & PostgreSQL Integration Guide

This guide provides step-by-step instructions for integrating the SkillMate AI system with a Flask backend and PostgreSQL database.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [API Endpoints](#api-endpoints)
4. [Flask Setup](#flask-setup)
5. [PostgreSQL Setup](#postgresql-setup)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Flask 2.0+
- API keys for OpenAI and/or Google Gemini

## Installation

1. Install required packages:

```bash
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv
```

2. Install SkillMate package:

```bash
pip install -r requirements.txt
```

3. Set up API keys:

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

**Response:** (abbreviated)
```json
{
  "success": true,
  "roadmap": {
    "phases": [
      {
        "name": "Phase 1: Planning",
        "duration": "2 weeks",
        "tasks": ["Requirement gathering", "Architecture design"]
      }
    ],
    "milestones": [
      {
        "name": "Project kickoff",
        "date": "Week 1",
        "deliverables": ["Project charter", "Initial requirements"]
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

**Response:** (abbreviated)
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
  "response": "Based on your current sprint and project goals, I recommend focusing on implementing the product catalog API and UI components in the next sprint.",
  "team_id": "team123",
  "workflow_analysis": {
    "needs_planning": true,
    "needs_technical_help": false,
    "needs_coordination": true,
    "action_items": ["Define product catalog schema", "Create API endpoints", "Design UI components"]
  }
}
```

## Flask Setup

### 1. Project Structure

Create the following directory structure:

```
skillmate_app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── services.py
├── config.py
├── .env
└── run.py
```

### 2. Configuration

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

### 3. Database Models

```python
# app/models.py
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

### 4. Flask Application

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
    
    from app import routes
    
    return app
```

### 5. SkillMate Service

```python
# app/services.py
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

### 6. Routes

```python
# app/routes.py
from flask import request, jsonify, Blueprint
from app.services import SkillMateService

skillmate_service = SkillMateService()

# General Assistant routes
@Blueprint('assistant', __name__)
def create_assistant_routes():
    bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')
    
    @bp.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'message' not in data:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        user_id = data['user_id']
        message = data['message']
        
        response = skillmate_service.generate_assistant_response(user_id, message)
        return jsonify(response)
    
    return bp

# Roadmap Generator routes
def create_roadmap_routes():
    bp = Blueprint('roadmap', __name__, url_prefix='/api/roadmap')
    
    @bp.route('/generate', methods=['POST'])
    def generate_roadmap():
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Missing request data'}), 400
        
        response = skillmate_service.generate_roadmap(data)
        return jsonify(response)
    
    return bp

# Project Planner routes
def create_planner_routes():
    bp = Blueprint('planner', __name__, url_prefix='/api/planner')
    
    @bp.route('/plan', methods=['POST'])
    def create_plan():
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Missing request data'}), 400
        
        response = skillmate_service.create_plan(data)
        return jsonify(response)
    
    return bp

# Smart Matcher routes
def create_matcher_routes():
    bp = Blueprint('matcher', __name__, url_prefix='/api/matcher')
    
    @bp.route('/match', methods=['POST'])
    def match_candidates():
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Missing request data'}), 400
        
        response = skillmate_service.match_candidates(data)
        return jsonify(response)
    
    return bp

# Team Assistant routes
def create_team_routes():
    bp = Blueprint('team', __name__, url_prefix='/api/team')
    
    @bp.route('/chat', methods=['POST'])
    def team_chat():
        data = request.get_json()
        
        if not data or 'team_id' not in data or 'message' not in data or 'team_info' not in data:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        team_id = data['team_id']
        message = data['message']
        team_info = data['team_info']
        
        response = skillmate_service.process_team_message(team_id, message, team_info)
        return jsonify(response)
    
    return bp

def register_blueprints(app):
    app.register_blueprint(create_assistant_routes())
    app.register_blueprint(create_roadmap_routes())
    app.register_blueprint(create_planner_routes())
    app.register_blueprint(create_matcher_routes())
    app.register_blueprint(create_team_routes())
```

Update the `__init__.py` to register the blueprints:

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
    
    from app.routes import register_blueprints
    register_blueprints(app)
    
    return app
```

### 7. Run Script

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

# For Windows
# Download and install from https://www.postgresql.org/download/windows/
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

### 5. PostgreSQL Memory Manager

Create a custom memory manager that uses PostgreSQL for persistence:

```python
# app/db_memory_manager.py
from skillmate.ai.memory.conversation_memory import ConversationMemoryManager
from skillmate.ai.schemas.message_schemas import MessageSchema
from app.models import Conversation
from app import db
from datetime import datetime

class PostgreSQLMemoryManager(ConversationMemoryManager):
    """Memory manager that stores conversations in PostgreSQL."""
    
    def add_message(self, conversation_id, message):
        # Call parent implementation to update in-memory store
        super().add_message(conversation_id, message)
        
        # Store in database
        db_message = Conversation(
            conversation_id=conversation_id,
            sender_id=message.sender_id,
            role=message.role,
            content=message.content
        )
        
        db.session.add(db_message)
        db.session.commit()
    
    def get_messages(self, conversation_id):
        # Check if we already have messages in memory
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]
        
        # Try to load from database
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
        
        # No messages found
        return []
```

Update the service to use the PostgreSQL memory manager:

```python
# app/services.py
from app.db_memory_manager import PostgreSQLMemoryManager

class SkillMateService:
    def __init__(self):
        self.memory_manager = PostgreSQLMemoryManager()
        self.general_assistant = GeneralAssistantAgent(self.memory_manager)
        # ...
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

### 2. Create a Test Script

```python
# test_api.py
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
python test_api.py
```

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Check that your API keys are correctly set in the `.env` file
   - Verify the API keys are valid and have sufficient quota
   - Error message: "Authentication error" or "API key not valid"

2. **Database Connection Issues**:
   - Ensure PostgreSQL is running
   - Verify database credentials in the `.env` file
   - Error message: "Could not connect to PostgreSQL" or "Database connection error"

3. **Import Errors**:
   - Make sure all required packages are installed
   - Check that the SkillMate package is properly installed
   - Error message: "ModuleNotFoundError: No module named 'skillmate'"

4. **Memory Issues**:
   - If conversations aren't persisting, check the database connection
   - Verify that the `Conversation` model has the correct fields
   - Error message: "Table 'conversation' doesn't exist"

### Debugging Tips

1. Enable Flask debugging:
```python
app.run(debug=True)
```

2. Add logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. Check PostgreSQL logs:
```bash
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

4. Verify database tables:
```bash
sudo -u postgres psql -d skillmate -c "\dt"
```

5. Check database contents:
```bash
sudo -u postgres psql -d skillmate -c "SELECT * FROM conversation LIMIT 10;"
```
