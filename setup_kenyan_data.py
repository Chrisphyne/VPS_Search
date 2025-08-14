#!/usr/bin/env python3
"""
Setup script for Kenyan Sugar Board CSV files
This script helps you prepare and test the adaptive multi-agent system
"""

import os
import pandas as pd
from pathlib import Path

def find_kenyan_csv_files():
    """Find Kenyan sugar CSV files in the repository"""
    print("🔍 Searching for Kenyan Sugar CSV files...")
    
    search_locations = [
        ".",
        "./RAG", 
        "./data",
        "./RAG/data",
        "../data"
    ]
    
    target_files = [
        "kenyan_sugar_weekly_factory.csv",
        "kenyan_sugar_weekly_factory_agg.csv"
    ]
    
    found_files = {}
    
    for location in search_locations:
        if not os.path.exists(location):
            continue
            
        print(f"  📂 Checking: {location}")
        
        for target_file in target_files:
            file_path = os.path.join(location, target_file)
            if os.path.exists(file_path):
                found_files[target_file] = file_path
                print(f"  ✅ Found: {file_path}")
    
    return found_files

def inspect_csv_structure(file_path):
    """Inspect the structure of a CSV file"""
    try:
        df = pd.read_csv(file_path)
        print(f"\n📊 Structure of {os.path.basename(file_path)}:")
        print(f"   📏 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   📋 Columns: {', '.join(df.columns.tolist())}")
        
        # Show data types
        print(f"   🔢 Data types:")
        for col, dtype in df.dtypes.items():
            print(f"      {col}: {dtype}")
        
        # Show sample data
        print(f"   📝 Sample data:")
        print(df.head().to_string(index=False))
        
        # Show unique values for key columns
        for col in ['Factory', 'Region', 'Year', 'Week']:
            if col in df.columns:
                unique_vals = df[col].unique()
                if len(unique_vals) <= 20:
                    print(f"   🏷️ {col}: {', '.join(map(str, unique_vals))}")
                else:
                    print(f"   🏷️ {col}: {len(unique_vals)} unique values (showing first 10): {', '.join(map(str, unique_vals[:10]))}")
        
        return df
        
    except Exception as e:
        print(f"   ❌ Error reading {file_path}: {e}")
        return None

def test_adaptive_system():
    """Test the adaptive multi-agent system"""
    print("\n🧪 Testing Adaptive Multi-Agent System...")
    
    try:
        from kenya_sugar_adaptive_multiagent import AdaptiveKenyaSugarAnalyzer
        
        # Create analyzer
        analyzer = AdaptiveKenyaSugarAnalyzer()
        
        print("\n📋 Data Summary:")
        print(analyzer.get_data_summary())
        
        # Test quick data analysis
        print("\n🧪 Testing Quick Data Analysis...")
        test_query = "Show me basic statistics for the available datasets"
        
        try:
            result = analyzer.quick_data_analysis(test_query)
            print("✅ Quick data analysis test successful!")
        except Exception as e:
            print(f"⚠️ Quick data analysis test failed: {e}")
        
        return analyzer
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure kenya_sugar_adaptive_multiagent.py is in the current directory")
        return None
    except Exception as e:
        print(f"❌ System error: {e}")
        return None

