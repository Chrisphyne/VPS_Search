#!/bin/bash

# Kenya Sugar Board Analysis System - Web UI Launcher
# This script opens the web interface for the analysis system

echo "🇰🇪 Kenya Sugar Board Analysis System - Web UI Launcher"
echo "=" * 60

# Check if web_ui.html exists
if [ ! -f "web_ui.html" ]; then
    echo "❌ web_ui.html not found in current directory"
    echo "💡 Make sure you're in the correct directory with the web_ui.html file"
    exit 1
fi

# Check if API server is running
echo "🔍 Checking if API server is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API server is running on port 8000"
else
    echo "⚠️ API server not detected on port 8000"
    echo "🚀 Starting API server..."
    
    # Try to start the simple working API
    if [ -f "simple_working_api.py" ]; then
        echo "📡 Starting simple_working_api.py..."
        python3 simple_working_api.py &
        API_PID=$!
        echo "🆔 API server started with PID: $API_PID"
        
        # Wait for server to start
        echo "⏳ Waiting for server to initialize..."
        sleep 3
        
        # Check if it started successfully
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ API server started successfully!"
        else
            echo "❌ Failed to start API server"
            echo "💡 Try running manually: python3 simple_working_api.py"
            exit 1
        fi
    else
        echo "❌ simple_working_api.py not found"
        echo "💡 Please ensure the API server file exists"
        exit 1
    fi
fi

# Get the absolute path to web_ui.html
WEB_UI_PATH=$(realpath web_ui.html)
echo "📁 Web UI file: $WEB_UI_PATH"

# Detect the operating system and open accordingly
echo "🌐 Opening web interface..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open > /dev/null; then
        xdg-open "file://$WEB_UI_PATH"
        echo "✅ Opened with xdg-open (Linux)"
    elif command -v firefox > /dev/null; then
        firefox "file://$WEB_UI_PATH" &
        echo "✅ Opened with Firefox"
    elif command -v google-chrome > /dev/null; then
        google-chrome "file://$WEB_UI_PATH" &
        echo "✅ Opened with Chrome"
    elif command -v chromium-browser > /dev/null; then
        chromium-browser "file://$WEB_UI_PATH" &
        echo "✅ Opened with Chromium"
    else
        echo "⚠️ No browser found. Please open manually:"
        echo "   file://$WEB_UI_PATH"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "file://$WEB_UI_PATH"
    echo "✅ Opened with default browser (macOS)"
    
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    start "file://$WEB_UI_PATH"
    echo "✅ Opened with default browser (Windows)"
    
else
    # Unknown OS
    echo "⚠️ Unknown operating system. Please open manually:"
    echo "   file://$WEB_UI_PATH"
fi

echo ""
echo "🎯 SYSTEM READY!"
echo "=" * 60
echo "📊 Web Interface: file://$WEB_UI_PATH"
echo "🌐 API Server: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs (if FastAPI is running)"
echo "💬 Health Check: http://localhost:8000/health"
echo ""
echo "🧪 Test Commands:"
echo "# Health check"
echo "curl http://localhost:8000/health"
echo ""
echo "# Sample analysis query"
echo "curl -X POST http://localhost:8000/analyze \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"query\": \"What are the financial challenges in Kenya sugar sector?\", \"conversation_id\": \"user_001\"}'"
echo ""
echo "⏹️ To stop the API server:"
echo "pkill -f simple_working_api"
echo ""
echo "🎉 Your Kenya Sugar Board Analysis System is ready!"
echo "   - Conversation Memory ✅"
echo "   - Web Research Enhanced ✅" 
echo "   - Expert Industry Analysis ✅"