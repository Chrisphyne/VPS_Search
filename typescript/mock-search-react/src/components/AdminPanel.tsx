import React, { useState } from 'react';
import { Settings, Database, RefreshCw, Bug, FileText } from 'lucide-react';

export function AdminPanel() {
  const [selectedAction, setSelectedAction] = useState<string>('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);

  const adminActions = [
    { id: 'create-index', label: 'Create Meilisearch Index', icon: Database },
    { id: 'index-data', label: 'Index Data', icon: RefreshCw },
    { id: 'debug-suspects', label: 'Debug Suspect Names', icon: Bug },
    { id: 'debug-documents', label: 'Debug Indexed Documents', icon: FileText },
  ];

  const executeAction = async () => {
    if (!selectedAction) return;

    setIsExecuting(true);
    setMessage(null);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      switch (selectedAction) {
        case 'create-index':
          setMessage({ type: 'success', text: 'Meilisearch index created and configured successfully.' });
          break;
        case 'index-data':
          setMessage({ type: 'success', text: 'Data indexed successfully. 1,247 documents processed.' });
          break;
        case 'debug-suspects':
          setMessage({ type: 'info', text: 'Found 89 documents with suspect information.' });
          break;
        case 'debug-documents':
          setMessage({ type: 'info', text: 'Index contains 1,247 documents across all sub-modules.' });
          break;
        default:
          setMessage({ type: 'error', text: 'Unknown action selected.' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Action failed. Please try again.' });
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mt-6">
      <div className="flex items-center space-x-2 mb-4">
        <Settings className="w-5 h-5 text-gray-600" />
        <h3 className="text-lg font-semibold text-gray-900">Admin Panel</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <label htmlFor="admin-action" className="block text-sm font-medium text-gray-700 mb-2">
            Select Action
          </label>
          <select
            id="admin-action"
            value={selectedAction}
            onChange={(e) => setSelectedAction(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Choose an action...</option>
            {adminActions.map((action) => (
              <option key={action.id} value={action.id}>
                {action.label}
              </option>
            ))}
          </select>
        </div>
        
        <button
          onClick={executeAction}
          disabled={!selectedAction || isExecuting}
          className="w-full flex items-center justify-center space-x-2 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          {isExecuting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Executing...</span>
            </>
          ) : (
            <>
              <Settings className="w-4 h-4" />
              <span>Execute</span>
            </>
          )}
        </button>
        
        {message && (
          <div className={`p-3 rounded-lg text-sm ${
            message.type === 'success' ? 'bg-green-50 text-green-800 border border-green-200' :
            message.type === 'error' ? 'bg-red-50 text-red-800 border border-red-200' :
            'bg-blue-50 text-blue-800 border border-blue-200'
          }`}>
            {message.text}
          </div>
        )}
      </div>
    </div>
  );
}