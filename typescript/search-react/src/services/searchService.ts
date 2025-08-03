import { SearchResult } from '../context/SearchContext';

interface SearchParams {
  query: string;
  startDate: string;
  endDate: string;
  databases: string[];
  subModules: string[];
  page: number;
  useHybrid?: boolean;
  semanticRatio?: number;
}

interface SearchResponse {
  hits: SearchResult[];
  totalHits: number;
  processingTimeMs: number;
  page: number;
  totalPages: number;
}

interface AdminResponse {
  success: boolean;
  message: string;
  details?: any;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001';

class SearchService {
  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async search(params: SearchParams): Promise<SearchResponse> {
    return this.makeRequest<SearchResponse>('/api/search', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  async getSubModules(): Promise<string[]> {
    return this.makeRequest<string[]>('/api/sub-modules');
  }

  async createIndex(): Promise<AdminResponse> {
    return this.makeRequest<AdminResponse>('/api/admin/create-index', {
      method: 'POST',
    });
  }

  async indexData(): Promise<AdminResponse> {
    return this.makeRequest<AdminResponse>('/api/admin/index-data', {
      method: 'POST',
    });
  }

  async debugSuspects(): Promise<AdminResponse> {
    return this.makeRequest<AdminResponse>('/api/admin/debug-suspects');
  }

  async debugDocuments(): Promise<AdminResponse> {
    return this.makeRequest<AdminResponse>('/api/admin/debug-documents');
  }

  async checkHealth(): Promise<{ status: string; services: Record<string, string> }> {
    return this.makeRequest<{ status: string; services: Record<string, string> }>('/api/health');
  }
}

export const searchService = new SearchService();

// Keep the mock search for fallback/development
const mockResults: SearchResult[] = [
  {
    id: '1001',
    sub_module_name: 'Motor Vehicle Theft',
    location: 'Nairobi CBD',
    submissionDate: '2025-06-15T10:30:00Z',
    description: 'Toyota Corolla stolen from parking lot near Kencom House',
    vehicle_registration: 'KCA 123A',
    suspect_name: 'John Doe',
    suspect_description: 'Male, approximately 25-30 years old, medium build',
    formData: {
      'Make': 'Toyota',
      'Model': 'Corolla',
      'Color': 'White',
      'Year': '2018'
    },
    _rankingScore: 0.95
  },
  {
    id: '1002',
    sub_module_name: 'Missing Person',
    location: 'Westlands',
    submissionDate: '2025-06-20T14:15:00Z',
    description: 'Missing person case - Jane Smith, last seen at Sarit Centre',
    victim_name: 'Jane Smith',
    formData: {
      'Age': '28',
      'Height': '5\'6"',
      'Last seen wearing': 'Blue dress and white sneakers'
    },
    _rankingScore: 0.87
  }
];

export async function mockSearch(params: SearchParams): Promise<SearchResponse> {
  // Try real search first, fallback to mock if it fails
  try {
    return await searchService.search(params);
  } catch (error) {
    console.warn('Real search failed, using mock data:', error);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Filter mock results based on search parameters
    let filteredResults = mockResults;

    // Filter by query
    if (params.query) {
      const query = params.query.toLowerCase();
      filteredResults = filteredResults.filter(result => 
        result.description?.toLowerCase().includes(query) ||
        result.location?.toLowerCase().includes(query) ||
        result.suspect_name?.toLowerCase().includes(query) ||
        result.victim_name?.toLowerCase().includes(query) ||
        result.vehicle_registration?.toLowerCase().includes(query) ||
        result.stolen_items?.toLowerCase().includes(query)
      );
    }

    // Filter by sub-modules
    if (params.subModules.length > 0) {
      filteredResults = filteredResults.filter(result =>
        params.subModules.includes(result.sub_module_name)
      );
    }

    // Simulate pagination
    const pageSize = 10;
    const startIndex = (params.page - 1) * pageSize;
    const paginatedResults = filteredResults.slice(startIndex, startIndex + pageSize);

    return {
      hits: paginatedResults,
      totalHits: filteredResults.length,
      processingTimeMs: Math.random() * 100 + 50,
      page: params.page,
      totalPages: Math.ceil(filteredResults.length / pageSize)
    };
  }
}