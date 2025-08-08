#!/usr/bin/env python3
"""
Setup script for Kenya Sugar Board Multi-Agent System
"""

import os
import sys

def setup_api_keys():
    """Interactive setup for API keys"""
    print("🔑 API KEY CONFIGURATION")
    print("=" * 40)
    
    # Google API Key
    current_google = os.environ.get('GOOGLE_API_KEY')
    if current_google:
        print(f"✅ Google API Key already configured (length: {len(current_google)})")
        change = input("Do you want to change it? (y/n): ").lower().strip()
        if change != 'y':
            print("✅ Keeping existing Google API key")
        else:
            google_key = input("Enter your Google API key: ").strip()
            if google_key:
                os.environ['GOOGLE_API_KEY'] = google_key
                print("✅ Google API key updated")
    else:
        print("⚠️ Google API key not configured")
        google_key = input("Enter your Google API key (required): ").strip()
        if google_key:
            os.environ['GOOGLE_API_KEY'] = google_key
            print("✅ Google API key configured")
            
            # Write to shell profile
            shell_cmd = f'export GOOGLE_API_KEY="{google_key}"'
            print(f"\n💡 To make this permanent, add this to your shell profile:")
            print(f"   {shell_cmd}")
        else:
            print("❌ Google API key is required for the system to work")
    
    # Tavily API Key (optional)
    current_tavily = os.environ.get('TAVILY_API_KEY')
    if current_tavily:
        print(f"✅ Tavily API Key already configured (length: {len(current_tavily)})")
    else:
        print("\n⚠️ Tavily API key not configured (optional)")
        print("Tavily provides web search capabilities. Without it, the system will use mock search.")
        tavily_key = input("Enter your Tavily API key (optional, press Enter to skip): ").strip()
        if tavily_key:
            os.environ['TAVILY_API_KEY'] = tavily_key
            print("✅ Tavily API key configured")
            
            shell_cmd = f'export TAVILY_API_KEY="{tavily_key}"'
            print(f"💡 To make this permanent, add this to your shell profile:")
            print(f"   {shell_cmd}")
        else:
            print("⚠️ Skipping Tavily API key - will use mock search")

def test_system():
    """Test the system after setup"""
    print("\n🧪 TESTING SYSTEM")
    print("=" * 40)
    
    try:
        from kenya_sugar_multiagent import KenyaSugarDataAnalyzer
        
        print("✅ Importing system...")
        analyzer = KenyaSugarDataAnalyzer()
        print("✅ System initialized successfully!")
        
        # Test with a simple query
        print("\n🧪 Running test query...")
        test_query = "Show me a summary of the top 3 factories by yield in 2025"
        
        result = analyzer.quick_data_analysis(test_query)
        print("✅ Test query completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🇰🇪 KENYA SUGAR BOARD MULTI-AGENT SYSTEM SETUP")
    print("=" * 60)
    
    print("\n🎯 This script will help you configure the multi-agent system.")
    print("You'll need:")
    print("1. Google API key (for Gemini LLM) - Required")
    print("2. Tavily API key (for web search) - Optional")
    
    # API Key setup
    setup_api_keys()
    
    # Test system
    print("\n" + "=" * 60)
    success = test_system()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE")
    print("=" * 60)
    
    if success:
        print("✅ System is ready to use!")
        print("\n🚀 To get started:")
        print("1. Run: python kenya_sugar_multiagent.py")
        print("2. Or try: python test_simple.py")
        
        print("\n💡 Example usage:")
        print("```python")
        print("from kenya_sugar_multiagent import KenyaSugarDataAnalyzer")
        print("analyzer = KenyaSugarDataAnalyzer()")
        print("analyzer.analyze('Which factories performed best in 2025?')")
        print("```")
    else:
        print("⚠️ System setup encountered issues.")
        print("\n🔧 Troubleshooting:")
        print("1. Run: python test_simple.py")
        print("2. Check your API keys")
        print("3. Ensure all dependencies are installed")
        
    print("\n📚 For more help, check the README or run test_simple.py")

if __name__ == "__main__":
    main()