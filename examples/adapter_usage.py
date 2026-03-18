#!/usr/bin/env python3
"""
Examples of using PrivySHA with different adapters and models.

This demonstrates how users can use THEIR OWN models with the library.
"""

from privysha import Agent

def example_user_models():
    """
    Examples showing how users can use their own models.
    The library is now flexible and doesn't hardcode model names.
    """
    
    print("PrivySHA Adapter Usage Examples")
    print("=" * 50)
    
    # Example 1: User wants to use their specific OpenAI model
    print("\n1. OpenAI Models (User's Choice):")
    openai_models = [
        "gpt-4",
        "gpt-4-turbo", 
        "gpt-3.5-turbo",
        "gpt-4o-mini",
        "custom-gpt-model"  # User's own fine-tuned model
    ]
    
    for model in openai_models:
        try:
            # Note: Will fail without OPENAI_API_KEY, but shows flexibility
            agent = Agent(model=model, privacy=True)
            print(f"✅ {model}: OpenAI adapter created")
        except Exception as e:
            print(f"⚠️  {model}: {str(e)[:50]}...")
    
    # Example 2: User wants to use their specific Claude model
    print("\n2. Claude Models (User's Choice):")
    claude_models = [
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229", 
        "claude-3-haiku-20240307",
        "claude-2.1",
        "custom-claude-model"  # User's own fine-tuned model
    ]
    
    for model in claude_models:
        try:
            # Note: Will fail without ANTHROPIC_API_KEY, but shows flexibility
            agent = Agent(model=model, privacy=True)
            print(f"✅ {model}: Claude adapter created")
        except Exception as e:
            print(f"⚠️  {model}: {str(e)[:50]}...")
    
    # Example 3: User wants to use ANY HuggingFace model
    print("\n3. HuggingFace Models (Complete Freedom):")
    hf_models = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "microsoft/DialoGPT-large",
        "facebook/opt-1.3b", 
        "google/flan-t5-large",
        "EleutherAI/gpt-neo-2.7B",
        "user/custom-model",  # User's own trained model
        "my-org/my-finetuned-model"  # User's organization model
    ]
    
    for model in hf_models:
        try:
            # Note: Will fail without transformers installed, but shows flexibility
            agent = Agent(model=model, privacy=True)
            print(f"✅ {model}: HuggingFace adapter created")
        except Exception as e:
            print(f"⚠️  {model}: {str(e)[:50]}...")
    
    # Example 4: User wants to use local Ollama models
    print("\n4. Ollama Models (Local Models):")
    ollama_models = [
        "llama2",
        "codellama",
        "mistral",
        "vicuna",
        "user-custom-model"  # User's custom Ollama model
    ]
    
    for model in ollama_models:
        try:
            # Note: Will fail without Ollama server, but shows flexibility
            agent = Agent(model=model, privacy=True)
            print(f"✅ {model}: Ollama adapter created")
        except Exception as e:
            print(f"⚠️  {model}: {str(e)[:50]}...")
    
    # Example 5: Always works - Mock for testing
    print("\n5. Mock Adapter (Always Works):")
    try:
        agent = Agent(model="mock", privacy=True)
        response = agent.run("Test prompt")
        print(f"✅ mock: {response}")
    except Exception as e:
        print(f"❌ mock: {e}")

def example_real_usage():
    """
    Example of how a real user would use the library
    """
    print("\n\nReal Usage Examples:")
    print("=" * 30)
    
    # User has their OpenAI API key and wants to use GPT-4
    print("\n# User with OpenAI:")
    print("import os")
    print("os.environ['OPENAI_API_KEY'] = 'your-api-key'")
    print("agent = Agent(model='gpt-4', privacy=True)")
    print("response = agent.run('Your prompt here')")
    
    # User has their own HuggingFace model
    print("\n# User with custom HuggingFace model:")
    print("agent = Agent(model='my-org/my-custom-model', privacy=True)")
    print("response = agent.run('Your prompt here')")
    
    # User has Claude API
    print("\n# User with Claude:")
    print("os.environ['ANTHROPIC_API_KEY'] = 'your-api-key'")
    print("agent = Agent(model='claude-3-sonnet-20240229', privacy=True)")
    print("response = agent.run('Your prompt here')")

if __name__ == "__main__":
    example_user_models()
    example_real_usage()
