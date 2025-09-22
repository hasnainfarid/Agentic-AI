# Web-Searching Agentic AI

A powerful ReAct (Reasoning + Acting) agent with beautiful GUI, real-time web search, and intelligent tool usage.

## Features
- 🧠 **ReAct Reasoning** - See AI thinking process step by step
- 🌐 **Web Search** - Real-time information with Tavily
- 🧮 **Calculator** - Math problem solving
- 🌤️ **Weather** - Mock weather information
- 🎨 **Beautiful GUI** - Clean, modern interface
- ⚡ **Fast Performance** - Powered by Groq's Llama 3.3 70B

## Setup

1. Get API Keys:
   - **Groq**: Sign up at [console.groq.com](https://console.groq.com/keys)
   - **Tavily**: Sign up at [tavily.com](https://tavily.com/)

2. Set environment variables:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
export TAVILY_API_KEY="your_tavily_api_key_here"
```

   Or create a `.env` file (copy from `env_example.txt`):
```bash
cp env_example.txt .env
# Edit .env with your API keys
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python web_searching_agentic_ai.py
```

## Usage
- **Math questions**: "What is 2+2*3?"
- **Weather info**: "What's the weather in London?"
- **Web search**: "What's the latest news about AI?"
- **General questions**: "Tell me about Pakistan's economy"

## GUI Features
- **ReAct Steps Tab** - Watch AI reasoning in real-time
- **Conversation Tab** - Clean chat history
- **Color-coded steps** - Easy to follow thinking process
- **Progress indicators** - Visual feedback during processing

## How It Works

This agent uses the ReAct (Reasoning + Acting) framework:
1. **🧠 Thought**: AI reasons about what to do
2. **⚡ Action**: AI selects appropriate tool
3. **👁️ Observation**: AI gets results from tool
4. **✅ Final Answer**: AI provides complete response

## Contributing

Feel free to submit issues and enhancement requests!

## License
MIT © 2025 Hasnain Fareed
