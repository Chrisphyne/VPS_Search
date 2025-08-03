import React, { useState } from 'react';
import { ChevronDown, ChevronUp, MapPin, Calendar, User, Car, Package, AlertTriangle } from 'lucide-react';
import { useSearch } from '../context/SearchContext';
import { format } from 'date-fns';

export function SearchResults() {
  const { state } = useSearch();
  const [expandedResults, setExpandedResults] = useState<Set<string>>(new Set());

  const toggleExpanded = (id: string) => {
    const newExpanded = new Set(expandedResults);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedResults(newExpanded);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return dateString;
    }
  };

  const getModuleIcon = (moduleName: string) => {
    switch (moduleName?.toLowerCase()) {
      case 'missing person':
        return <User className="w-5 h-5 text-orange-600" />;
      case 'motor vehicle theft':
        return <Car className="w-5 h-5 text-red-600" />;
      case 'stolen lost item':
        return <Package className="w-5 h-5 text-purple-600" />;
      case 'gbv':
      case 'rape':
      case 'assault':
        return <AlertTriangle className="w-5 h-5 text-red-600" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-gray-600" />;
    }
  };

  const getModuleColor = (moduleName: string) => {
    switch (moduleName?.toLowerCase()) {
      case 'missing person':
        return 'bg-orange-50 text-orange-800 border-orange-200';
      case 'motor vehicle theft':
        return 'bg-red-50 text-red-800 border-red-200';
      case 'stolen lost item':
        return 'bg-purple-50 text-purple-800 border-purple-200';
      case 'gbv':
      case 'rape':
      case 'assault':
        return 'bg-red-50 text-red-800 border-red-200';
      case 'cyber crime':
        return 'bg-blue-50 text-blue-800 border-blue-200';
      case 'homicide':
      case 'death':
        return 'bg-gray-50 text-gray-800 border-gray-200';
      default:
        return 'bg-gray-50 text-gray-800 border-gray-200';
    }
  };

  if (state.isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <div className="flex items-center justify-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          <span className="text-gray-600">Searching...</span>
        </div>
      </div>
    );
  }

  if (state.results.length === 0 && state.query) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
        <div className="text-gray-500">
          <Package className="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Results Found</h3>
          <p>Try adjusting your search terms or filters.</p>
        </div>
      </div>
    );
  }

  if (state.results.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
        <div className="text-gray-500">
          <Package className="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Search</h3>
          <p>Enter keywords and select filters to begin your search.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            Search Results ({state.totalResults} found)
          </h2>
          <span className="text-sm text-gray-500">
            Page {state.currentPage} of {state.totalPages}
          </span>
        </div>
      </div>

      {state.results.map((result) => {
        const isExpanded = expandedResults.has(result.id);
        
        return (
          <div
            key={result.id}
            className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
          >
            <div
              className="p-6 cursor-pointer"
              onClick={() => toggleExpanded(result.id)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-3">
                    {getModuleIcon(result.sub_module_name)}
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getModuleColor(result.sub_module_name)}`}>
                      {result.sub_module_name || 'Unknown'}
                    </span>
                    <span className="text-sm text-gray-500">ID: {result.id}</span>
                  </div>
                  
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    {result.description || 'No description available'}
                  </h3>
                  
                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                    {result.location && (
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4" />
                        <span>{result.location}</span>
                      </div>
                    )}
                    {result.submissionDate && (
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(result.submissionDate)}</span>
                      </div>
                    )}
                    {result._rankingScore && (
                      <div className="text-xs bg-gray-100 px-2 py-1 rounded">
                        Score: {result._rankingScore.toFixed(2)}
                      </div>
                    )}
                  </div>
                </div>
                
                <button className="ml-4 p-2 hover:bg-gray-100 rounded-lg transition-colors">
                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  )}
                </button>
              </div>
            </div>
            
            {isExpanded && (
              <div className="border-t border-gray-200 p-6 bg-gray-50">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Key Information */}
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Key Information</h4>
                    <div className="space-y-2 text-sm">
                      {result.victim_name && (
                        <div>
                          <span className="font-medium text-gray-700">Victim:</span>
                          <span className="ml-2 text-gray-600">{result.victim_name}</span>
                        </div>
                      )}
                      {result.suspect_name && (
                        <div>
                          <span className="font-medium text-gray-700">Suspect:</span>
                          <span className="ml-2 text-gray-600">{result.suspect_name}</span>
                        </div>
                      )}
                      {result.vehicle_registration && (
                        <div>
                          <span className="font-medium text-gray-700">Vehicle Reg:</span>
                          <span className="ml-2 text-gray-600">{result.vehicle_registration}</span>
                        </div>
                      )}
                      {result.stolen_items && (
                        <div>
                          <span className="font-medium text-gray-700">Stolen Items:</span>
                          <span className="ml-2 text-gray-600">{result.stolen_items}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  {/* Additional Details */}
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Additional Details</h4>
                    <div className="space-y-2 text-sm">
                      {result.suspect_description && (
                        <div>
                          <span className="font-medium text-gray-700">Suspect Description:</span>
                          <p className="mt-1 text-gray-600">{result.suspect_description}</p>
                        </div>
                      )}
                      {result.formData && Object.keys(result.formData).length > 0 && (
                        <div>
                          <span className="font-medium text-gray-700">Form Data:</span>
                          <div className="mt-2 space-y-1">
                            {Object.entries(result.formData).slice(0, 5).map(([key, value]) => (
                              <div key={key} className="text-xs">
                                <span className="font-medium text-gray-600">{key}:</span>
                                <span className="ml-1 text-gray-500">{String(value)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}