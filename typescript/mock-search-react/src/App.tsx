import React, { useState } from 'react';
import { Header } from './components/Header';
import { SearchFilters } from './components/SearchFilters';
import { SearchForm } from './components/SearchForm';
import { SearchResults } from './components/SearchResults';
import { AdminPanel } from './components/AdminPanel';
import { Pagination } from './components/Pagination';
import { SearchProvider } from './context/SearchContext';

function App() {
  const [showAdminPanel, setShowAdminPanel] = useState(false);

  return (
    <SearchProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Header onToggleAdmin={() => setShowAdminPanel(!showAdminPanel)} />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <div className="lg:col-span-1">
              <SearchFilters />
              {showAdminPanel && <AdminPanel />}
            </div>
            
            {/* Main Content */}
            <div className="lg:col-span-3 space-y-6">
              <SearchForm />
              <SearchResults />
              <Pagination />
            </div>
          </div>
        </div>
      </div>
    </SearchProvider>
  );
}

export default App;