#!/usr/bin/env python3
"""
Test script for new adapters (HuggingFace and Claude)
"""

from privysha import Agent

def test_adapters():
    print("Testing New Adapters")
    print("=" * 40)
    
    # Test HuggingFace adapter
    print("\n1. Testing HuggingFace Adapter:")
    try:
        agent = Agent(model="mistralai/Mistral-7B-Instruct-v0.2", privacy=True)
        response = agent.run("Hello, how are you?")
        print(f"✅ HF Response: {response[:100]}...")
    except Exception as e:
        print(f"⚠️  HF Adapter Error: {e}")
    
    # Test Claude adapter (will fail without API key)
    print("\n2. Testing Claude Adapter:")
    try:
        agent = Agent(model="claude-3-sonnet-20240229", privacy=True)
        response = agent.run("Hello, how are you?")
        print(f"✅ Claude Response: {response[:100]}...")
    except Exception as e:
        print(f"⚠️  Claude Adapter Error: {e}")
    
    # Test model name detection
    print("\n3. Testing Model Detection:")
    test_models = [
        "mock",
        "gpt-4", 
        "claude-3-opus-20240229",
        "mistralai/Mistral-7B-Instruct-v0.2",
        "llama",
        "unknown-model"
    ]
    
    for model in test_models:
        try:
            agent = Agent(model=model, privacy=True)
            print(f"✅ {model}: Adapter created successfully")
        except Exception as e:
            print(f"⚠️  {model}: {e}")

if __name__ == "__main__":
    test_adapters()
