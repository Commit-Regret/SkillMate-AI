# SkillMate AI System - Setup Guide 🚀

## Quick Start - Get Running in 5 Minutes!

### 🚀 **Super Easy Installation (Recommended)**
```bash
cd skillmate/ai
python install.py
```
This automated script will:
- ✅ Check Python version (including Python 3.13 support!)
- ✅ Install all dependencies with correct versions
- ✅ Create necessary directories
- ✅ Check API key setup
- ✅ Test the installation

**🐍 Python 3.13 Users:** The installer automatically detects Python 3.13 and uses compatible packages. See [PYTHON313_SETUP.md](PYTHON313_SETUP.md) for details.

### 📝 **Manual Installation**

**Step 1: API Key Setup (Required)**

**Option A: Using .env file (Recommended)**
```bash
# Create .env file in skillmate/ai/ directory
echo 'OPENAI_API_KEY=your_openai_api_key_here' > .env
```

**Option B: Using Environment Variables**

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_openai_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

**Step 2: Install Dependencies**
```bash
cd skillmate/ai

# For Python 3.13 users:
pip install -r ../requirements-python313.txt

# For Python 3.11/3.12 - stable, tested versions (recommended):
pip install -r ../requirements-stable.txt

# Or use latest versions (may have compatibility issues):
pip install -r ../requirements.txt
```

**Step 3: Run Tests**
```bash
python run_tests.py
```

## 🔧 Detailed Configuration

### API Keys Setup

**Get OpenAI API Key:**
1. Go to [OpenAI API Platform](https://platform.openai.com/)
2. Sign up/Login
3. Go to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-`)

**Set the API Key:**

Create a `.env` file in the `skillmate/ai/` directory:
```env
# REQUIRED: Your OpenAI API Key
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Model Configuration

**Default Models (Balanced Cost/Performance):**
```env
GENERAL_ASSISTANT_MODEL=gpt-3.5-turbo
TEAM_ASSISTANT_MODEL=gpt-4
PLANNER_MODEL=gpt-4
MATCHER_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
```

**Budget-Friendly Configuration:**
```env
GENERAL_ASSISTANT_MODEL=gpt-3.5-turbo
TEAM_ASSISTANT_MODEL=gpt-3.5-turbo
PLANNER_MODEL=gpt-3.5-turbo
MATCHER_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
```

**High-Performance Configuration:**
```env
GENERAL_ASSISTANT_MODEL=gpt-4-turbo
TEAM_ASSISTANT_MODEL=gpt-4-turbo
PLANNER_MODEL=gpt-4-turbo
MATCHER_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-3-large
```

### Vector Database Setup

**Local Storage (Default):**
```env
VECTOR_DB_TYPE=faiss
VECTOR_DB_PATH=./vector_db
```

**Persistent Storage:**
```env
VECTOR_DB_TYPE=chroma
VECTOR_DB_PATH=./chroma_db
```

## 🧪 Testing Your Setup

### 1. Quick Health Check
```bash
cd skillmate/ai
python -c "from main import SkillMateAI; ai = SkillMateAI(); print('✅ Setup successful!')"
```

### 2. Comprehensive Testing
```bash
# Run full test suite (takes 2-3 minutes)
python run_tests.py
```

Expected output:
```
🚀 Starting SkillMate AI System Comprehensive Testing...
============================================================
✅ PASS - General AI Test
✅ PASS - Resume Analysis Test
✅ PASS - Roadmap Generation Test
✅ PASS - Project Planning Test
✅ PASS - Smart Matching Test
✅ PASS - Team Chat AI Test

📊 TEST SUMMARY REPORT
Total Tests: 47
✅ Passed: 43
Success Rate: 91.5%
🎉 System is ready for production!
```

### 3. Interactive Testing
```bash
# Manual testing with menu
python manual_test_guide.py
```

### 4. Individual Feature Testing

**Test General AI:**
```python
from main import SkillMateAI
ai = SkillMateAI()
response = ai.general_ai_response("user123", "What is machine learning?")
print(response)
```

**Test Resume Analysis:**
```python
# Upload a resume file
result = ai.upload_and_query_resume("user123", "path/to/resume.pdf")
# Query the resume
answer = ai.upload_and_query_resume("user123", "What are the main skills?")
print(answer)
```

## 🚨 Troubleshooting

### Common Issues:

**1. Python 3.13 Build Errors ("Cannot import setuptools.build_meta")**
✅ **FIXED!** We now have Python 3.13 specific requirements.
```bash
# Use the automated installer (detects Python 3.13 automatically):
cd skillmate/ai
python install.py

# Or manually for Python 3.13:
pip install -r ../requirements-python313.txt

# See PYTHON313_SETUP.md for detailed Python 3.13 guide
```

**2. "No matching distribution found" or similar version errors**
✅ **FIXED!** We now provide multiple requirement files for different Python versions.
```bash
# Use the automated installer (tries appropriate versions):
cd skillmate/ai
python install.py

# Or manually choose based on your Python version:
pip install -r ../requirements-stable.txt  # Python 3.11/3.12
pip install -r ../requirements-python313.txt  # Python 3.13
```

**2. "OPENAI_API_KEY not set" Warning**
```bash
# Make sure your .env file is in the correct location
ls skillmate/ai/.env

# Check if the key is loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY', 'NOT SET'))"
```

**3. "Rate limit exceeded" Error**
- You're hitting OpenAI's rate limits
- Wait a few minutes between tests
- Consider upgrading your OpenAI plan

**4. "Module not found" Errors**
```bash
# Reinstall dependencies with correct versions
cd skillmate/ai
python install.py
# OR manually:
pip install -r ../requirements.txt --force-reinstall
```

**5. Permission Errors**
```bash
# Create directories manually
mkdir -p skillmate/ai/vector_db
mkdir -p skillmate/ai/resume_storage
```

### Performance Tips:

**1. Speed up testing:**
```env
# Use faster models for testing
GENERAL_ASSISTANT_MODEL=gpt-3.5-turbo
TEAM_ASSISTANT_MODEL=gpt-3.5-turbo
```

**2. Reduce costs:**
```env
# Use smaller embedding model
EMBEDDING_MODEL=text-embedding-3-small
# Reduce memory limits
MEMORY_TOKEN_LIMIT=2000
```

## 🎯 Production Deployment

### Environment Variables for Production:
```env
# Production-ready configuration
OPENAI_API_KEY=your_production_api_key
GENERAL_ASSISTANT_MODEL=gpt-4
TEAM_ASSISTANT_MODEL=gpt-4
PLANNER_MODEL=gpt-4
MATCHER_MODEL=gpt-3.5-turbo
VECTOR_DB_TYPE=chroma
VECTOR_DB_PATH=/app/data/vector_db
RESUME_STORAGE_PATH=/app/data/resumes
```

### Pre-deployment Checklist:
- [ ] All tests passing (>90% success rate)
- [ ] Production API keys configured
- [ ] Persistent storage configured
- [ ] Error handling tested
- [ ] Performance benchmarks met
- [ ] Memory limits appropriate

## 🔗 Integration with Flask Backend

Your backend team can integrate using:
```python
from ai.main import SkillMateAI

# Initialize once
ai_system = SkillMateAI()

# Use in Flask routes
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    user_id = request.json['user_id']
    message = request.json['message']
    response = ai_system.general_ai_response(user_id, message)
    return jsonify({"response": response})
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the test output for specific errors
3. Ensure your OpenAI API key is valid and has credits
4. Verify all dependencies are installed correctly

The system is designed to be robust and provide helpful error messages to guide you through any issues. 