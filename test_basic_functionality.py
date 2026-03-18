#!/usr/bin/env python3
"""
Basic functionality test for PrivySHA package
Tests the core pipeline without requiring external LLM services
"""

from src.privysha import Agent

def test_basic_pipeline():
    """Test the basic pipeline functionality with mock adapter"""
    print("Testing PrivySHA Basic Functionality")
    print("=" * 50)
    
    # Test with mock adapter (should work without external services)
    agent = Agent(
        model="mock",
        privacy=True,
        token_budget=1200
    )
    
    # Test prompt
    test_prompt = "Hey bro can you analyze this dataset for anomalies? My email is john@example.com"
    
    print(f"Input prompt: {test_prompt}")
    print()
    
    try:
        # This should fail due to missing mock adapter
        result = agent.run(test_prompt, trace=True)
        print("SUCCESS: Pipeline processed without errors")
        print()
        
        # Display the pipeline trace
        for stage, output in result.items():
            if stage != "response":
                print(f"{stage.upper()}:")
                print(f"  {output}")
                print()
                
    except Exception as e:
        print(f"ERROR: {e}")
        print()
        print("This indicates the package needs a mock adapter for testing")
        
def test_import():
    """Test that the package can be imported"""
    try:
        from privysha import Agent
        print("✓ Package imports successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("PrivySHA Package Readiness Test")
    print("=" * 50)
    
    # Test import
    import_success = test_import()
    print()
    
    if import_success:
        test_basic_pipeline()
    else:
        print("Package cannot be imported - not ready for public use")
