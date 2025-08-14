# Test script for Kenya Sugar Board Multi-Agent System
import os
import pandas as pd

def test_system():
    """Test the multi-agent system with sample data"""
    
    print("🇰🇪 KENYA SUGAR BOARD MULTI-AGENT ANALYSIS SYSTEM TEST")
    print("=" * 60)
    
    # Check if data files exist
    if not os.path.exists('ksb_data_1.csv') or not os.path.exists('ksb_data_2.csv'):
        print("📊 CSV data files found!")
        
        # Load and display basic info
        try:
            df1 = pd.read_csv('ksb_data_1.csv')
            df2 = pd.read_csv('ksb_data_2.csv')
            
            print(f"✅ Dataset 1 loaded: {df1.shape[0]} records, {df1.shape[1]} columns")
            print(f"✅ Dataset 2 loaded: {df2.shape[0]} records, {df2.shape[1]} columns")
            
            # Show sample
            print("\n📋 Sample from Dataset 1:")
            print(df1.head())
            
            print("\n📋 Sample from Dataset 2:")
            print(df2.head())
            
            # Combine datasets
            combined = pd.merge(df1, df2, on=['Factory', 'Region', 'Year'], how='inner')
            print(f"\n✅ Combined dataset: {combined.shape[0]} records, {combined.shape[1]} columns")
            
            print("\n🏭 Available Factories:")
            for factory in combined['Factory'].unique():
                print(f"  - {factory}")
                
            print("\n🗺️ Available Regions:")
            for region in combined['Region'].unique():
                print(f"  - {region}")
                
            print(f"\n📅 Years: {', '.join(map(str, sorted(combined['Year'].unique())))}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    else:
        print("⚠️ Data files not found. Please ensure ksb_data_1.csv and ksb_data_2.csv are in current directory.")
        return False

def show_usage():
    """Show usage instructions"""
    print("\n" + "=" * 60)
    print("📖 USAGE INSTRUCTIONS")
    print("=" * 60)
    
    print("\n🔧 **Setup Requirements:**")
    print("1. Install dependencies:")
    print("   pip install langchain langchain-community langchain-experimental")
    print("   pip install langgraph tavily-python pandas")
    
    print("\n2. Set API keys:")
    print("   export GOOGLE_API_KEY='your-google-api-key'")
    print("   export TAVILY_API_KEY='your-tavily-api-key'  # Optional")
    
    print("\n3. Ensure data files are present:")
    print("   - ksb_data_1.csv")
    print("   - ksb_data_2.csv")
    
    print("\n🚀 **Running the System:**")
    print("```python")
    print("from kenya_sugar_multiagent import KenyaSugarDataAnalyzer")
    print("")
    print("# Initialize the system")
    print("analyzer = KenyaSugarDataAnalyzer()")
    print("")
    print("# Comprehensive analysis")
    print("analyzer.analyze('Which factories performed best in 2025?')")
    print("")
    print("# Quick data analysis")
    print("analyzer.quick_data_analysis('Calculate average yields by region')")
    print("")
    print("# Quick research")
    print("analyzer.quick_research('Global sugar industry best practices')")
    print("```")
    
    print("\n💡 **Example Questions:**")
    questions = [
        "Which top 5 factories performed best in 2025 in terms of yield and sucrose content?",
        "Compare regional performance across all metrics",
        "What are the efficiency trends from 2023 to 2025?",
        "Research global sugar industry benchmarks and compare with Kenya",
        "Analyze correlation between processing capacity and revenue generation",
        "Find best practices for sugar mill modernization"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    print("\n✨ **Multi-Agent Architecture Benefits:**")
    print("🔒 **Context Quarantine** - Each agent has isolated context")
    print("📊 **Data Agent** - Specialized pandas analysis")
    print("🌐 **Research Agent** - External industry research")
    print("🎯 **Supervisor** - Intelligent coordination and synthesis")
    print("⚡ **Efficiency** - Parallel processing, reduced token usage")
    print("🎨 **Flexibility** - Easy to add new specialized agents")

if __name__ == "__main__":
    # Test the system
    success = test_system()
    
    # Show usage regardless
    show_usage()
    
    if success:
        print("\n✅ **System Ready!** You can now run the multi-agent analysis.")
    else:
        print("\n⚠️ **Setup Required** - Please follow the setup instructions above.")
        
    print("\n🎉 **Next Steps:**")
    print("1. Configure your API keys")
    print("2. Run: python kenya_sugar_multiagent.py")
    print("3. Or import the KenyaSugarDataAnalyzer class in your notebook")