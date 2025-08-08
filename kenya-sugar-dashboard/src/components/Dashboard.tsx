'use client'

import React, { useState } from 'react'
import { Factory, TrendingUp, Globe, MessageSquare, BarChart3, MapPin } from 'lucide-react'
import StatsCards from './StatsCards'
import FactoryAnalytics from './FactoryAnalytics'
import ChatInterface from './ChatInterface'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-orange-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-green-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <div className="bg-green-600 p-2 rounded-lg">
                <Factory className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  🇰🇪 Kenya Sugar Board
                </h1>
                <p className="text-sm text-gray-600">
                  AI-Powered Industry Analytics
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 px-3 py-1 rounded-full">
                <span className="text-sm font-medium text-green-800">
                  15 Factories • 8 Regions • 795 Records
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'analytics', label: 'Factory Analytics', icon: Factory },
              { id: 'regions', label: 'Regional Analysis', icon: MapPin },
              { id: 'ai-chat', label: 'AI Assistant', icon: MessageSquare },
              { id: 'global', label: 'Global Insights', icon: Globe }
            ].map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-green-500 text-green-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Industry Overview
              </h2>
              <p className="text-gray-600">
                Real-time insights from Kenya's sugar industry performance across all regions and factories.
              </p>
            </div>
            <StatsCards />
            <FactoryAnalytics />
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Factory Performance Analytics
              </h2>
              <p className="text-gray-600">
                Detailed analysis of production efficiency, quality metrics, and operational performance.
              </p>
            </div>
            <FactoryAnalytics detailed={true} />
          </div>
        )}

        {activeTab === 'regions' && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Regional Performance Analysis
              </h2>
              <p className="text-gray-600">
                Comparative analysis across Kenya's 8 sugar-producing regions.
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-center py-12">
                <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Regional Analytics</h3>
                <p className="text-gray-600">Coming soon - Interactive regional performance maps and comparisons</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ai-chat' && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                AI Assistant
              </h2>
              <p className="text-gray-600">
                Ask questions about your sugar industry data. Get insights powered by Google Gemini and Tavily research.
              </p>
            </div>
            <ChatInterface />
          </div>
        )}

        {activeTab === 'global' && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Global Industry Insights
              </h2>
              <p className="text-gray-600">
                How Kenya compares to global sugar industry standards and best practices.
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-center py-12">
                <Globe className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Global Benchmarking</h3>
                <p className="text-gray-600">Real-time global industry comparisons and research insights</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}