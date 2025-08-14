'use client'

import React from 'react'
import { Factory, MapPin, TrendingUp, Award, DollarSign, Zap } from 'lucide-react'

const statsData = [
  {
    title: 'Total Factories',
    value: '15',
    subtitle: 'Across 8 regions',
    icon: Factory,
    color: 'bg-blue-500',
    trend: '+2 this year'
  },
  {
    title: 'Total Production',
    value: '4.69M',
    subtitle: 'tonnes annually',
    icon: TrendingUp,
    color: 'bg-green-500',
    trend: '+8.5% vs last year'
  },
  {
    title: 'Production Value',
    value: 'KSh 25.2B',
    subtitle: 'million total value',
    icon: DollarSign,
    color: 'bg-yellow-500',
    trend: '+12.3% growth'
  },
  {
    title: 'Average Sucrose',
    value: '12.8%',
    subtitle: 'content quality',
    icon: Award,
    color: 'bg-purple-500',
    trend: 'Industry standard'
  },
  {
    title: 'Top Producer',
    value: 'National',
    subtitle: '2.34M tonnes',
    icon: Zap,
    color: 'bg-red-500',
    trend: 'Leading factory'
  },
  {
    title: 'Regions Covered',
    value: '8',
    subtitle: 'Geographic spread',
    icon: MapPin,
    color: 'bg-indigo-500',
    trend: 'Nationwide coverage'
  }
]

export default function StatsCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {statsData.map((stat, index) => {
        const Icon = stat.icon
        return (
          <div
            key={index}
            className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow duration-200"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3">
                  <div className={`${stat.color} p-2 rounded-lg`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  </div>
                </div>
                <div className="mt-3">
                  <p className="text-sm text-gray-500">{stat.subtitle}</p>
                  <p className="text-xs text-green-600 font-medium mt-1">{stat.trend}</p>
                </div>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}