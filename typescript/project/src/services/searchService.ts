import { SearchResult } from "../context/SearchContext";

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

// Use empty string to leverage Vite's proxy configuration
const API_BASE_URL = "";

console.log("🔗 Using Vite proxy for API calls");

class SearchService {
    private async makeRequest<T>(
        endpoint: string,
        options: RequestInit = {},
    ): Promise<T> {
        const url = `${API_BASE_URL}${endpoint}`;
        console.log("🌐 Making request to:", url);
        console.log("📋 Request options:", options);

        try {
            const response = await fetch(url, {
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                    ...options.headers,
                },
                ...options,
            });

            console.log("📡 Response status:", response.status);
            console.log("📡 Response ok:", response.ok);

            if (!response.ok) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch {
                    errorData = {
                        error: `HTTP ${response.status}: ${response.statusText}`,
                    };
                }
                console.error("❌ API Error:", errorData);
                throw new Error(
                    errorData.error ||
                        `HTTP ${response.status}: ${response.statusText}`,
                );
            }

            const data = await response.json();
            console.log("✅ Response data:", data);
            return data;
        } catch (error) {
            console.error("🚨 Request failed:", error);
            if (error instanceof TypeError && error.message.includes("fetch")) {
                throw new Error(`Cannot connect to API server. Please ensure:

1. The API server is running on port 3001
2. Disable any ad blockers or browser extensions that might block requests
3. Check if your firewall is blocking the connection
4. Try refreshing the page

Error details: ${error.message}`);
            }
            throw error;
        }
    }

    async search(params: SearchParams): Promise<SearchResponse> {
        console.log("🔍 Performing search with params:", params);
        return this.makeRequest<SearchResponse>("/api/search", {
            method: "POST",
            body: JSON.stringify(params),
        });
    }

    async getSubModules(): Promise<string[]> {
        console.log("📋 Fetching sub-modules");
        return this.makeRequest<string[]>("/api/sub-modules");
    }

    async createIndex(): Promise<AdminResponse> {
        console.log("🔧 Creating index");
        return this.makeRequest<AdminResponse>("/api/admin/create-index", {
            method: "POST",
        });
    }

    async indexData(): Promise<AdminResponse> {
        console.log("📊 Indexing data");
        return this.makeRequest<AdminResponse>("/api/admin/index-data", {
            method: "POST",
        });
    }

    async debugSuspects(): Promise<AdminResponse> {
        console.log("🐛 Debugging suspects");
        return this.makeRequest<AdminResponse>("/api/admin/debug-suspects");
    }

    async debugDocuments(): Promise<AdminResponse> {
        console.log("🐛 Debugging documents");
        return this.makeRequest<AdminResponse>("/api/admin/debug-documents");
    }

    async checkHealth(): Promise<{
        status: string;
        services: Record<string, string>;
    }> {
        console.log("🏥 Checking health");
        return this.makeRequest<{
            status: string;
            services: Record<string, string>;
        }>("/api/health");
    }
}

export const searchService = new SearchService();

// Keep the mock search for fallback/development
const mockResults: SearchResult[] = [
    {
        id: "1001",
        sub_module_name: "Motor Vehicle Theft",
        location: "Nairobi CBD",
        submissionDate: "2025-06-15T10:30:00Z",
        description: "Toyota Corolla stolen from parking lot near Kencom House",
        vehicle_registration: "KCA 123A",
        suspect_name: "John Doe",
        suspect_description:
            "Male, approximately 25-30 years old, medium build",
        formData: {
            Make: "Toyota",
            Model: "Corolla",
            Color: "White",
            Year: "2018",
        },
        _rankingScore: 0.95,
    },
    {
        id: "1002",
        sub_module_name: "Missing Person",
        location: "Westlands",
        submissionDate: "2025-06-20T14:15:00Z",
        description:
            "Missing person case - Jane Smith, last seen at Sarit Centre",
        victim_name: "Jane Smith",
        formData: {
            Age: "28",
            Height: "5'6\"",
            "Last seen wearing": "Blue dress and white sneakers",
        },
        _rankingScore: 0.87,
    },
];

export async function mockSearch(
    params: SearchParams,
): Promise<SearchResponse> {
    console.warn("🔄 Using mock search - API may be unavailable");

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Filter mock results based on search parameters
    let filteredResults = mockResults;

    // Filter by query
    if (params.query) {
        const query = params.query.toLowerCase();
        filteredResults = filteredResults.filter(
            (result) =>
                result.description?.toLowerCase().includes(query) ||
                result.location?.toLowerCase().includes(query) ||
                result.suspect_name?.toLowerCase().includes(query) ||
                result.victim_name?.toLowerCase().includes(query) ||
                result.vehicle_registration?.toLowerCase().includes(query) ||
                result.stolen_items?.toLowerCase().includes(query),
        );
    }

    // Filter by sub-modules
    if (params.subModules.length > 0) {
        filteredResults = filteredResults.filter((result) =>
            params.subModules.includes(result.sub_module_name),
        );
    }

    // Simulate pagination
    const pageSize = 10;
    const startIndex = (params.page - 1) * pageSize;
    const paginatedResults = filteredResults.slice(
        startIndex,
        startIndex + pageSize,
    );

    return {
        hits: paginatedResults,
        totalHits: filteredResults.length,
        processingTimeMs: Math.random() * 100 + 50,
        page: params.page,
        totalPages: Math.ceil(filteredResults.length / pageSize),
    };
}
