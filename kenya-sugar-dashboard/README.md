# Kenya Sugar Board Dashboard

This Next.js dashboard connects to a Python FastAPI backend that wraps the Adaptive Kenya Sugar Multi-Agent analyzer.

## Development

- Start both services using the root script:

```bash
./launch_dashboard.sh
```

- Or run manually:

```bash
# Terminal 1 (root)
export GOOGLE_API_KEY=your_key
export TAVILY_API_KEY=optional_key
uvicorn kenya_sugar_api:app --host 0.0.0.0 --port 8000

# Terminal 2 (kenya-sugar-dashboard)
export PYTHON_BACKEND_URL=http://localhost:8000
npm install
npm run dev
```

The chat API route reads `PYTHON_BACKEND_URL` to call the Python backend `/analyze` endpoint. If the backend is unavailable, it falls back to a local mock response for a smooth UX.
