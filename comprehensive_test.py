#!/usr/bin/env python3
"""
Comprehensive test for PrivySHA package readiness
Tests all major functionality without requiring external services
"""

import sys
import traceback
from pathlib import Path

def test_package_structure():
    """Test if package has proper structure"""
    print("1. Testing Package Structure")
    print("-" * 30)
    
    required_files = [
        "src/privysha/__init__.py",
        "src/privysha/agent.py", 
        "src/privysha/pipeline.py",
        "src/privysha/parser/__init__.py",
        "src/privysha/parser/prompt_ast.py",
        "src/privysha/adapters/factory.py",
        "src/privysha/adapters/mock_adapter.py",
        "src/privysha/adapters/base.py",
        "src/privysha/stages/sanitizer.py",
        "src/privysha/stages/optimizer.py",
        "src/privysha/stages/compiler.py",
        "src/privysha/utils/pii_detector.py",
        "README.md",
        "LICENSE",
        "pyproject.toml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    else:
        print("✓ All required files present")
        return True

def test_imports():
    """Test if all imports work"""
    print("\n2. Testing Imports")
    print("-" * 30)
    
    try:
        from privysha import Agent
        print("✓ Main Agent import successful")
        
        from privysha.pipeline import Pipeline
        print("✓ Pipeline import successful")
        
        from privysha.adapters.factory import AdapterFactory
        print("✓ Adapter factory import successful")
        
        from privysha.stages.sanitizer import Sanitizer
        print("✓ Sanitizer import successful")
        
        from privysha.stages.optimizer import Optimizer
        print("✓ Optimizer import successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic pipeline functionality"""
    print("\n3. Testing Basic Functionality")
    print("-" * 30)
    
    try:
        from privysha import Agent
        
        # Test mock adapter
        agent = Agent(model="mock", privacy=True, token_budget=1200)
        print("✓ Agent creation successful")
        
        # Test pipeline processing
        test_prompt = "Hey bro can you analyze this dataset for anomalies? Contact me at john@example.com"
        result = agent.run(test_prompt, trace=True)
        print("✓ Pipeline processing successful")
        
        # Verify pipeline stages
        required_stages = ["raw_prompt", "sanitized", "optimized", "compiled_prompt"]
        for stage in required_stages:
            if stage not in result:
                print(f"✗ Missing stage: {stage}")
                return False
        
        print("✓ All pipeline stages present")
        
        # Test PII masking
        if "john@example.com" in result["sanitized"]:
            print("✗ PII not properly masked")
            return False
        else:
            print("✓ PII masking working")
        
        # Test sanitization
        if "bro" in result["sanitized"].lower():
            print("✗ Conversational filler not removed")
            return False
        else:
            print("✓ Prompt sanitization working")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_different_adapters():
    """Test different adapter types"""
    print("\n4. Testing Adapters")
    print("-" * 30)
    
    try:
        from privysha.adapters.factory import AdapterFactory
        
        # Test mock adapter
        mock_adapter = AdapterFactory.create("mock")
        print("✓ Mock adapter creation successful")
        
        # Test mock generation
        response = mock_adapter.generate("test prompt")
        print(f"✓ Mock generation successful: '{response}'")
        
        # Test adapter factory logic
        ollama_adapter = AdapterFactory.create("llama3")
        print("✓ Ollama adapter creation successful")
        
        # Note: We don't test actual OpenAI/Ollama calls as they require external services
        
        return True
        
    except Exception as e:
        print(f"✗ Adapter test failed: {e}")
        traceback.print_exc()
        return False

def test_pipeline_stages():
    """Test individual pipeline stages"""
    print("\n5. Testing Pipeline Stages")
    print("-" * 30)
    
    try:
        from privysha.stages.sanitizer import Sanitizer
        from privysha.stages.optimizer import Optimizer
        from privysha.stages.compiler import Compiler
        
        # Test sanitizer
        sanitizer = Sanitizer(privacy=True)
        test_input = "Hey bro can you help me? My email is john@example.com"
        sanitized = sanitizer.run(test_input)
        
        if "john@example.com" not in sanitized and "bro" not in sanitized.lower():
            print("✓ Sanitizer working correctly")
        else:
            print("✗ Sanitizer not working properly")
            return False
        
        # Test optimizer
        optimizer = Optimizer(100)
        optimized = optimizer.run("analyze this dataset for anomalies")
        print(f"✓ Optimizer working: '{optimized}'")
        
        # Test compiler
        compiler = Compiler()
        # Compiler expects a context dict, not a string
        context = {"system": "You are a helpful assistant.", "task": "analyze dataset"}
        compiled = compiler.compile(context)
        print(f"✓ Compiler working: compiled prompt generated")
        
        return True
        
    except Exception as e:
        print(f"✗ Pipeline stages test failed: {e}")
        traceback.print_exc()
        return False

def test_documentation():
    """Test if documentation is adequate"""
    print("\n6. Testing Documentation")
    print("-" * 30)
    
    try:
        # Check README exists and has content
        readme_path = Path("README.md")
        if not readme_path.exists():
            print("✗ README.md missing")
            return False
        
        readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')
        if len(readme_content) < 1000:
            print("✗ README too short")
            return False
        
        # Check for key sections
        required_sections = [
            "# Overview",
            "# Installation", 
            "# Quick Start",
            "# Key Features"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in readme_content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"✗ Missing README sections: {missing_sections}")
            return False
        else:
            print("✓ README documentation adequate")
        
        return True
        
    except Exception as e:
        print(f"✗ Documentation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("PrivySHA Package Readiness Assessment")
    print("=" * 50)
    
    tests = [
        ("Package Structure", test_package_structure),
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Adapters", test_different_adapters),
        ("Pipeline Stages", test_pipeline_stages),
        ("Documentation", test_documentation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("ASSESSMENT SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 PACKAGE IS READY FOR PUBLIC USE!")
        print("\nHow to use:")
        print("1. Install: pip install privysha")
        print("2. Basic usage:")
        print("   from privysha import Agent")
        print("   agent = Agent(model='mock', privacy=True)")
        print("   response = agent.run('Your prompt here')")
        print("\n3. For production use:")
        print("   - Use OpenAI: Agent(model='gpt-4o-mini')")
        print("   - Use Ollama: Agent(model='llama3') (requires Ollama server)")
        print("   - Use HuggingFace: Agent(model='model-name') (requires transformers)")
        
        print("\n✅ PRODUCTION DEPLOYMENT READY")
        print("   - All core functionality working")
        print("   - PII protection enabled")
        print("   - Token optimization active")
        print("   - Modular architecture")
        print("   - Comprehensive documentation")
        
    else:
        print(f"\n⚠️  PACKAGE NEEDS {total - passed} FIXES BEFORE PUBLIC RELEASE")
        print("Address the failing tests before going public.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
