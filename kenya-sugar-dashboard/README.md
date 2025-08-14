# 🇰🇪 Kenya Sugar Board Dashboard

A modern Next.js web interface for the Kenya Sugar Board Multi-Agent AI Analysis System.

## Features

### 📊 **Dashboard Overview**
- Real-time industry statistics and KPIs
- Interactive charts and visualizations
- Factory performance rankings
- Regional comparison analytics

### 🤖 **AI Assistant Chat**
- Powered by Google Gemini & Tavily Research
- Multi-agent analysis capabilities:
  - 📊 **Data Agent**: Local CSV data analysis
  - 🌐 **Research Agent**: Global industry insights
  - 🎯 **Supervisor Agent**: Strategic recommendations

### 📈 **Analytics & Visualizations**
- Production trends and seasonal patterns
- Sucrose content quality analysis
- Regional performance comparisons
- Efficiency benchmarking

### 🎯 **Smart Query System**
- Natural language queries
- Contextual response types (Data, Research, Comprehensive)
- Suggested questions and quick actions

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Your Python backend running (see main project)

### Installation

1. **Navigate to the dashboard directory:**
```bash
cd kenya-sugar-dashboard
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
# Create .env.local file
echo "PYTHON_BACKEND_URL=http://localhost:8000" > .env.local
```

4. **Start the development server:**
```bash
npm run dev
```

5. **Open your browser:**
Navigate to [http://localhost:3000](http://localhost:3000)

## Dashboard Sections

### 🏠 **Overview Tab**
- Industry statistics cards
- Production charts
- Top performing factories
- Regional distribution

### 🏭 **Factory Analytics Tab**
- Detailed factory performance metrics
- Sucrose content quality trends
- Monthly production patterns
- Efficiency rankings

### 🗺️ **Regional Analysis Tab**
- Geographic performance mapping
- Regional comparison charts
- Investment priority recommendations

### 🤖 **AI Assistant Tab**
- Interactive chat interface
- Natural language queries
- Multi-agent responses
- Data-driven insights

### 🌍 **Global Insights Tab**
- International benchmarking
- Global best practices
- Competitive analysis
- Industry trends

## Sample Queries

Try asking the AI assistant:

### 📊 **Data Analysis Queries:**
- "Which factory has the highest production efficiency?"
- "Compare Kakamega region to other regions"
- "What are the seasonal production patterns?"
- "Show me the top 5 factories by sucrose content"

### 🌐 **Research Queries:**
- "How does Kenya compare to global sugar standards?"
- "What are international best practices for sugar production?"
- "What technologies could improve our productivity?"

### 🎯 **Strategic Queries:**
- "What are the top 3 investment priorities for Kenya's sugar industry?"
- "How can we reduce import dependency?"
- "Which regions should receive development focus?"

## Technology Stack

- **Frontend**: Next.js 14, React, TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Backend Integration**: REST API routes
- **AI Backend**: Python multi-agent system

## Data Source

The dashboard displays insights from:
- **795 production records** across **15 factories** in **8 regions**
- Real Kenya Sugar Board data including:
  - Production quantities and values
  - Sucrose content percentages
  - Crop yields and areas
  - Weekly and seasonal patterns

## API Integration

The dashboard connects to your Python backend through:
- `/api/chat` - AI assistant interactions
- Environment variable: `PYTHON_BACKEND_URL`

### Connecting to Python Backend

To connect to your actual Python multi-agent system:

1. **Ensure your Python backend is running:**
```bash
# In the main project directory
source rag_env/bin/activate
python kenya_sugar_adaptive_multiagent.py
```

2. **Update the API route** in `src/app/api/chat/route.ts`:
```typescript
// Uncomment these lines for production:
const response = await fetch(`${pythonBackendUrl}/analyze`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: message, type: queryType })
})
```

## Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Environment Variables
```bash
PYTHON_BACKEND_URL=http://your-backend-url:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Features Breakdown

### 🎨 **Modern UI/UX**
- Responsive design for all devices
- Kenya-themed color scheme (green/orange)
- Smooth animations and transitions
- Professional dashboard layout

### 📊 **Data Visualization**
- Interactive bar charts for production data
- Line charts for quality trends
- Pie charts for regional distribution
- Real-time statistics cards

### 🤖 **AI Integration**
- Context-aware responses
- Multiple agent types (Data, Research, Strategic)
- Suggested queries for easy interaction
- Real-time typing indicators

### 🔧 **Developer Experience**
- TypeScript for type safety
- Component-based architecture
- Clean API structure
- Comprehensive error handling

## Contributing

This dashboard is part of the larger Kenya Sugar Board Multi-Agent Analysis System. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For questions about the dashboard or integration with the Python backend, please refer to the main project documentation or create an issue.

---

**Built with ❤️ for Kenya's Sugar Industry** 🇰🇪

*Empowering data-driven decisions through AI-powered analytics*
