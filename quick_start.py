#!/usr/bin/env python3
"""
Quick Start - Kenya Sugar Board Analysis
Get instant insights from your sugar industry data
"""

import os
from kenya_sugar_adaptive_multiagent import AdaptiveKenyaSugarAnalyzer

# Set up your API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyCefrCL_4j6SUdLhuUp94BXso64DS4qK0g"
os.environ["TAVILY_API_KEY"] = "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"

def main():
    print("🇰🇪 KENYA SUGAR BOARD QUICK ANALYSIS")
    print("="*50)
    
    # Initialize the analyzer
    print("🔄 Initializing analyzer...")
    analyzer = AdaptiveKenyaSugarAnalyzer()
    
    # Quick efficiency analysis
    print("\n📊 FACTORY EFFICIENCY ANALYSIS:")
    print("-" * 30)
    efficiency_result = analyzer.quick_data_analysis(
        "Rank all factories by production efficiency (production per hectare). "
        "Show the top 5 most efficient and bottom 3 least efficient factories with their key metrics."
    )
    
    # Regional comparison 
    print("\n🗺️ REGIONAL PERFORMANCE COMPARISON:")
    print("-" * 35)
    regional_result = analyzer.quick_data_analysis(
        "Compare all 8 regions by total production, average sucrose content, and yield per hectare. "
        "Rank them from best to worst overall performance."
    )
    
    # Global competitiveness
    print("\n🌍 GLOBAL COMPETITIVENESS ASSESSMENT:")
    print("-" * 40)
    global_result = analyzer.analyze(
        "How do Kenya's sugar production metrics compare to global standards? "
        "What are the 3 most critical areas for improvement to compete internationally?"
    )
    
    print("\n✅ QUICK ANALYSIS COMPLETE!")
    print("🎯 For custom queries, run: python kenya_sugar_interactive.py")

if __name__ == "__main__":
    main()