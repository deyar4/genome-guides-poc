"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sun, Moon, Dna, Search } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useState } from "react";
import { searchGenes, Gene } from "@/services/genomeApi";
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

type HeaderProps = {
  onGeneSelect: (geneSymbol: string) => void;
};

export default function Header({ onGeneSelect }: HeaderProps) {
  const { theme, setTheme } = useTheme();
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState<Gene[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearchChange = async (query: string) => {
    setSearchQuery(query);
    if (query.length < 2) {
      setResults([]);
      return;
    }
    setIsLoading(true);
    const searchResults = await searchGenes(query);
    setResults(searchResults);
    setIsLoading(false);
  };

  const handleSelectGene = (gene: Gene) => {
    if (gene.gene_name) {
      onGeneSelect(gene.gene_name);
      setSearchQuery("");
      setResults([]);
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-card px-6 py-4 flex justify-between items-center">
      {/* Left Side: Logo and App Name */}
      <div className="flex items-center gap-3">
        <Dna className="h-7 w-7 text-primary" />
        <h1 className="text-xl font-bold">Genome Guides</h1>
      </div>
      
      {/* Right Side: Search, Theme Toggle, and User Info */}
      <div className="flex gap-6">
        {/* Search Bar */}
        <div className="relative right-35 w-180">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search gene..."
            className="pl-10 w-180"
            value={searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
          />
          {results.length > 0 && (
            <div className="absolute top-full w-full mt-1 bg-popover border rounded-md shadow-lg z-50">
              {results.map((gene) => (
                <div
                  key={gene.id}
                  className="px-4 py-2 hover:bg-accent cursor-pointer"
                  onClick={() => handleSelectGene(gene)}
                >
                  <p className="font-medium">{gene.gene_name}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Theme Toggle Button */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        >
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
        
        {/* User Info */}
        <div className="flex items-center gap-2">
      <Avatar>
        <AvatarImage src="https://avatars.githubusercontent.com/u/6730450?v=4" alt="@shadcn" />
        <AvatarFallback>DA</AvatarFallback>
      </Avatar>          <div>
            <p className="text-sm font-medium">Dyar Amanalla</p>
            <p className="text-xs text-muted-foreground">dyar@genomeguides.de</p>
          </div>
        </div>
      </div>
    </header>
  );
}