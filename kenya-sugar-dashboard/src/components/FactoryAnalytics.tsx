'use client'

import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'

// Sample data based on your actual Kenya Sugar Board data
const factoryProductionData = [
  { name: 'National', production: 2343393, sucrose: 0, efficiency: 100 },
  { name: 'Butali', production: 351318, sucrose: 13.6, efficiency: 85 },
  { name: 'West-Kenya', production: 338866, sucrose: 13.3, efficiency: 82 },
  { name: 'Kibos', production: 330860, sucrose: 12.8, efficiency: 78 },
  { name: 'Mumias', production: 325017, sucrose: 13.2, efficiency: 80 },
  { name: 'Nzoia', production: 310729, sucrose: 11.7, efficiency: 75 },
  { name: 'Muhoroni', production: 83693, sucrose: 12.9, efficiency: 65 },
  { name: 'Olepito', production: 81705, sucrose: 11.8, efficiency: 62 }
]

const regionalData = [
  { name: 'National', value: 2343393, color: '#ff6b6b' },
  { name: 'Kakamega', value: 1093037, color: '#4ecdc4' },
  { name: 'Kisumu', value: 488789, color: '#45b7d1' },
  { name: 'Trans-Nzoia', value: 310729, color: '#96ceb4' },
  { name: 'Narok', value: 228361, color: '#feca57' },
  { name: 'Kericho', value: 80539, color: '#ff9ff3' },
  { name: 'Busia', value: 71491, color: '#54a0ff' },
  { name: 'Migori', value: 70447, color: '#5f27cd' }
]

const monthlyTrends = [
  { month: 'Jan', production: 380000, quality: 12.5 },
  { month: 'Feb', production: 420000, quality: 12.8 },
  { month: 'Mar', production: 450000, quality: 13.1 },
  { month: 'Apr', production: 480000, quality: 13.3 },
  { month: 'May', production: 520000, quality: 13.0 },
  { month: 'Jun', production: 510000, quality: 12.9 },
  { month: 'Jul', production: 490000, quality: 12.7 },
  { month: 'Aug', production: 460000, quality: 12.6 }
]

interface FactoryAnalyticsProps {
  detailed?: boolean
}

export default function FactoryAnalytics({ detailed = false }: FactoryAnalyticsProps) {
  return (
    <div className="space-y-8">
      {/* Production by Factory */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Production by Factory (Tonnes)
        </h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={factoryProductionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45}
                textAnchor="end"
                height={80}
                fontSize={12}
              />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'production' ? `${Number(value).toLocaleString()} tonnes` : `${value}%`,
                  name === 'production' ? 'Production' : 'Sucrose Content'
                ]}
              />
              <Bar dataKey="production" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {detailed && (
        <>
          {/* Sucrose Content Quality */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              Sucrose Content Quality by Factory
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={factoryProductionData.filter(f => f.sucrose > 0)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis domain={[10, 16]} />
                  <Tooltip formatter={(value) => [`${value}%`, 'Sucrose Content']} />
                  <Line 
                    type="monotone" 
                    dataKey="sucrose" 
                    stroke="#f59e0b" 
                    strokeWidth={3}
                    dot={{ fill: '#f59e0b', strokeWidth: 2, r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Monthly Production Trends */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              Monthly Production Trends
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={monthlyTrends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Line 
                    yAxisId="left"
                    type="monotone" 
                    dataKey="production" 
                    stroke="#10b981" 
                    strokeWidth={3}
                    name="Production (tonnes)"
                  />
                  <Line 
                    yAxisId="right"
                    type="monotone" 
                    dataKey="quality" 
                    stroke="#f59e0b" 
                    strokeWidth={3}
                    name="Quality (%)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}

      {/* Regional Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Production by Region
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={regionalData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {regionalData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${Number(value).toLocaleString()} tonnes`, 'Production']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Top Performing Factories
          </h3>
          <div className="space-y-4">
            {factoryProductionData.slice(0, 6).map((factory, index) => (
              <div key={factory.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="bg-green-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{factory.name}</p>
                    <p className="text-sm text-gray-600">
                      {factory.sucrose > 0 ? `${factory.sucrose}% sucrose` : 'Leading producer'}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">
                    {(factory.production / 1000).toFixed(0)}K tonnes
                  </p>
                  <p className="text-sm text-green-600">
                    {factory.efficiency}% efficiency
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}