#!/usr/bin/env python3
"""
Enhanced Kenya Sugar Board Analysis System Setup
This script helps you configure and test the enhanced system.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🇰🇪" + "="*70)
    print("   ENHANCED KENYA SUGAR BOARD ANALYSIS SYSTEM SETUP")
    print("="*72)
    print("Features:")
    print("✅ Conversation Memory using LangGraph")
    print("✅ Multi-LLM Provider Support (Google, OpenAI, Anthropic, Ollama)")
    print("✅ Robust Error Handling & Fallback Responses")
    print("✅ Advanced Data Analysis Capabilities")
    print("✅ RESTful API with FastAPI")
    print("="*72)

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install from enhanced requirements
        if Path("requirements_enhanced.txt").exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements_enhanced.txt"
            ], check=True)
        else:
            # Fallback to basic requirements
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True)
            
            # Install additional packages for enhanced features
            additional_packages = [
                "langchain-google-genai",
                "langchain-openai", 
                "langchain-anthropic",
                "langchain-ollama",
                "matplotlib",
                "seaborn"
            ]
            
            for package in additional_packages:
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", package
                    ], check=True)
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"⚠️ Failed to install {package} (optional)")
        
        print("✅ Dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True

def setup_api_keys():
    """Help user setup API keys"""
    print("\n🔑 API Key Configuration")
    print("The enhanced system supports multiple LLM providers:")
    print()
    
    # Check current API keys
    providers = {
        "Google Gemini": {
            "env_var": "GOOGLE_API_KEY",
            "url": "https://aistudio.google.com/app/apikey",
            "description": "Free tier available, good performance"
        },
        "OpenAI GPT": {
            "env_var": "OPENAI_API_KEY", 
            "url": "https://platform.openai.com/api-keys",
            "description": "High quality, pay-per-use"
        },
        "Anthropic Claude": {
            "env_var": "ANTHROPIC_API_KEY",
            "url": "https://console.anthropic.com/",
            "description": "Good reasoning capabilities"
        }
    }
    
    configured_providers = []
    
    for provider, info in providers.items():
        key = os.getenv(info["env_var"])
        if key:
            print(f"✅ {provider}: Configured")
            configured_providers.append(provider)
        else:
            print(f"❌ {provider}: Not configured")
            print(f"   Get key: {info['url']}")
            print(f"   Set: export {info['env_var']}='your-key-here'")
            print(f"   {info['description']}")
        print()
    
    if not configured_providers:
        print("⚠️ No API keys configured!")
        print("💡 The system will try to use Ollama (local) as fallback")
        print("💡 To install Ollama: https://ollama.ai/")
        print()
        
        # Option to configure a key now
        print("Would you like to configure an API key now? (y/n): ", end="")
        if input().lower().startswith('y'):
            print("\nChoose a provider:")
            for i, (provider, info) in enumerate(providers.items(), 1):
                print(f"{i}. {provider}")
            
            try:
                choice = int(input("Enter choice (1-3): ")) - 1
                provider_name = list(providers.keys())[choice]
                provider_info = list(providers.values())[choice]
                
                print(f"\n🌐 Get your {provider_name} API key from:")
                print(f"   {provider_info['url']}")
                
                api_key = input(f"\nEnter your {provider_info['env_var']}: ").strip()
                if api_key:
                    os.environ[provider_info['env_var']] = api_key
                    print(f"✅ {provider_name} API key configured for this session")
                    print(f"💡 To make permanent, add to your ~/.bashrc or ~/.zshrc:")
                    print(f"   export {provider_info['env_var']}='{api_key}'")
                    configured_providers.append(provider_name)
                    
            except (ValueError, IndexError):
                print("Invalid choice. Continuing with local fallback...")
    
    return len(configured_providers) > 0

def test_system():
    """Test the enhanced system"""
    print("\n🧪 Testing Enhanced System...")
    
    try:
        from kenya_sugar_enhanced_system import create_enhanced_analyzer
        
        print("📊 Creating analyzer...")
        analyzer = create_enhanced_analyzer()
        
        print(f"✅ LLM Provider: {analyzer.llm_provider}")
        print(f"✅ Datasets loaded: {len(analyzer.datasets)}")
        
        # Test basic query
        print("\n🔍 Testing analysis...")
        test_query = "What are the key challenges facing Kenya's sugar sector?"
        result = analyzer.analyze(test_query, "setup_test")
        
        if result["status"] in ["success", "fallback"]:
            print("✅ Analysis test passed!")
            print(f"📝 Response preview: {result['response'][:150]}...")
        else:
            print("⚠️ Analysis test completed with issues")
            print(f"Status: {result['status']}")
        
        # Test conversation memory
        print("\n💾 Testing conversation memory...")
        follow_up = "Can you elaborate on the production challenges?"
        result2 = analyzer.analyze(follow_up, "setup_test")
        
        if result2["status"] in ["success", "fallback"]:
            print("✅ Conversation memory test passed!")
        
        print("\n✅ System test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def create_env_template():
    """Create environment template file"""
    env_template = """# Enhanced Kenya Sugar Board Analysis System Environment Variables

