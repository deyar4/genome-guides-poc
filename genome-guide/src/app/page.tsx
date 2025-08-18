// src/app/page.tsx
"use client"
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sun, Moon, Dna, Search, Activity, Book, Settings, Home, Database } from 'lucide-react';
import { useTheme } from 'next-themes';

export default function GenomeDashboard() {
  const { theme, setTheme } = useTheme();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [gene, setGene] = useState('BRCA1');
  const [location, setLocation] = useState('chr17:43,044,295-43,125,482');

  const genes = [
    { id: 'BRCA1', name: 'Breast Cancer Type 1', location: 'chr17:43,044,295-43,125,482', 
      description: 'Tumor suppressor gene involved in DNA repair. Mutations in BRCA1 increase the risk of breast and ovarian cancer.' },
    { id: 'TP53', name: 'Tumor Protein P53', location: 'chr17:7,668,421-7,687,624', 
      description: 'Crucial tumor suppressor gene. Encodes a protein that regulates cell division and prevents tumor formation.' },
    { id: 'CFTR', name: 'Cystic Fibrosis Transmembrane', location: 'chr7:117,480,025-117,668,665', 
      description: 'Encodes a chloride channel protein. Mutations cause cystic fibrosis, affecting lung and digestive system function.' },
  ];

  const geneData = genes.find(g => g.id === gene);

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 shadow-sm px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Dna className="h-7 w-7 text-blue-600 dark:text-blue-400" />
          <h1 className="text-xl font-bold">Genome Guides</h1>
          <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded-full">v-Alpha-1.0</span>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              type="text"
              placeholder="Search genes, regions, variants..."
              className="pl-10 w-64"
            />
          </div>
          
          <Button 
            variant="outline"
            size="sm"
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
            className="rounded-full"
          >
            {theme === 'light' ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          </Button>
          
          <div className="flex items-center gap-2">
            <div className="bg-gray-200 dark:bg-gray-700 border-2 border-dashed rounded-xl w-8 h-8" />
            <div>
              <p className="text-sm font-medium">Researcher</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">user@genomeguide.org</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="sticky top-16 h-[calc(100vh-4rem)] w-64 bg-white dark:bg-gray-800 border-r shadow-sm">
          <nav className="p-4 space-y-1">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === 'dashboard' 
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Home className="h-5 w-5" />
              <span>Dashboard</span>
            </button>
            
            <button 
              onClick={() => setActiveTab('browser')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === 'browser' 
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Dna className="h-5 w-5" />
              <span>Genome Browser</span>
            </button>
            
            <button 
              onClick={() => setActiveTab('tools')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === 'tools' 
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Activity className="h-5 w-5" />
              <span>Analysis Tools</span>
            </button>
            
            <button 
              onClick={() => setActiveTab('data')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === 'data' 
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Database className="h-5 w-5" />
              <span>Data Sources</span>
            </button>
            
            <button 
              onClick={() => setActiveTab('docs')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === 'docs' 
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Book className="h-5 w-5" />
              <span>Documentation</span>
            </button>
            
            <button 
              onClick={() => setActiveTab('settings')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === 'settings' 
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Settings className="h-5 w-5" />
              <span>Settings</span>
            </button>
          </nav>
          
          <div className="absolute bottom-0 w-full p-4 border-t">
            <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">Need help?</div>
            <Button variant="outline" className="w-full">
              Contact Support
            </Button>
          </div>
        </aside>

        {/* Content Area */}
        <main className="flex-1 overflow-auto max-h-[calc(100vh-4rem)]">
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Genome Browser */}
              <div className="lg:col-span-2">
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-xl font-semibold">Genome Browser</h2>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        Zoom In
                      </Button>
                      <Button variant="outline" size="sm">
                        Zoom Out
                      </Button>
                      <Button variant="outline" size="sm">
                        Reset View
                      </Button>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex gap-2">
                      <select
                        value={gene}
                        onChange={(e) => setGene(e.target.value)}
                        className="border rounded-lg px-3 py-2 bg-transparent text-sm w-full"
                      >
                        {genes.map((gene) => (
                          <option key={gene.id} value={gene.id}>
                            {gene.id} - {gene.name}
                          </option>
                        ))}
                      </select>
                      <Button className="whitespace-nowrap">
                        <Search className="h-4 w-4 mr-2" />
                        Search
                      </Button>
                    </div>
                    
                    <div className="bg-gray-100 dark:bg-gray-700/50 rounded-xl p-4">
                      <div className="flex justify-between mb-2 text-sm">
                        <span>{geneData?.location.split(':')[0]}</span>
                        <span className="text-gray-500 dark:text-gray-400">Scale: 1Mbp</span>
                      </div>
                      
                      {/* Chromosome Visualization */}
                      <div className="relative h-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
                        <div className="absolute top-0 bottom-0 bg-blue-300 dark:bg-blue-600 w-1/2 left-1/4 rounded-lg"></div>
                        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-lg text-xs font-medium">
                          {gene}
                        </div>
                      </div>
                      
                      {/* Gene Track */}
                      <div className="mt-6">
                        <div className="flex justify-between mb-1 text-sm">
                          <span className="font-medium">Genes</span>
                          <span className="text-gray-500 dark:text-gray-400">RefSeq</span>
                        </div>
                        <div className="relative h-16 bg-gray-50 dark:bg-gray-800/30 border rounded-lg">
                          <div className="absolute top-4 left-1/4 w-1/2 h-8 bg-green-200 dark:bg-green-800/70 border border-green-400 dark:border-green-600 rounded-lg flex items-center justify-center">
                            <span className="text-xs font-medium">{gene}</span>
                          </div>
                        </div>
                      </div>
                      
                      {/* Conservation Track */}
                      <div className="mt-4">
                        <div className="flex justify-between mb-1 text-sm">
                          <span className="font-medium">Conservation</span>
                          <span className="text-gray-500 dark:text-gray-400">PhyloP</span>
                        </div>
                        <div className="relative h-16 bg-gray-50 dark:bg-gray-800/30 border rounded-lg">
                          <div className="absolute top-0 bottom-0 left-1/4 w-1/2 bg-gradient-to-r from-blue-100 to-blue-400 dark:from-blue-900/50 dark:to-blue-600 rounded-lg"></div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500 dark:text-gray-400">Current Gene</p>
                        <p className="font-medium">{gene}</p>
                      </div>
                      <div>
                        <p className="text-gray-500 dark:text-gray-400">Location</p>
                        <p className="font-medium">{geneData?.location}</p>
                      </div>
                      <div>
                        <p className="text-gray-500 dark:text-gray-400">Gene Type</p>
                        <p className="font-medium">Protein Coding</p>
                      </div>
                      <div>
                        <p className="text-gray-500 dark:text-gray-400">Strand</p>
                        <p className="font-medium">Minus (-)</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Tools Section */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                  <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-5 hover:shadow-md transition-shadow">
                    <div className="bg-blue-100 dark:bg-blue-900/30 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                      <Activity className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h3 className="font-semibold mb-2">Variant Analyzer</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                      Upload VCF files to analyze genetic variants
                    </p>
                    <Button variant="outline" size="sm">
                      Try Now
                    </Button>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-5 hover:shadow-md transition-shadow">
                    <div className="bg-green-100 dark:bg-green-900/30 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                      <Dna className="h-6 w-6 text-green-600 dark:text-green-400" />
                    </div>
                    <h3 className="font-semibold mb-2">CRISPR Guide</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                      Design and validate CRISPR guide RNAs
                    </p>
                    <Button variant="outline" size="sm">
                      Try Now
                    </Button>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-5 hover:shadow-md transition-shadow">
                    <div className="bg-purple-100 dark:bg-purple-900/30 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                      <Database className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                    </div>
                    <h3 className="font-semibold mb-2">Sequence Aligner</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                      Align DNA/protein sequences with various algorithms
                    </p>
                    <Button variant="outline" size="sm">
                      Try Now
                    </Button>
                  </div>
                </div>
              </div>

              {/* Gene Information Panel */}
              <div className="space-y-6">
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-6">
                  <h2 className="text-xl font-semibold mb-4">Gene Information</h2>
                  <div className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 rounded-lg p-4 mb-6">
                    <div className="flex items-start gap-4">
                      <div className="bg-blue-500 text-white rounded-lg p-2">
                        <Dna className="h-6 w-6" />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold">{gene}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-300">{geneData?.name}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Location</p>
                      <p className="font-medium">{geneData?.location}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Description</p>
                      <p className="font-medium">{geneData?.description}</p>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Gene Type</p>
                        <p className="font-medium">Protein Coding</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Strand</p>
                        <p className="font-medium">Minus (-)</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Transcripts</p>
                        <p className="font-medium">5</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Exons</p>
                        <p className="font-medium">22</p>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Associated Diseases</p>
                      <div className="flex flex-wrap gap-2">
                        <span className="px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200 rounded-full text-xs">
                          Breast Cancer
                        </span>
                        <span className="px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200 rounded-full text-xs">
                          Ovarian Cancer
                        </span>
                        <span className="px-3 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-200 rounded-full text-xs">
                          Prostate Cancer
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recently Viewed Genes */}
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-6">
                  <h2 className="text-xl font-semibold mb-4">Recently Viewed</h2>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {genes.map((g) => (
                      <div 
                        key={g.id}
                        className={`p-4 rounded-lg border cursor-pointer transition-colors ${
                          g.id === gene
                            ? 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-700'
                            : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                        }`}
                        onClick={() => setGene(g.id)}
                      >
                        <div className="flex justify-between">
                          <span className="font-medium">{g.id}</span>
                          <span className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                            {g.location.split(':')[0]}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">{g.name}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Genome Statistics */}
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border p-6">
                  <h2 className="text-xl font-semibold mb-4">Genome Statistics</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-4">
                      <p className="text-sm text-gray-500 dark:text-gray-400">Total Genes</p>
                      <p className="text-2xl font-bold mt-1">20,365</p>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-4">
                      <p className="text-sm text-gray-500 dark:text-gray-400">Chromosomes</p>
                      <p className="text-2xl font-bold mt-1">24</p>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-4">
                      <p className="text-sm text-gray-500 dark:text-gray-400">Base Pairs</p>
                      <p className="text-2xl font-bold mt-1">3.2B</p>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-4">
                      <p className="text-sm text-gray-500 dark:text-gray-400">Known Variants</p>
                      <p className="text-2xl font-bold mt-1">676M</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}