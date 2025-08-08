#!/usr/bin/env python3
"""
Simple test for Kenya Sugar Board Multi-Agent System
"""

import os
import sys

def test_imports():
    """Test if all required imports work"""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        from langchain.chat_models import init_chat_model
        print("✅ langchain.chat_models imported")
    except ImportError as e:
        print(f"❌ langchain.chat_models import failed: {e}")
        return False
    
    try:
        from langchain_experimental.tools import PythonAstREPLTool
        print("✅ langchain_experimental imported")
    except ImportError as e:
        print(f"❌ langchain_experimental import failed: {e}")
        return False
    
    try:
        from langgraph.prebuilt import create_react_agent
        print("✅ langgraph imported")
    except ImportError as e:
        print(f"❌ langgraph import failed: {e}")
        return False
    
    print("✅ All basic imports successful!")
    return True

def test_data_loading():
    """Test if data files can be loaded"""
    print("\n📊 Testing data loading...")
    
    try:
        import pandas as pd
        
        # Check if files exist
        if not os.path.exists('ksb_data_1.csv'):
            print("❌ ksb_data_1.csv not found")
            return False
        
        if not os.path.exists('ksb_data_2.csv'):
            print("❌ ksb_data_2.csv not found")
            return False
        
        # Try loading
        df1 = pd.read_csv('ksb_data_1.csv')
        df2 = pd.read_csv('ksb_data_2.csv')
        
        print(f"✅ Dataset 1 loaded: {df1.shape[0]} records, {df1.shape[1]} columns")
        print(f"✅ Dataset 2 loaded: {df2.shape[0]} records, {df2.shape[1]} columns")
        
        # Test merge
        combined = pd.merge(df1, df2, on=['Factory', 'Region', 'Year'], how='inner')
        print(f"✅ Combined dataset: {combined.shape[0]} records, {combined.shape[1]} columns")
        
        return True
        
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_api_keys():
    """Test if API keys are configured"""
    print("\n🔑 Testing API keys...")
    
    google_key = os.environ.get('GOOGLE_API_KEY')
    if google_key:
        print(f"✅ GOOGLE_API_KEY configured (length: {len(google_key)})")
    else:
        print("⚠️ GOOGLE_API_KEY not configured")
    
    tavily_key = os.environ.get('TAVILY_API_KEY')
    if tavily_key:
        print(f"✅ TAVILY_API_KEY configured (length: {len(tavily_key)})")
    else:
        print("⚠️ TAVILY_API_KEY not configured (optional)")
    
    return google_key is not None

def test_system():
    """Test the actual multi-agent system"""
    print("\n🤖 Testing multi-agent system...")
    
    try:
        # Set a dummy API key if none exists (for testing imports)
        if not os.environ.get('GOOGLE_API_KEY'):
            os.environ['GOOGLE_API_KEY'] = 'dummy-key-for-testing'
            print("⚠️ Using dummy API key for import testing only")
        
        from kenya_sugar_multiagent import KenyaSugarDataAnalyzer
        print("✅ KenyaSugarDataAnalyzer imported successfully")
        
        # Try to initialize (this might fail without proper API keys)
        try:
            analyzer = KenyaSugarDataAnalyzer()
            print("✅ KenyaSugarDataAnalyzer initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️ KenyaSugarDataAnalyzer initialization failed (expected with dummy API key): {e}")
            print("💡 This is normal if using dummy API keys")
            return False
            
    except ImportError as e:
        print(f"❌ System import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🇰🇪 KENYA SUGAR BOARD MULTI-AGENT SYSTEM - DIAGNOSTICS")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test data loading
    results.append(test_data_loading())
    
    # Test API keys
    results.append(test_api_keys())
    
    # Test system
    results.append(test_system())
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System should work correctly.")
    elif passed >= 3:
        print("✅ Most tests passed. System should work with proper API keys.")
    else:
        print("⚠️ Several tests failed. Please check the setup.")
    
    print("\n💡 Next steps:")
    if not results[0]:
        print("1. Install missing dependencies: pip install langchain langchain-community langchain-experimental langgraph")
    if not results[1]:
        print("2. Ensure CSV data files are in the current directory")
    if not results[2]:
        print("3. Set your Google API key: export GOOGLE_API_KEY='your-api-key'")
    if passed >= 3:
        print("4. Run the system: python kenya_sugar_multiagent.py")

if __name__ == "__main__":
    main()