#!/bin/bash

# Run UXAgent with Bruvi.com website
# Make sure you have your API keys set:
# export OPENAI_API_KEY=sk-your-key-here
# OR
# export AWS_ACCESS_KEY_ID=your-access-key
# export AWS_SECRET_ACCESS_KEY=your-secret-key

# Set visual mode (optional)
export HEADLESS=false

echo "🎯 Running UXAgent with Bruvi.com..."
echo "👩‍💼 Persona: Jessica (Tech Product Manager from Seattle)"
echo "🎯 Goal: Buy a Bruvi coffee machine with subscription bundle"
echo ""

cd src && /Users/gabefish/Projects/UXAgent/simulated_web_agent_env/bin/python -m simulated_web_agent.main \
  --persona "../example_data/personas/json/bruvi_coffee_shopper.json" \
  --output "../output" \
  --website bruvi \
  --llm-provider openai

echo ""
echo "✅ Bruvi simulation completed!"
echo "📁 Check the output folder for results" 