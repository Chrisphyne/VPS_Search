#!/usr/bin/env python3
"""
Interactive Kenya Sugar Board Analysis
Run custom queries on your sugar industry data
"""

import os
from kenya_sugar_adaptive_multiagent import AdaptiveKenyaSugarAnalyzer

def setup_api_keys():
    """Set up API keys for the session"""
    # Set your API keys
    os.environ["GOOGLE_API_KEY"] = "AIzaSyCefrCL_4j6SUdLhuUp94BXso64DS4qK0g"
    os.environ["TAVILY_API_KEY"] = "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"
    print("🔑 API keys configured!")

def run_sample_queries():
    """Run some sample queries to demonstrate capabilities"""
    print("\n🇰🇪 INITIALIZING KENYA SUGAR BOARD ANALYZER...")
    analyzer = AdaptiveKenyaSugarAnalyzer()
    
    sample_queries = [
        {
            "title": "🏭 Factory Efficiency Analysis",
            "query": "Which 3 factories have the highest production efficiency? Calculate efficiency as production per hectare and identify what makes them successful.",
            "type": "data"
        },
        {
            "title": "🗺️ Regional Performance Comparison", 
            "query": "Compare all 8 regions by total production, average sucrose content, and yield per hectare. Which region should Kenya prioritize for investment?",
            "type": "data"
        },
        {
            "title": "📈 Seasonal Production Patterns",
            "query": "Analyze weekly production trends. Which weeks show peak production and what seasonal factors might influence this?",
            "type": "data"
        },
        {
            "title": "🌍 Global Competitiveness Assessment",
            "query": "How do Kenya's sugar factories compare to global industry standards? What specific improvements would make Kenya more competitive?",
            "type": "research"
        },
        {
            "title": "🎯 Strategic Investment Recommendations",
            "query": "Based on both local data and global trends, which 3 strategic investments would provide the highest ROI for Kenya's sugar industry?",
            "type": "comprehensive"
        }
    ]
    
    print(f"\n📋 RUNNING {len(sample_queries)} SAMPLE ANALYSES...")
    
    for i, sample in enumerate(sample_queries, 1):
        print(f"\n{'='*80}")
        print(f"📊 ANALYSIS {i}: {sample['title']}")
        print(f"{'='*80}")
        print(f"🔍 Query: {sample['query']}")
        print(f"📋 Type: {sample['type']}")
        print("-" * 80)
        
        try:
            if sample['type'] == 'data':
                result = analyzer.quick_data_analysis(sample['query'])
            elif sample['type'] == 'research':
                result = analyzer.quick_research(sample['query'])
            else:  # comprehensive
                result = analyzer.analyze(sample['query'])
            
            print("✅ ANALYSIS COMPLETE!")
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ Error in analysis: {e}")
            continue

def interactive_mode():
    """Run interactive query mode"""
    print("\n🎯 INTERACTIVE MODE")
    print("="*50)
    
    setup_api_keys()
    analyzer = AdaptiveKenyaSugarAnalyzer()
    
    print("\n💡 You can ask questions like:")
    sample_questions = [
        "Which factory has the best sucrose quality?",
        "How does Kakamega region perform compared to others?", 
        "What are global best practices for sugar production?",
        "Which weeks show the highest production volumes?",
        "How can Kenya improve its sugar competitiveness?"
    ]
    
    for i, q in enumerate(sample_questions, 1):
        print(f"   {i}. {q}")
    
    print("\n" + "="*50)
    
    while True:
        print("\n🔍 Enter your question (or 'quit' to exit):")
        query = input(">>> ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Thank you for using Kenya Sugar Board Analyzer!")
            break
            
        if not query:
            continue
            
        print(f"\n🤖 Analyzing: {query}")
        print("-" * 60)
        
        try:
            # Determine query type based on keywords
            if any(word in query.lower() for word in ['global', 'world', 'international', 'benchmark', 'compare', 'industry standards']):
                print("🌐 Using Research Agent + Data Analysis...")
                result = analyzer.analyze(query)
            elif any(word in query.lower() for word in ['factory', 'region', 'production', 'week', 'sucrose', 'yield']):
                print("📊 Using Data Analysis Agent...")
                result = analyzer.quick_data_analysis(query)
            else:
                print("🎯 Using Comprehensive Multi-Agent Analysis...")
                result = analyzer.analyze(query)
                
            print("✅ Analysis complete!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try rephrasing your question or ask something else.")

def main():
    """Main function"""
    print("🇰🇪 KENYA SUGAR BOARD INTERACTIVE ANALYZER")
    print("="*60)
    print("Your data: 795 records, 15 factories, 8 regions")
    print("Capabilities: Data analysis + Global research + Strategic insights")
    print("="*60)
    
    print("\nChoose mode:")
    print("1. 📋 Run sample analyses (automated demo)")
    print("2. 🎯 Interactive mode (ask custom questions)")
    print("3. 🚪 Exit")
    
    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            setup_api_keys()
            run_sample_queries()
            break
        elif choice == '2':
            interactive_mode()
            break
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()