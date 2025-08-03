import React, { createContext, useContext, useReducer, ReactNode } from 'react';

export interface SearchResult {
  id: string;
  sub_module_name: string;
  location?: string;
  submissionDate?: string;
  description?: string;
  suspect_name?: string;
  suspect_description?: string;
  victim_name?: string;
  vehicle_registration?: string;
  stolen_items?: string;
  formData?: Record<string, any>;
  _rankingScore?: number;
}

interface SearchState {
  query: string;
  startDate: string;
  endDate: string;
  selectedDatabases: string[];
  selectedSubModules: string[];
  results: SearchResult[];
  isLoading: boolean;
  currentPage: number;
  totalPages: number;
  totalResults: number;
  error: string | null;
}

type SearchAction =
  | { type: 'SET_QUERY'; payload: string }
  | { type: 'SET_DATE_RANGE'; payload: { startDate: string; endDate: string } }
  | { type: 'SET_DATABASES'; payload: string[] }
  | { type: 'SET_SUB_MODULES'; payload: string[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_RESULTS'; payload: { results: SearchResult[]; totalResults: number; totalPages: number } }
  | { type: 'SET_PAGE'; payload: number }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'RESET_SEARCH' };


// Get dynamic dates - 1 month before now
const getDefaultDates = () => {
  const now = new Date();
  const oneMonthAgo = new Date();
  oneMonthAgo.setMonth(now.getMonth() - 1);
  
  return {
    startDate: oneMonthAgo.toISOString().split('T')[0],
    endDate: now.toISOString().split('T')[0]
  };
};

const defaultDates = getDefaultDates();


const initialState: SearchState = {
  query: '',
  startDate: defaultDates.startDate,
  endDate: defaultDates.endDate,
  selectedDatabases: [],
  selectedSubModules: [],
  results: [],
  isLoading: false,
  currentPage: 1,
  totalPages: 1,
  totalResults: 0,
  error: null,
};

function searchReducer(state: SearchState, action: SearchAction): SearchState {
  switch (action.type) {
    case 'SET_QUERY':
      return { ...state, query: action.payload };
    case 'SET_DATE_RANGE':
      return { ...state, ...action.payload };
    case 'SET_DATABASES':
      return { ...state, selectedDatabases: action.payload };
    case 'SET_SUB_MODULES':
      return { ...state, selectedSubModules: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_RESULTS':
      return { 
        ...state, 
        results: action.payload.results,
        totalResults: action.payload.totalResults,
        totalPages: action.payload.totalPages,
        isLoading: false,
        error: null
      };
    case 'SET_PAGE':
      return { ...state, currentPage: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false };
    case 'RESET_SEARCH':
      const newDefaultDates = getDefaultDates();
      return { 
        ...initialState,
        startDate: newDefaultDates.startDate,
        endDate: newDefaultDates.endDate
      };
    default:
      return state;
  }
}

const SearchContext = createContext<{
  state: SearchState;
  dispatch: React.Dispatch<SearchAction>;
} | null>(null);

export function SearchProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(searchReducer, initialState);

  return (
    <SearchContext.Provider value={{ state, dispatch }}>
      {children}
    </SearchContext.Provider>
  );
}

export function useSearch() {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
}
