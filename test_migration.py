#!/usr/bin/env python3
"""
Test script to verify PrivySHA v1 → v2 migration compatibility.

This script tests that existing v1 code continues to work while
v2 features are available under the same API.
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_v1_compatibility():
    """Test that v1 code still works."""
    print("Testing v1 compatibility...")
    
    try:
        from privysha import Agent
        
        # Test basic v1 usage with mock
        agent = Agent(model="mock", privacy=True, token_budget=1200)
        print("✅ Agent creation works")
        
        # Test basic run
        response = agent.run("Test prompt with email@example.com")
        print("✅ Basic run works")
        print(f"Response: {response}")
        
        # Test trace
        result = agent.run("Test prompt", trace=True)
        print("✅ Trace mode works")
        print(f"Trace keys: {list(result.keys())}")
        
        # Test token metrics
        metrics = agent.get_token_metrics("Test prompt")
        print("✅ Token metrics work")
        print(f"Token metrics: {metrics}")
        
        return True
        
    except Exception as e:
        print(f"❌ v1 compatibility test failed: {e}")
        return False

def test_v2_features():
    """Test that v2 features are available."""
    print("\nTesting v2 features...")
    
    try:
        from privysha import Agent, PromptIR, SecurityLayer, ModelRouter
        
        # Test v2 Agent with fallbacks (using mock to avoid API key issues)
        agent = Agent(
            model="mock",
            fallback_providers=[
                {"provider": "mock", "model": "mock"}
            ]
        )
        print("✅ v2 Agent with fallbacks works")
        
        # Test advanced components
        print("✅ Advanced components importable:")
        print(f"  - PromptIR: {PromptIR}")
        print(f"  - SecurityLayer: {SecurityLayer}")
        print(f"  - ModelRouter: {ModelRouter}")
        
        # Test v2 methods
        metrics = agent.get_token_metrics("Test prompt")
        print("✅ Token metrics available")
        
        # Test creation methods
        simple_agent = Agent.create_simple("mock")
        print("✅ create_simple works")
        
        advanced_agent = Agent.create_advanced("mock")
        print("✅ create_advanced works")
        
        return True
        
    except Exception as e:
        print(f"❌ v2 features test failed: {e}")
        return False

def test_pipeline_compatibility():
    """Test pipeline compatibility."""
    print("\nTesting pipeline compatibility...")
    
    try:
        from privysha import Pipeline
        
        pipeline = Pipeline(privacy=True, token_budget=1200)
        print("✅ Pipeline creation works")
        
        result = pipeline.process("Test prompt")
        print("✅ Pipeline processing works")
        print(f"Pipeline result keys: {list(result.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline compatibility test failed: {e}")
        return False

def test_adapter_factory():
    """Test adapter factory enhancements."""
    print("\nTesting adapter factory...")
    
    try:
        from privysha import AdapterFactory
        
        # Test v1 method
        adapter = AdapterFactory.create("mock")
        print("✅ Legacy factory method works")
        
        # Test v2 methods (use mock to avoid API key issues)
        universal = AdapterFactory.create_universal("mock", "mock")
        print("✅ Universal adapter creation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Adapter factory test failed: {e}")
        return False

def main():
    """Run all migration tests."""
    print("🔄 PrivySHA v1 → v2 Migration Test")
    print("=" * 50)
    
    tests = [
        test_v1_compatibility,
        test_v2_features,
        test_pipeline_compatibility,
        test_adapter_factory
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Migration successful!")
        return True
    else:
        print("❌ Some tests failed. Migration needs fixes.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
