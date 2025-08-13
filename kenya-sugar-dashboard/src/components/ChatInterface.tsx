'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, Factory, Globe, BarChart3 } from 'lucide-react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
  type?: 'data' | 'research' | 'comprehensive'
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I\'m your Kenya Sugar Board AI Assistant. I can help you analyze factory performance, regional comparisons, and provide global industry insights. What would you like to know?',
      sender: 'ai',
      timestamp: new Date(),
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const suggestedQueries = [
    {
      text: "Which factory has the highest production efficiency?",
      icon: Factory,
      type: 'data' as const
    },
    {
      text: "Compare Kakamega region to other regions",
      icon: BarChart3,
      type: 'data' as const
    },
    {
      text: "How does Kenya compare to global sugar standards?",
      icon: Globe,
      type: 'research' as const
    },
    {
      text: "What are the seasonal production patterns?",
      icon: BarChart3,
      type: 'data' as const
    },
    {
      text: "Strategic recommendations for improving competitiveness",
      icon: Globe,
      type: 'comprehensive' as const
    }
  ]

  const handleSendMessage = async (text: string = inputText) => {
    if (!text.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      // Call the API route which connects to Python backend
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          queryType: determineQueryType(text)
        }),
      })

      const data = await response.json()

      if (data.success) {
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response,
          sender: 'ai',
          timestamp: new Date(),
          type: data.queryType
        }

        setMessages(prev => [...prev, aiResponse])
      } else {
        throw new Error(data.error || 'API request failed')
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const determineQueryType = (text: string): 'data' | 'research' | 'comprehensive' => {
    const lowerText = text.toLowerCase()
    if (lowerText.includes('global') || lowerText.includes('international') || lowerText.includes('world')) {
      return 'research'
    } else if (lowerText.includes('recommend') || lowerText.includes('strategy') || lowerText.includes('improve')) {
      return 'comprehensive'
    }
    return 'data'
  }

  const generateMockResponse = (query: string): string => {
    const lowerQuery = query.toLowerCase()
    
    if (lowerQuery.includes('efficiency') || lowerQuery.includes('production')) {
      return `Based on your data analysis:\n\n**Top 3 Most Efficient Factories:**\n1. **Butali** - 351K tonnes, 13.6% sucrose, 79.7 t/ha yield\n2. **West-Kenya** - 339K tonnes, 13.3% sucrose, 79.6 t/ha yield\n3. **Mumias** - 325K tonnes, 13.2% sucrose, 79.5 t/ha yield\n\n**Key Insights:**\n- Kakamega region factories (Butali, West-Kenya, Mumias) dominate efficiency rankings\n- Average sucrose content is 13.4% across top performers\n- These factories achieve 50% higher yields than industry average\n\n**Recommendations:**\n- Study Kakamega region's best practices\n- Implement similar irrigation and cultivation methods in other regions`
    }
    
    if (lowerQuery.includes('region') || lowerQuery.includes('kakamega')) {
      return `**Regional Performance Analysis:**\n\n**Kakamega Region (Leading Performer):**\n- 4 factories: Butali, West-Kenya, Mumias, Sukari\n- Total production: 1.09M tonnes (23% of national output)\n- Average sucrose: 13.3% (above national average)\n- Average yield: 80.1 t/ha (highest in Kenya)\n\n**Comparison with Other Regions:**\n- **National**: 2.34M tonnes (single large factory)\n- **Kisumu**: 489K tonnes across 3 factories\n- **Trans-Nzoia**: 311K tonnes (Nzoia factory)\n\n**Strategic Insight:**\nKakamega's cluster of high-performing factories suggests strong regional infrastructure, climate advantages, and effective farming practices that should be replicated elsewhere.`
    }
    
    if (lowerQuery.includes('global') || lowerQuery.includes('world') || lowerQuery.includes('international')) {
      return `**Global Sugar Industry Comparison:**\n\n**Kenya vs World Standards:**\n- **Productivity**: Kenya avg 60 t/ha vs Global best practice 80-120 t/ha\n- **Sucrose Content**: Kenya 10-16% vs Global optimal 12-14%\n- **Market Position**: Kenya ranks among top 15 global producers\n\n**Global Benchmarks:**\n- **Brazil**: 150+ t/ha (world leader)\n- **Australia**: 100+ t/ha\n- **Zambia**: 113 t/ha (regional competitor)\n- **Malawi**: 105 t/ha\n\n**Competitive Challenges:**\n- Kenyan consumers pay 39% above COMESA average\n- Import dependency: 184K tonnes imported vs 194K produced\n- Need for mill modernization and irrigation investment\n\n**Global Best Practices to Adopt:**\n- Precision agriculture and drip irrigation\n- High-sucrose variety cultivation\n- Bagasse co-generation for energy efficiency`
    }

    return `I understand you're asking about "${query}". Based on your Kenya Sugar Board data:\n\n**Current Status:**\n- 15 factories across 8 regions\n- 795 production records analyzed\n- Total annual production: 4.69M tonnes\n- Average sucrose content: 12.8%\n\n**Key Trends:**\n- National factory dominates with 2.34M tonnes\n- Kakamega region shows highest efficiency\n- Quality varies from 10-16% sucrose content\n\n**Recommendations:**\n- Focus on yield improvement programs\n- Implement quality standardization\n- Invest in modern processing technology\n\nWould you like me to dive deeper into any specific aspect?`
  }

  const getMessageTypeLabel = (type: string) => {
    switch (type) {
      case 'data': return '📊 Data Analysis'
      case 'research': return '🌐 Global Research'
      case 'comprehensive': return '🎯 Strategic Insight'
      default: return '🤖 AI Assistant'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
      {/* Chat Header */}
      <div className="bg-green-600 text-white p-4 rounded-t-lg flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Bot className="h-6 w-6" />
          <div>
            <h3 className="font-semibold">Kenya Sugar Board AI Assistant</h3>
            <p className="text-sm text-green-100">Powered by Google Gemini & Tavily Research</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {message.sender === 'ai' && message.type && (
                <div className="text-xs font-medium text-green-600 mb-1">
                  {getMessageTypeLabel(message.type)}
                </div>
              )}
              <div className="whitespace-pre-wrap">{message.text}</div>
              <div className={`text-xs mt-1 ${
                message.sender === 'user' ? 'text-green-100' : 'text-gray-500'
              }`}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}

        {/* Expandable thinking section */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-50 border border-gray-200 p-3 rounded-lg w-full max-w-md">
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin text-green-600" />
                <span className="text-gray-700 font-medium">Thinking…</span>
              </div>
              <details className="mt-2 text-sm text-gray-600">
                <summary className="cursor-pointer select-none">Show details</summary>
                <div className="mt-2">
                  The AI is analyzing your data or performing research. This may take a few seconds depending on the query.
                </div>
              </details>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick questions */}
      <div className="px-4 pb-2">
        <div className="text-xs text-gray-600 mb-2">Quick questions:</div>
        <div className="flex flex-wrap gap-2">
          {suggestedQueries.slice(0, 4).map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(q.text)}
              className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-md text-gray-800 border border-gray-200"
            >
              {q.text}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
            placeholder="Ask about factory performance, regions, seasonal trends, or global comparisons…"
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-black placeholder:text-gray-500"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={!inputText.trim() || isLoading}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-300 text-white p-3 rounded-lg transition-colors"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  )
}