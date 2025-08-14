# Kenya Sugar Board Analysis System - Next.js UI

A modern, responsive web interface for the Kenya Sugar Board Analysis System built with Next.js, TypeScript, and Tailwind CSS.

## 🌟 Features

- **🎨 Modern UI/UX** - Clean, responsive design with Tailwind CSS
- **💬 Real-time Chat Interface** - Interactive conversation with AI assistant
- **🧠 Conversation Memory** - Maintains context across multiple queries
- **🔧 Server Configuration** - Easy setup for remote server connections
- **📱 Mobile Responsive** - Works on desktop, tablet, and mobile devices
- **⚡ Fast Performance** - Built with Next.js 14 and React 18
- **🎯 Kenya Sugar Focused** - Specialized for sugar industry analysis

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Running Kenya Sugar Analysis API server

### Installation

```bash
# Navigate to the UI directory
cd kenya-sugar-nextjs-ui

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:7550`

## 🔧 Configuration

### Server Connection

1. **Local Development**: The app defaults to `http://localhost:7560`
2. **Remote Server**: Click "Settings" and enter your server IP and port
3. **Environment Variables**: Update `.env.local` for persistent configuration

### Environment Variables

```bash
# .env.local
API_BASE_URL=http://your-server-ip:7560
```

## 📱 Usage

### 1. Connect to Server
- Click the "Settings" button in the header
- Enter your server IP address and port (default: 7560)
- Click "Test Connection" to verify connectivity

### 2. Start Analyzing
- Use sample queries from the sidebar
- Or type your own questions about Kenya's sugar sector
- The AI will provide comprehensive, research-based responses

### 3. Conversation Memory
- The system remembers your conversation context
- Follow-up questions will reference previous discussions
- Clear conversation history using the trash icon

## 🎯 Sample Queries

The interface includes ready-to-use sample queries:

- "What are the key financial challenges facing Kenya's sugar sector?"
- "Compare production efficiency across different factories"
- "What are the main production challenges in the sugar industry?"
- "Which regions have the highest sugar production?"
- "Analyze seasonal patterns in sugar production"
- "Provide recommendations for improving factory efficiency"

## 🏗️ Project Structure

```
kenya-sugar-nextjs-ui/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Main page component
├── public/                  # Static assets
├── .env.local              # Environment variables
├── next.config.js          # Next.js configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── package.json            # Dependencies and scripts
└── README.md               # This file
```

## 🎨 Styling

- **Framework**: Tailwind CSS for utility-first styling
- **Icons**: Lucide React for modern, consistent icons
- **Typography**: Inter font for clean, readable text
- **Theme**: Custom Kenya-inspired color palette

## 📦 Scripts

```bash
# Development
npm run dev          # Start development server

# Production
npm run build        # Build for production
npm start           # Start production server

# Maintenance
npm run lint        # Run ESLint
```

## 🌐 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker

```bash
# Build Docker image
docker build -t kenya-sugar-ui .

# Run container
docker run -p 7550:7550 -e API_BASE_URL=http://your-server:7560 kenya-sugar-ui
```

### Manual Deployment

```bash
# Build for production
npm run build

# Copy build files to your web server
cp -r .next/static/* /var/www/html/
```

## 🔧 API Integration

The UI connects to the Kenya Sugar Analysis API with these endpoints:

- `GET /health` - Server health check
- `POST /analyze` - Submit analysis queries
- `GET /conversations/{id}/history` - Retrieve conversation history
- `POST /conversations/{id}/clear` - Clear conversation

## 📱 Mobile Support

The interface is fully responsive and optimized for:
- 📱 Mobile phones (320px+)
- 📟 Tablets (768px+)  
- 💻 Laptops (1024px+)
- 🖥️ Desktop (1280px+)

## 🛠️ Development

### Adding New Features

1. **Components**: Add reusable components in `components/`
2. **Pages**: Create new pages in `app/`
3. **Styles**: Use Tailwind classes or extend in `globals.css`
4. **API**: Update API calls in page components

### Code Style

- **TypeScript**: Strongly typed components and functions
- **ESLint**: Consistent code formatting
- **Tailwind**: Utility-first CSS approach

## 🚀 Performance

- **Next.js 14**: Latest features and optimizations
- **Static Generation**: Fast loading times
- **Tree Shaking**: Minimal bundle size
- **Image Optimization**: Automatic image compression

## 🎯 Next Steps

1. **Start the API server**: `python3 simple_working_api.py`
2. **Launch the UI**: `npm run dev`
3. **Configure connection**: Enter your server details
4. **Start analyzing**: Ask questions about Kenya's sugar sector!

## 🆘 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify API server is running on specified port
   - Check firewall settings allow port 7560
   - Ensure server binds to `0.0.0.0` for remote access

2. **Build Errors**
   - Run `npm install` to ensure all dependencies are installed
   - Check Node.js version (18+ required)

3. **CORS Issues**
   - API server already includes CORS headers
   - For custom domains, update server CORS configuration

### Support

For issues specific to the Kenya Sugar Analysis System, check:
- API server logs for connection issues
- Browser console for JavaScript errors
- Network tab for failed API requests

## 🎉 Ready to Analyze!

Your professional Next.js interface for Kenya Sugar Board analysis is ready! 

Features:
- ✅ Modern, responsive design
- ✅ Real-time AI conversations  
- ✅ Conversation memory
- ✅ Professional UI/UX
- ✅ Easy server configuration
- ✅ Mobile-friendly

Start exploring Kenya's sugar industry with AI-powered insights! 🇰🇪📊