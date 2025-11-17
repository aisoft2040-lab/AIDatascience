# Getting Started with AI Engineering

Welcome! This guide will help you set up your environment and start your journey as an AI Engineer.

## 🎯 What You'll Learn

By the end of this guide, you'll:
- Understand what an AI Engineer does
- Have your development environment set up
- Make your first LLM API call
- Know the key tools and technologies
- Be ready to start the curriculum

## 👨‍💻 What is an AI Engineer?

An AI Engineer builds production-ready applications that leverage AI models, particularly Large Language Models (LLMs). Unlike ML Engineers who train models, AI Engineers:

- **Integrate** existing models into applications
- **Optimize** for cost, performance, and quality
- **Deploy** AI features to production
- **Monitor** AI systems in real-world use
- **Ensure** safety, privacy, and compliance

Think of it as: **ML Engineer builds the engine, AI Engineer builds the car.**

## 🛠️ Prerequisites

### Required Skills
- **Programming**: Python (intermediate level)
- **APIs**: Understanding of REST APIs
- **Git**: Basic version control
- **Command Line**: Comfortable with terminal

### Helpful (But Not Required)
- Web development basics
- Cloud platforms (AWS, GCP, Azure)
- Docker/containers
- Databases

### If You're Missing Prerequisites
- **New to Python?** Complete [Python for Everybody](https://www.py4e.com/) (2-4 weeks)
- **New to APIs?** Read [Understanding APIs](https://www.freecodecamp.org/news/what-is-an-api-in-english-please-b880a3214a82/) (1 day)
- **New to Git?** Try [Git Handbook](https://guides.github.com/introduction/git-handbook/) (1 day)

## 💻 Environment Setup

### 1. Install Python

You'll need Python 3.9 or later.

**Check your Python version:**
```bash
python --version
# or
python3 --version
```

**Install Python if needed:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python3`
- **Linux**: Usually pre-installed, or `sudo apt install python3`

### 2. Set Up Virtual Environment

Virtual environments keep project dependencies isolated.

```bash
# Create a virtual environment
python -m venv ai-engineer-env

# Activate it
# On Mac/Linux:
source ai-engineer-env/bin/activate

# On Windows:
ai-engineer-env\Scripts\activate

# Your prompt should now show (ai-engineer-env)
```

### 3. Install Essential Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install core packages
pip install openai anthropic python-dotenv jupyter

# Install useful utilities
pip install requests python-dotenv tiktoken tenacity

# For data work
pip install pandas numpy

# For evaluation
pip install pytest pytest-cov
```

### 4. Set Up API Access

You'll need API keys from LLM providers.

#### OpenAI (Recommended for starting)

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up for an account
3. Add payment method (you'll get $5 free credit)
4. Generate API key at [API Keys page](https://platform.openai.com/api-keys)

**Cost estimate**: $1-5 for learning/experimentation

#### Anthropic (Alternative/Additional)

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up for account
3. Add payment method
4. Generate API key

**Cost estimate**: $1-5 for learning/experimentation

### 5. Configure Environment Variables

Create a `.env` file to store API keys securely.

```bash
# In your project directory
touch .env
```

Edit `.env`:
```bash
# OpenAI
OPENAI_API_KEY=sk-...your-key-here...

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-...your-key-here...

# Other settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Important**: Never commit `.env` to version control!

Add to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

### 6. Verify Setup

Create `test_setup.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Test API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in environment")
    exit(1)

print("✅ API key loaded successfully")

# Test API connection
try:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello, AI Engineer!'"}],
        max_tokens=10
    )
    print(f"✅ API connection successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API connection failed: {e}")
```

Run it:
```bash
python test_setup.py
```

Expected output:
```
✅ API key loaded successfully
✅ API connection successful!
Response: Hello, AI Engineer!
```

## 🚀 Your First LLM Application

Let's build a simple chatbot to get started.

Create `first_chatbot.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI()

def chat(user_message, model="gpt-3.5-turbo"):
    """Send a message to the LLM and get response"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        # Extract the response
        assistant_message = response.choices[0].message.content
        
        # Print usage stats
        usage = response.usage
        print(f"\n📊 Usage: {usage.total_tokens} tokens")
        print(f"   Input: {usage.prompt_tokens}, Output: {usage.completion_tokens}")
        
        return assistant_message
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main loop
def main():
    print("🤖 Simple Chatbot (type 'quit' to exit)\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        response = chat(user_input)
        if response:
            print(f"\nAssistant: {response}\n")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python first_chatbot.py
```

Try asking:
- "What is AI Engineering?"
- "Explain prompt engineering"
- "What are the key skills for an AI Engineer?"

## 📚 Essential Tools

### IDEs & Editors
- **VS Code** (Recommended): Free, great Python support
- **PyCharm**: Professional Python IDE
- **Jupyter**: For interactive notebooks

### Version Control
- **Git**: Essential for tracking changes
- **GitHub**: Host your portfolio projects

### API Testing
- **Postman**: Test API calls visually
- **curl**: Command-line API testing

### LLM-Specific Tools
- **LangChain**: Framework for LLM apps
- **LlamaIndex**: Data framework for LLMs
- **Tiktoken**: Token counting for OpenAI models

## 🎓 Key Concepts

Before diving deeper, understand these concepts:

### Tokens
- LLMs process text as "tokens" (roughly 4 characters)
- Pricing is per token
- Context window limits measured in tokens
- Example: "Hello, World!" ≈ 4 tokens

### Prompts
- The input text you send to an LLM
- Critical for getting good results
- Can include instructions, examples, and context

### Temperature
- Controls randomness (0.0 to 2.0)
- Lower (0.0-0.3): More focused, deterministic
- Higher (0.7-1.0): More creative, varied

### Context Window
- Maximum tokens the model can process at once
- Includes both input (prompt) and output
- GPT-3.5: 4K or 16K tokens
- GPT-4: 8K or 128K tokens

## 🗺️ Learning Roadmap

Now that you're set up, here's your path forward:

### Week 1: Foundations
- [Module 1: LLM Fundamentals](README.md#module-1-llm-fundamentals)
- Build a few simple chatbots
- Experiment with different prompts

### Week 2-3: Core Skills
- [Module 2: Prompt Engineering](README.md#module-2-prompt-engineering)
- [Module 3: Evaluation & Testing](README.md#module-3-evaluation--testing)
- Start tracking costs and quality

### Week 4+: Production Skills
- Follow the full [curriculum](README.md)
- Build [portfolio projects](README.md#portfolio-projects)
- Join the community

## 🤝 Getting Help

### When You're Stuck
1. **Read error messages carefully** - They usually tell you what's wrong
2. **Check the documentation** - OpenAI, Anthropic docs are excellent
3. **Search existing issues** - Someone likely had the same problem
4. **Ask in community forums** - See [resources](../resources/community.md)

### Common Issues

**Issue**: `ImportError: No module named 'openai'`
**Solution**: Install the package: `pip install openai`

**Issue**: `AuthenticationError: Invalid API key`
**Solution**: Check your `.env` file and that it's loaded correctly

**Issue**: `RateLimitError: Too many requests`
**Solution**: You're hitting API rate limits. Wait a moment and try again.

**Issue**: High costs
**Solution**: Use `max_tokens` parameter to limit output length

## ✅ Ready Checklist

Before proceeding, make sure you have:

- [ ] Python 3.9+ installed
- [ ] Virtual environment set up
- [ ] Essential packages installed
- [ ] API key(s) obtained and configured
- [ ] Successfully run test_setup.py
- [ ] Built and tested first_chatbot.py
- [ ] Understand basic concepts (tokens, prompts, temperature)
- [ ] Joined community (optional but recommended)

## 🎯 Next Steps

You're ready! Choose your path:

1. **Structured Learning**: Start [Module 1](README.md#module-1-llm-fundamentals)
2. **Project-Based**: Jump to [Portfolio Week 1](../../portfolio/weeks/week-01/README.md)
3. **Topic-Specific**: Browse [Tutorials](../tutorials/README.md)

## 🔗 Quick Reference

- [Full Curriculum](README.md)
- [Tutorial Index](../tutorials/README.md)
- [Resource Library](../resources/README.md)
- [Portfolio Projects](../../portfolio/weeks/README.md)

---

**Congratulations!** 🎉 You're now set up and ready to become an AI Engineer. The journey ahead is exciting - let's build the future of AI applications together!
