"use client";

import { useState } from 'react';
// 1. Import the Tabs components from shadcn/ui
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
// 2. Import your ChromosomeTable component
import { ChromosomeTable } from './ChromosomeTable';

export default function GenomeBrowser() {
  const [gene, setGene] = useState('BRCA1');
  
  // This placeholder data will eventually come from your API
  const genes = [
    { id: 'BRCA1', name: 'Breast Cancer Type 1', location: 'chr17:43,044,295-43,125,482' },
    { id: 'TP53', name: 'Tumor Protein P53', location: 'chr17:7,668,421-7,687,624' },
    { id: 'CFTR', name: 'Cystic Fibrosis Transmembrane', location: 'chr7:117,480,025-117,668,665' },
  ];

  return (
    // 3. Wrap everything in the Tabs component
    <Tabs defaultValue="gene-view" className="w-full">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="gene-view">Detailed Gene View</TabsTrigger>
        <TabsTrigger value="chromosome-list">Chromosome List</TabsTrigger>
      </TabsList>

      {/* This is the content for the "Detailed Gene View" tab */}
      <TabsContent value="gene-view">
        <div className="space-y-4 p-4 border rounded-lg mt-4 bg-white dark:bg-gray-800">
          <div className="flex gap-2 items-center">
            <label htmlFor="gene-select" className="text-sm font-medium">Select Gene:</label>
            <select
              id="gene-select"
              value={gene}
              onChange={(e) => setGene(e.target.value)}
              className="border rounded px-3 py-2 bg-transparent w-full"
            >
              {genes.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.id} - {g.name}
                </option>
              ))}
            </select>
          </div>
          
          {/* Chromosome Visualization */}
          <div className="bg-gray-100 dark:bg-gray-900/50 p-4 rounded">
            <div className="flex justify-between mb-2 text-sm">
              <span>{genes.find(g => g.id === gene)?.location.split(':')[0]}</span>
              <span>Scale: 1Mbp</span>
            </div>
            
            <div className="relative h-8 bg-blue-100 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded">
              <div className="absolute top-0 bottom-0 bg-blue-300 dark:bg-blue-600 w-1/2 left-1/4"></div>
              <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-2 py-1 rounded text-xs">
                {gene}
              </div>
            </div>
            
            {/* Gene Track */}
            <div className="mt-6">
              <div className="flex justify-between mb-1 text-sm">
                <span className="font-medium">Genes</span>
                <span className="text-gray-500 dark:text-gray-400">RefSeq</span>
              </div>
              <div className="relative h-16 bg-gray-50 dark:bg-gray-800/50 border rounded">
                <div className="absolute top-4 left-1/4 w-1/2 h-8 bg-green-200 dark:bg-green-800 border border-green-400 dark:border-green-600 rounded flex items-center justify-center">
                  <span className="text-xs">{gene}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </TabsContent>

      {/* This is the content for the "Chromosome List" tab */}
      <TabsContent value="chromosome-list">
        {/* 4. Place the ChromosomeTable component here */}
        <ChromosomeTable />
      </TabsContent>
    </Tabs>
  );
}