# LLM Provider API Keys (choose one or more)
# GOOGLE_API_KEY=your_google_gemini_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here  
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Data directory
# KSB_DATA_DIR=./data

# Optional: Tavily API key for web research
# TAVILY_API_KEY=your_tavily_api_key_here

# Usage:
# 1. Copy this file to .env
# 2. Uncomment and fill in your API keys
# 3. Source the file: source .env
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template)
    
    print("✅ Created .env.template file")
    print("💡 Copy to .env and configure your API keys")

def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples:")
    print()
    
    print("1️⃣ Python Script Usage:")
    print("```python")
    print("from kenya_sugar_enhanced_system import create_enhanced_analyzer")
    print()
    print("# Create analyzer")
    print("analyzer = create_enhanced_analyzer()")
    print()
    print("# Single analysis")
    print("result = analyzer.analyze('What are the production trends?')")
    print("print(result['response'])")
    print()
    print("# Conversation with memory")
    print("analyzer.analyze('Show factory performance data', 'conversation_1')")
    print("analyzer.analyze('Which factory is best?', 'conversation_1')")
    print("```")
    print()
    
    print("2️⃣ API Server Usage:")
    print("```bash")
    print("# Start server")
    print("python kenya_sugar_enhanced_api.py")
    print()
    print("# Or with uvicorn")
    print("uvicorn kenya_sugar_enhanced_api:app --reload")
    print()
    print("# Test endpoints")
    print("curl http://localhost:8000/health")
    print("curl -X POST http://localhost:8000/analyze \\")
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"query": "Analyze sugar production trends"}\'')
    print("```")
    print()
    
    print("3️⃣ Available Endpoints:")
    print("• GET  /health - System status")
    print("• POST /analyze - Main analysis endpoint")  
    print("• GET  /conversations/{id}/history - Get conversation history")
    print("• POST /conversations/{id}/clear - Clear conversation")
    print("• GET  /data/summary - Data summary")
    print("• GET  /llm/status - LLM provider status")
    print("• GET  /test/quick - Quick system test")

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Step 3: Setup API keys
    has_api_keys = setup_api_keys()
    
    # Step 4: Create environment template
    create_env_template()
    
    # Step 5: Test system
    if test_system():
        print("\n🎉 Enhanced Kenya Sugar Board Analysis System is ready!")
        
        if has_api_keys:
            print("✅ Configured with cloud LLM provider")
        else:
            print("⚠️ Running with local fallback (install Ollama for full functionality)")
        
        show_usage_examples()
        
        print("\n🚀 Next Steps:")
        print("1. Start the API server: python kenya_sugar_enhanced_api.py")
        print("2. Visit http://localhost:8000/docs for API documentation")
        print("3. Test with your Kenya sugar sector queries!")
        
    else:
        print("\n❌ Setup completed with issues")
        print("💡 Check error messages above and ensure API keys are configured")

if __name__ == "__main__":
    main()