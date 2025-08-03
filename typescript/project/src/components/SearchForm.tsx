import React from "react";
import { Search, RotateCcw, Calendar, Zap } from "lucide-react";
import { useSearch } from "../context/SearchContext";
import { searchService } from "../services/searchService";

export function SearchForm() {
    const { state, dispatch } = useSearch();

    const handleSearch = async (useHybrid = false) => {
        if (!state.query.trim()) {
            dispatch({
                type: "SET_ERROR",
                payload: "Please enter a search query.",
            });
            return;
        }

        dispatch({ type: "SET_LOADING", payload: true });
        dispatch({ type: "SET_ERROR", payload: null });

        console.log("🔍 Starting search with query:", state.query);
        console.log("📊 Search parameters:", {
            query: state.query,
            startDate: state.startDate,
            endDate: state.endDate,
            databases: state.selectedDatabases,
            subModules: state.selectedSubModules,
            page: state.currentPage,
            useHybrid,
            semanticRatio: 0.5,
        });

        try {
            const results = await searchService.search({
                query: state.query,
                startDate: state.startDate,
                endDate: state.endDate,
                databases: state.selectedDatabases,
                subModules: state.selectedSubModules,
                page: state.currentPage,
                useHybrid,
                semanticRatio: 0.5,
            });

            console.log("✅ Search completed successfully:", results);

            dispatch({
                type: "SET_RESULTS",
                payload: {
                    results: results.hits,
                    totalResults: results.totalHits,
                    totalPages: results.totalPages,
                },
            });
        } catch (error) {
            console.error("❌ Search failed:", error);
            const errorMessage =
                error instanceof Error ? error.message : "Search failed";
            dispatch({
                type: "SET_ERROR",
                payload: errorMessage,
            });
        }
    };

    const handleReset = () => {
        console.log("🔄 Resetting search");
        dispatch({ type: "RESET_SEARCH" });
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="space-y-6">
                {/* Search Input */}
                <div>
                    <label
                        htmlFor="search"
                        className="block text-sm font-medium text-gray-700 mb-2"
                    >
                        {/* Search Keywords */}
                    </label>
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                            id="search"
                            type="text"
                            value={state.query}
                            onChange={(e) =>
                                dispatch({
                                    type: "SET_QUERY",
                                    payload: e.target.value,
                                })
                            }
                            placeholder="Enter keywords to search..."
                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                            onKeyPress={(e) =>
                                e.key === "Enter" && handleSearch()
                            }
                        />
                    </div>
                </div>

                {/* Date Range */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label
                            htmlFor="startDate"
                            className="block text-sm font-medium text-gray-700 mb-2"
                        >
                            Start Date
                        </label>
                        <div className="relative">
                            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                id="startDate"
                                type="date"
                                value={state.startDate}
                                onChange={(e) =>
                                    dispatch({
                                        type: "SET_DATE_RANGE",
                                        payload: {
                                            startDate: e.target.value,
                                            endDate: state.endDate,
                                        },
                                    })
                                }
                                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                            />
                        </div>
                    </div>

                    <div>
                        <label
                            htmlFor="endDate"
                            className="block text-sm font-medium text-gray-700 mb-2"
                        >
                            End Date
                        </label>
                        <div className="relative">
                            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                id="endDate"
                                type="date"
                                value={state.endDate}
                                onChange={(e) =>
                                    dispatch({
                                        type: "SET_DATE_RANGE",
                                        payload: {
                                            startDate: state.startDate,
                                            endDate: e.target.value,
                                        },
                                    })
                                }
                                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                            />
                        </div>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row gap-3">
                    <button
                        onClick={() => handleSearch(false)}
                        disabled={state.isLoading}
                        className="flex-1 flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-6 rounded-lg transition-colors"
                    >
                        <Search className="w-5 h-5" />
                        <span>
                            {state.isLoading ? "Searching..." : "Search"}
                        </span>
                    </button>

                    {/* <button
                        onClick={() => handleSearch(true)}
                        disabled={state.isLoading}
                        className="flex-1 flex items-center justify-center space-x-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white font-medium py-3 px-6 rounded-lg transition-colors"
                    >
                        <Zap className="w-5 h-5" />
                        <span>
                            {state.isLoading ? "Searching..." : "AI Search"}
                        </span>
                    </button> */}

                    <button
                        onClick={handleReset}
                        className="flex items-center justify-center space-x-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-6 rounded-lg transition-colors"
                    >
                        <RotateCcw className="w-5 h-5" />
                        <span>Reset</span>
                    </button>
                </div>

                {/* Error Display */}
                {state.error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p className="text-red-800 text-sm font-medium">
                            Error:
                        </p>
                        <p className="text-red-700 text-sm mt-1">
                            {state.error}
                        </p>
                        <div className="mt-2 text-xs text-red-600">
                            <p>Troubleshooting tips:</p>
                            <ul className="list-disc list-inside mt-1 space-y-1">
                                <li>
                                    Check if the API server is running on port
                                    3001
                                </li>
                                <li>Try the Health Check in the Admin Panel</li>
                                <li>
                                    Check browser console for detailed error
                                    messages
                                </li>
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
