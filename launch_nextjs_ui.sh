#!/bin/bash

# Kenya Sugar Board Analysis System - Next.js UI Launcher
echo "🇰🇪 Kenya Sugar Board Analysis System - Next.js UI Launcher"
echo "=" * 70

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "💡 Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version $NODE_VERSION is too old"
    echo "💡 Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js $(node --version) detected"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    echo "💡 Please install npm or use yarn"
    exit 1
fi

echo "✅ npm $(npm --version) detected"

# Navigate to UI directory
if [ ! -d "kenya-sugar-nextjs-ui" ]; then
    echo "❌ kenya-sugar-nextjs-ui directory not found"
    echo "💡 Please ensure you're in the correct directory"
    exit 1
fi

cd kenya-sugar-nextjs-ui

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    echo "💡 Please ensure the Next.js project is properly set up"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "💡 Try running: npm install --legacy-peer-deps"
        exit 1
    fi
    
    echo "✅ Dependencies installed successfully"
else
    echo "✅ Dependencies already installed"
fi

# Check if API server is running
echo "🔍 Checking API server..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API server is running on port 8000"
else
    echo "⚠️ API server not detected on port 8000"
    echo "💡 Make sure to start your API server first:"
    echo "   python3 simple_working_api.py"
    echo ""
    echo "🚀 Starting UI anyway - you can configure the server connection in the app"
fi

# Start the development server
echo ""
echo "🚀 Starting Next.js development server..."
echo "🌐 The UI will be available at: http://localhost:3000"
echo "⚡ Hot reloading enabled - changes will update automatically"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start with npm run dev
npm run dev

echo ""
echo "✅ Next.js UI server stopped"