def create_sample_kenyan_files():
    """Create sample Kenyan sugar CSV files for testing"""
    print("\n📝 Creating sample Kenyan sugar CSV files...")
    
    # Sample weekly factory data
    weekly_data = {
        'Factory': ['Mumias Sugar Company', 'Chemelil Sugar Company', 'South Nyanza Sugar Company', 
                   'West Kenya Sugar Company', 'Nzoia Sugar Company'] * 20,
        'Region': ['Western', 'Nyanza', 'Nyanza', 'Western', 'Western'] * 20,
        'Year': [2023] * 50 + [2024] * 50,
        'Week': list(range(1, 51)) * 2,
        'Cane_Delivered_Tonnes': [8500, 7200, 6800, 5900, 6400] * 20,
        'Sugar_Produced_Tonnes': [950, 810, 765, 660, 720] * 20,
        'Sucrose_Content_Percent': [11.2, 11.8, 11.5, 10.9, 11.3] * 20,
        'Mill_Efficiency_Percent': [85.2, 87.1, 86.4, 82.8, 84.6] * 20
    }
    
    # Sample aggregated factory data  
    agg_data = {
        'Factory': ['Mumias Sugar Company', 'Chemelil Sugar Company', 'South Nyanza Sugar Company',
                   'West Kenya Sugar Company', 'Nzoia Sugar Company'] * 20,
        'Region': ['Western', 'Nyanza', 'Nyanza', 'Western', 'Western'] * 20,
        'Year': [2023] * 50 + [2024] * 50,
        'Week': list(range(1, 51)) * 2,
        'Total_Revenue_KES': [14500000, 12300000, 11600000, 10100000, 10900000] * 20,
        'Operating_Costs_KES': [11200000, 9800000, 9300000, 8400000, 8900000] * 20,
        'Employment_Count': [3200, 2800, 2650, 2200, 2400] * 20,
        'Farmers_Registered': [18500, 16200, 15400, 12800, 14100] * 20
    }
    
    # Create DataFrames
    weekly_df = pd.DataFrame(weekly_data)
    agg_df = pd.DataFrame(agg_data)
    
    # Save to CSV files
    weekly_file = "kenyan_sugar_weekly_factory.csv"
    agg_file = "kenyan_sugar_weekly_factory_agg.csv"
    
    weekly_df.to_csv(weekly_file, index=False)
    agg_df.to_csv(agg_file, index=False)
    
    print(f"✅ Created {weekly_file}: {weekly_df.shape[0]} records")
    print(f"✅ Created {agg_file}: {agg_df.shape[0]} records")
    
    return weekly_file, agg_file

def main():
    """Main setup function"""
    print("🇰🇪 KENYAN SUGAR BOARD DATA SETUP")
    print("=" * 50)
    
    # Step 1: Look for existing CSV files
    found_files = find_kenyan_csv_files()
    
    if found_files:
        print(f"\n✅ Found {len(found_files)} CSV file(s)!")
        
        # Inspect each file
        for filename, filepath in found_files.items():
            df = inspect_csv_structure(filepath)
            
        # Test the system with found files
        print("\n" + "=" * 50)
        analyzer = test_adaptive_system()
        
    else:
        print("\n⚠️ No Kenyan sugar CSV files found.")
        print("💡 Let me create sample files for testing...")
        
        # Create sample files
        sample_files = create_sample_kenyan_files()
        
        print(f"\n📁 Sample files created:")
        for file in sample_files:
            print(f"  - {file}")
        
        # Inspect the sample files
        for file in sample_files:
            inspect_csv_structure(file)
        
        # Test the system with sample files
        print("\n" + "=" * 50)
        analyzer = test_adaptive_system()
    
    # Provide next steps
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    
    print("\n🚀 Next Steps:")
    
    if found_files:
        print("1. ✅ Your CSV files were detected and loaded successfully!")
        print("2. 🧪 Run: python kenya_sugar_adaptive_multiagent.py")
        print("3. 💡 Or try specific analyses:")
    else:
        print("1. 📁 Sample CSV files have been created for testing")
        print("2. 📤 Upload your actual kenyan_sugar_weekly_factory*.csv files")
        print("3. 🧪 Run: python kenya_sugar_adaptive_multiagent.py")
        print("4. 💡 Or try specific analyses:")
    
    print("\n📋 Example Usage:")
    print("""```python
from kenya_sugar_adaptive_multiagent import AdaptiveKenyaSugarAnalyzer

# Initialize system (auto-detects your CSV files)
analyzer = AdaptiveKenyaSugarAnalyzer()

# Quick data analysis
analyzer.quick_data_analysis("Show weekly production trends by factory")

# Comprehensive analysis with research
analyzer.analyze("How do Kenya's sugar factories compare to global standards?")

# Industry research
analyzer.quick_research("Latest trends in sugar industry efficiency")
```""")
    
    print("\n💡 Sample Questions to Try:")
    questions = [
        "Which factories have the highest production efficiency?",
        "Compare regional performance across all metrics",
        "What are the weekly production trends for 2024?",
        "Research global sugar industry benchmarks for Kenya",
        "Analyze profitability patterns by factory size"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

if __name__ == "__main__":
    main()