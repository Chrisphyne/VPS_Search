import React from "react";
import { Search, Settings, Shield } from "lucide-react";

interface HeaderProps {
    onToggleAdmin: () => void;
}

export function Header({ onToggleAdmin }: HeaderProps) {
    return (
        <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center space-x-3">
                        <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
                            <Shield className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-xl font-semibold text-gray-900">
                                ISE SEARCH
                            </h1>
                            <p className="text-sm text-gray-500">
                                Criminal Investigation Database
                            </p>
                        </div>
                    </div>

                    <div className="flex items-center space-x-4">
                        <button
                            onClick={onToggleAdmin}
                            className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
                        >
                            <Settings className="w-4 h-4" />
                            <span>Admin</span>
                        </button>

                        <div className="flex items-center space-x-2 px-3 py-2 bg-blue-50 rounded-md">
                            <Search className="w-4 h-4 text-blue-600" />
                            <span className="text-sm font-medium text-blue-900">
                                Search Portal
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}
