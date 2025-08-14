'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, Settings, MessageCircle, Trash2, Server, CheckCircle, AlertCircle, Clock } from 'lucide-react';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  status?: string;
  provider?: string;
}

interface ServerConfig {
  host: string;
  port: string;
  isConnected: boolean;
  status?: string;
  provider?: string;
  version?: string;
}

const SAMPLE_QUERIES = [
  "What are the key financial challenges facing Kenya's sugar sector?",
  "Compare production efficiency across different factories",
  "What are the main production challenges in the sugar industry?",
  "Which regions have the highest sugar production?",
  "Analyze seasonal patterns in sugar production",
  "Provide recommendations for improving factory efficiency"
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId] = useState('nextjs_user_001');
  const [showSettings, setShowSettings] = useState(false);
  
  // Get API base URL from environment variable or default
  const envApiUrl = process.env.API_BASE_URL || 'http://localhost:8000';
  const urlParts = envApiUrl.replace('http://', '').split(':');
  
  const [serverConfig, setServerConfig] = useState<ServerConfig>({
    host: urlParts[0] || 'localhost',
    port: urlParts[1] || '8000',
    isConnected: false
  });

  const apiBaseUrl = process.env.API_BASE_URL || `http://${serverConfig.host}:${serverConfig.port}`;

  useEffect(() => {
    // Add welcome message
    setMessages([{
      id: '1',
      content: `Welcome to the Kenya Sugar Board Analysis System! 🇰🇪

I'm your AI assistant for analyzing Kenya's sugar industry. I can help you with:
• Financial challenges and performance analysis
• Production efficiency and factory comparisons  
• Regional performance insights
• Industry recommendations and strategic planning

Configure your server connection in settings, then start asking questions!

*This system has conversation memory - I'll remember our discussion context.*`,
      role: 'assistant',
      timestamp: new Date().toISOString()
    }]);

    // Try to connect to default server
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/health`, { timeout: 5000 });
      const data = response.data;
      
      setServerConfig(prev => ({
        ...prev,
        isConnected: true,
        status: data.status,
        provider: data.llm_provider,
        version: data.version
      }));

      // Load conversation history
      loadConversationHistory();
    } catch (error) {
      setServerConfig(prev => ({
        ...prev,
        isConnected: false,
        status: 'disconnected'
      }));
    }
  };

  const loadConversationHistory = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/conversations/${conversationId}/history`);
      if (response.data.success && response.data.messages.length > 0) {
        const historyMessages: Message[] = response.data.messages.map((msg: any, index: number) => ({
          id: `history_${index}`,
          content: msg.content,
          role: msg.role === 'human' ? 'user' : 'assistant',
          timestamp: msg.timestamp || new Date().toISOString()
        }));
        
        setMessages(prev => [prev[0], ...historyMessages]); // Keep welcome message first
      }
    } catch (error) {
      console.log('No conversation history found');
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading || !serverConfig.isConnected) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${apiBaseUrl}/analyze`, {
        query: inputValue,
        conversation_id: conversationId,
        type: 'comprehensive'
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.response,
        role: 'assistant',
        timestamp: new Date().toISOString(),
        status: response.data.status,
        provider: response.data.provider
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Error: Could not connect to the analysis system. Please check your server connection.`,
        role: 'assistant',
        timestamp: new Date().toISOString(),
        status: 'error'
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearConversation = async () => {
    if (!confirm('Clear conversation history?')) return;

    try {
      await axios.post(`${apiBaseUrl}/conversations/${conversationId}/clear`);
      setMessages([{
        id: '1',
        content: 'Conversation cleared! Ready for new questions about Kenya\'s sugar sector.',
        role: 'assistant',
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      console.error('Failed to clear conversation:', error);
    }
  };

  const useQuery = (query: string) => {
    setInputValue(query);
  };

  const formatMessage = (content: string) => {
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
      .replace(/- (.*?)(<br>|$)/g, '• $1$2');
  };

  const getStatusIcon = () => {
    if (serverConfig.isConnected) {
      return <CheckCircle className="w-5 h-5 text-green-500" />;
    } else {
      return <AlertCircle className="w-5 h-5 text-red-500" />;
    }
  };

  return (
    <div className="container mx-auto max-w-7xl h-screen flex flex-col p-4">
      {/* Header */}
      <div className="card mb-4 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
              🇰🇪 Kenya Sugar Board Analysis
            </h1>
            <p className="text-gray-600 mt-1">AI-Powered Data Analysis with Conversation Memory</p>
          </div>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="btn-secondary flex items-center gap-2"
          >
            <Settings className="w-4 h-4" />
            Settings
          </button>
        </div>

        {/* Server Status */}
        <div className="mt-4 flex items-center gap-4 text-sm">
          {getStatusIcon()}
          <span className={serverConfig.isConnected ? 'status-healthy' : 'status-error'}>
            {serverConfig.isConnected ? 'Connected' : 'Disconnected'}
          </span>
          {serverConfig.provider && (
            <span className="status-healthy">Provider: {serverConfig.provider}</span>
          )}
          {serverConfig.version && (
            <span className="status-healthy">Version: {serverConfig.version}</span>
          )}
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-3">Server Configuration</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Server Host</label>
                <input
                  type="text"
                  value={serverConfig.host}
                  onChange={(e) => setServerConfig(prev => ({ ...prev, host: e.target.value }))}
                  className="input-field"
                  placeholder="localhost or IP address"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Port</label>
                <input
                  type="text"
                  value={serverConfig.port}
                  onChange={(e) => setServerConfig(prev => ({ ...prev, port: e.target.value }))}
                  className="input-field"
                  placeholder="8000"
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={testConnection}
                  className="btn-success flex items-center gap-2 w-full"
                >
                  <Server className="w-4 h-4" />
                  Test Connection
                </button>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-600">
              Full URL: <code className="bg-gray-200 px-2 py-1 rounded">{apiBaseUrl}</code>
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 flex gap-4 min-h-0">
        {/* Sidebar */}
        <div className="w-80 card p-4 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-800">Conversation</h2>
            <button
              onClick={clearConversation}
              className="text-red-600 hover:text-red-700 p-1"
              title="Clear conversation"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>

          <div className="mb-4 text-sm text-gray-600">
            ID: <code className="bg-gray-100 px-2 py-1 rounded text-xs">{conversationId}</code>
          </div>

          <div className="flex-1">
            <h3 className="font-medium mb-3 text-gray-700">💡 Sample Queries</h3>
            <div className="space-y-2">
              {SAMPLE_QUERIES.map((query, index) => (
                <button
                  key={index}
                  onClick={() => useQuery(query)}
                  className="w-full text-left p-3 text-sm bg-gray-50 hover:bg-gray-100 rounded-lg border transition-colors"
                  disabled={!serverConfig.isConnected}
                >
                  {query}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 card flex flex-col">
          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto scrollbar-thin">
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <div className="flex items-center gap-2 mb-2 text-sm">
                        <MessageCircle className="w-4 h-4" />
                        <span className="font-medium">AI Assistant</span>
                        {message.status && (
                          <span className="text-xs opacity-75">
                            [{message.status}]
                          </span>
                        )}
                      </div>
                    )}
                    <div
                      dangerouslySetInnerHTML={{
                        __html: formatMessage(message.content)
                      }}
                    />
                    <div className="text-xs opacity-75 mt-2">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-3 rounded-lg">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Clock className="w-4 h-4 animate-spin" />
                      AI is analyzing your query...
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Input Area */}
          <div className="border-t p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder={
                  serverConfig.isConnected
                    ? "Ask about Kenya's sugar sector..."
                    : "Configure server connection first..."
                }
                className="flex-1 input-field"
                disabled={!serverConfig.isConnected || isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!inputValue.trim() || isLoading || !serverConfig.isConnected}
                className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-4 h-4" />
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}