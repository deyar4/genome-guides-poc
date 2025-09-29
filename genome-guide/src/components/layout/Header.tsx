"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sun, Moon, Dna, Search } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useState } from "react";

// In the future, this component will get the selected gene from props
// and call a function to update the global state.
export default function Header() {
  const { theme, setTheme } = useTheme();
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearchSubmit = () => {
    if (!searchQuery) return;
    // This logic will eventually be moved to a global state manager
    alert(`Searching for gene: ${searchQuery}`);
  };

  return (
    // We are using the exact styles from your original layout here
    <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 shadow-sm px-6 py-4 flex justify-between items-center">
      
      {/* Left Side: Logo and App Name */}
      <div className="flex items-center gap-3">
        <Dna className="h-7 w-7 text-blue-600 dark:text-blue-400" />
        <h1 className="text-xl font-bold">Genome Guides</h1>
        <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded-full">v-Alpha-1.0</span>
      </div>
      
      {/* Right Side: Search, Theme, and User Info */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            type="search"
            placeholder="Search gene..."
            className="pl-10 w-64"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearchSubmit()}
          />
        </div>

        <Button
          variant="ghost" // Using ghost variant for a cleaner look
          size="icon"
          onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        >
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
        
        <div className="flex items-center gap-2">
          <div className="bg-muted border-2 border-dashed rounded-full w-8 h-8" />
          <div>
            <p className="text-sm font-medium">Researcher</p>
            <p className="text-xs text-muted-foreground">user@genomeguide.org</p>
          </div>
        </div>
      </div>
    </header>
  );
}