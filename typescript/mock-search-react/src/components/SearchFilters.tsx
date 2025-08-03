import React from 'react';
import { Database, Filter } from 'lucide-react';
import { useSearch } from '../context/SearchContext';

const DATABASE_OPTIONS = [
  'ALL',
  'WATCHLIST DB',
  'STOLEN/LOST ITEMS DB',
  'MISSING PERSONS DB',
  'EVIDENCE DB',
  'STOLEN VEHICLES DB',
  'PRISONER PROPERTY DB'
];

const SUB_MODULE_OPTIONS = [
  'GBV',
  'Stolen Lost Item',
  'Robbery',
  'Rape',
  'Motor Vehicle Theft',
  'Missing Person',
  'Homicide',
  'Death',
  'Cyber Crime',
  'Burglary',
  'Assault',
  'Arson'
];

export function SearchFilters() {
  const { state, dispatch } = useSearch();

  const handleDatabaseChange = (database: string) => {
    let newSelection: string[];
    
    if (database === 'ALL') {
      newSelection = state.selectedDatabases.includes('ALL') ? [] : DATABASE_OPTIONS;
    } else {
      if (state.selectedDatabases.includes(database)) {
        newSelection = state.selectedDatabases.filter(db => db !== database && db !== 'ALL');
      } else {
        newSelection = [...state.selectedDatabases.filter(db => db !== 'ALL'), database];
        if (newSelection.length === DATABASE_OPTIONS.length - 1) {
          newSelection = DATABASE_OPTIONS;
        }
      }
    }
    
    dispatch({ type: 'SET_DATABASES', payload: newSelection });
  };

  const handleSubModuleChange = (subModule: string) => {
    const newSelection = state.selectedSubModules.includes(subModule)
      ? state.selectedSubModules.filter(sm => sm !== subModule)
      : [...state.selectedSubModules, subModule];
    
    dispatch({ type: 'SET_SUB_MODULES', payload: newSelection });
  };

  return (
    <div className="space-y-6">
      {/* Database Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Database className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Databases</h3>
        </div>
        
        <div className="space-y-3">
          {DATABASE_OPTIONS.map((database) => (
            <label
              key={database}
              className="flex items-center space-x-3 cursor-pointer group"
            >
              <input
                type="checkbox"
                checked={state.selectedDatabases.includes(database)}
                onChange={() => handleDatabaseChange(database)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
              />
              <span className={`text-sm font-medium transition-colors ${
                state.selectedDatabases.includes(database)
                  ? 'text-blue-900'
                  : 'text-gray-700 group-hover:text-gray-900'
              }`}>
                {database}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Sub-Module Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Filter className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Crime Types</h3>
        </div>
        
        <div className="space-y-3 max-h-64 overflow-y-auto">
          {SUB_MODULE_OPTIONS.map((subModule) => (
            <label
              key={subModule}
              className="flex items-center space-x-3 cursor-pointer group"
            >
              <input
                type="checkbox"
                checked={state.selectedSubModules.includes(subModule)}
                onChange={() => handleSubModuleChange(subModule)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
              />
              <span className={`text-sm font-medium transition-colors ${
                state.selectedSubModules.includes(subModule)
                  ? 'text-blue-900'
                  : 'text-gray-700 group-hover:text-gray-900'
              }`}>
                {subModule}
              </span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}