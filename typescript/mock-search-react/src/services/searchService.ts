import { SearchResult } from '../context/SearchContext';

interface SearchParams {
  query: string;
  startDate: string;
  endDate: string;
  databases: string[];
  subModules: string[];
  page: number;
}

interface SearchResponse {
  hits: SearchResult[];
  totalHits: number;
  processingTimeMs: number;
}

// Mock data for demonstration
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
  },
  {
    id: '1003',
    sub_module_name: 'Stolen Lost Item',
    location: 'Karen',
    submissionDate: '2025-06-18T09:45:00Z',
    description: 'Laptop and mobile phone stolen from residence',
    stolen_items: 'Electronics',
    suspect_description: 'Two suspects, both male, fled on motorcycle',
    formData: {
      'Items stolen': 'MacBook Pro, iPhone 13',
      'Time of incident': '3:00 AM',
      'Point of entry': 'Bedroom window'
    },
    _rankingScore: 0.82
  },
  {
    id: '1004',
    sub_module_name: 'Assault',
    location: 'Kibera',
    submissionDate: '2025-06-22T16:20:00Z',
    description: 'Physical assault case reported at local clinic',
    victim_name: 'Michael Ochieng',
    suspect_name: 'Unknown',
    formData: {
      'Injuries sustained': 'Bruises on face and arms',
      'Weapon used': 'Blunt object',
      'Witnesses': '2 witnesses present'
    },
    _rankingScore: 0.78
  },
  {
    id: '1005',
    sub_module_name: 'Cyber Crime',
    location: 'Online',
    submissionDate: '2025-06-25T11:30:00Z',
    description: 'Online fraud case - fake investment scheme',
    formData: {
      'Platform': 'WhatsApp',
      'Amount lost': 'KSh 50,000',
      'Suspect contact': '+254712345678'
    },
    _rankingScore: 0.75
  }
];

export async function mockSearch(params: SearchParams): Promise<SearchResponse> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Filter results based on search parameters
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

  // Filter by date range (simplified)
  if (params.startDate && params.endDate) {
    const startDate = new Date(params.startDate);
    const endDate = new Date(params.endDate);
    filteredResults = filteredResults.filter(result => {
      if (!result.submissionDate) return false;
      const resultDate = new Date(result.submissionDate);
      return resultDate >= startDate && resultDate <= endDate;
    });
  }

  // Simulate pagination
  const pageSize = 10;
  const startIndex = (params.page - 1) * pageSize;
  const paginatedResults = filteredResults.slice(startIndex, startIndex + pageSize);

  return {
    hits: paginatedResults,
    totalHits: filteredResults.length,
    processingTimeMs: Math.random() * 100 + 50
  };
}