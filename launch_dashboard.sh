#!/bin/bash

# 🇰🇪 Kenya Sugar Board Dashboard Launcher
echo "🇰🇪 KENYA SUGAR BOARD DASHBOARD LAUNCHER"
echo "========================================="

# Set API keys (consider moving to .env in production)
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-AIzaSyCefrCL_4j6SUdLhuUp94BXso64DS4qK0g}"
export TAVILY_API_KEY="${TAVILY_API_KEY:-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}"

# Configure backend URL for Next.js
export PYTHON_BACKEND_URL="${PYTHON_BACKEND_URL:-http://127.0.0.1:7400}"

echo "🔑 API keys configured"
echo "🔌 PYTHON_BACKEND_URL=${PYTHON_BACKEND_URL}"

# Function to start Python backend
start_python_backend() {
    echo "🐍 Starting Python Multi-Agent Backend (FastAPI)..."
    if [ -d "rag_env" ]; then
        source rag_env/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    # Install deps if missing (best-effort)
    python -m pip install -r requirements.txt >/dev/null 2>&1 || true
    uvicorn kenya_sugar_api:app --host 127.0.0.1 --port 7400 --workers 1 &
    PYTHON_PID=$!
    echo "✅ Python backend started (PID: $PYTHON_PID)"
}

# Function to start Next.js frontend
start_nextjs_frontend() {
    echo "⚛️ Starting Next.js Dashboard..."
    cd kenya-sugar-dashboard || exit 1
    # Ensure deps
    npm ci --no-audit --no-fund >/dev/null 2>&1 || npm install --no-audit --no-fund >/dev/null 2>&1
    # Export backend URL to Next env for server runtime
    export PYTHON_BACKEND_URL
    npm run dev -- -p 7500 -H 0.0.0.0 &
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
echo "📊 Dashboard UI: http://localhost:7500"
echo "🤖 Python Backend: ${PYTHON_BACKEND_URL}"
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