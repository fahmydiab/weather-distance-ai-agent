# Weather and Distance from Giza Agent

This is an AI agent built with Strands MCP that can:
1. Get the current weather for any city
2. Calculate the distance between a city and Giza, Egypt (location of the Great Pyramids)

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Install Ollama and download the Llama 3.2 model:
   ```
   # Install Ollama from https://ollama.com/
   # Start the Ollama server
   ollama serve
   
   # In another terminal, pull the Llama 3.2 model
   ollama pull llama3.2:latest
   ```

3. Run the agent:
   ```
   python weather_distance_agent.py
   ```

## Usage

Once the agent is running, you can ask questions like:
- "What's the weather in Tokyo?"
- "How far is New York from Giza?"
- "Tell me the weather in Paris and how far it is from the pyramids"

Type 'exit' to quit the application.

## How It Works

The agent uses:
- Strands Agents SDK for the AI agent framework
- Llama 3.2 model running locally through Ollama for natural language understanding
- wttr.in API for weather data (no API key required)
- Pre-defined coordinates for major cities to calculate distances from Giza

### Fallback Mode

If Ollama is not running or the Llama 3.2 model is not available, the agent will automatically fall back to a rule-based mode that doesn't require an AI model. This ensures the agent can always provide weather and distance information.

### Distance Calculation

The agent can calculate distances for these major cities:
New York, London, Paris, Tokyo, Sydney, Cairo, Beijing, Moscow, Dubai, Los Angeles, Chicago, Toronto, Mexico City, Sao Paulo, Mumbai, Singapore, Berlin, Rome, Madrid, Amsterdam, Bangkok, Seoul, Johannesburg, Istanbul, Rio de Janeiro, San Francisco, Barcelona, Vienna, Athens, and more.

## Requirements

- Python 3.8+
- Ollama installed with Llama 3.2 model (optional, for AI-powered responses)
- Internet connection for weather data
