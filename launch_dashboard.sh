#!/bin/bash

# 🇰🇪 Kenya Sugar Board Dashboard Launcher
echo "🇰🇪 KENYA SUGAR BOARD DASHBOARD LAUNCHER"
echo "========================================="

# Set API keys
export GOOGLE_API_KEY="AIzaSyCefrCL_4j6SUdLhuUp94BXso64DS4qK0g"
export TAVILY_API_KEY="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"

echo "🔑 API keys configured"

# Function to start Python backend
start_python_backend() {
    echo "🐍 Starting Python Multi-Agent Backend..."
    source rag_env/bin/activate
    python kenya_sugar_adaptive_multiagent.py &
    PYTHON_PID=$!
    echo "✅ Python backend started (PID: $PYTHON_PID)"
}

# Function to start Next.js frontend
start_nextjs_frontend() {
    echo "⚛️ Starting Next.js Dashboard..."
    cd kenya-sugar-dashboard
    npm run dev &
    NEXTJS_PID=$!
    echo "✅ Next.js dashboard started (PID: $NEXTJS_PID)"
    cd ..
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    
    if [[ ! -z "$PYTHON_PID" ]]; then
        kill $PYTHON_PID 2>/dev/null
        echo "✅ Python backend stopped"
    fi
    
    if [[ ! -z "$NEXTJS_PID" ]]; then
        kill $NEXTJS_PID 2>/dev/null
        echo "✅ Next.js dashboard stopped"
    fi
    
    echo "👋 Services stopped successfully"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Check if virtual environment exists
if [ ! -d "rag_env" ]; then
    echo "❌ Virtual environment 'rag_env' not found"
    echo "💡 Please set up the Python environment first"
    exit 1
fi

# Check if Next.js project exists
if [ ! -d "kenya-sugar-dashboard" ]; then
    echo "❌ Next.js dashboard directory not found"
    echo "💡 Please ensure the dashboard is properly set up"
    exit 1
fi

# Start services
start_python_backend
sleep 3  # Give Python backend time to start

start_nextjs_frontend
sleep 5  # Give Next.js time to start

echo ""
echo "🎉 SERVICES RUNNING:"
echo "📊 Dashboard UI: http://localhost:3000"
echo "🤖 Python Backend: Running with multi-agent system"
echo ""
echo "💡 Features available:"
echo "   - Interactive dashboard with Kenya Sugar Board data"
echo "   - AI assistant powered by Google Gemini & Tavily"
echo "   - Real-time data visualization and analytics"
echo "   - Multi-agent analysis (Data, Research, Strategic)"
echo ""
echo "🚀 Ready to analyze Kenya's sugar industry!"
echo "📱 Open http://localhost:3000 in your browser"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep script running until interrupted
wait