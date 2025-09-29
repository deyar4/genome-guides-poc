// src/components/GeneInfoPanel.tsx
"use client";

import { useState, useEffect } from 'react';
import { getGene } from '@/lib/api';

export default function GeneInfoPanel({ symbol }: { symbol: string }) {
  const [geneData, setGeneData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGeneData = async () => {
      try {
        setLoading(true);
        const data = await getGene(symbol);
        setGeneData(data);
        setError(null);
      } catch (err) {
        setError('Failed to load gene data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (symbol) {
      fetchGeneData();
    }
  }, [symbol]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Loading gene data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 p-4">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 rounded-lg p-4 mb-6">
        <div className="flex items-start gap-4">
          <div className="bg-blue-500 text-white rounded-lg p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-bold">{geneData.symbol}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">{geneData.name}</p>
          </div>
        </div>
      </div>
      
      <div className="space-y-4">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Location</p>
          <p className="font-medium">{geneData.chromosome}:{geneData.start_position.toLocaleString()}-{geneData.end_position.toLocaleString()}</p>
        </div>
        
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Description</p>
          <p className="font-medium">{geneData.description}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Gene Type</p>
            <p className="font-medium capitalize">{geneData.gene_type.replace('_', ' ')}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Strand</p>
            <p className="font-medium">{geneData.strand}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Species</p>
            <p className="font-medium">{geneData.species}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Length</p>
            <p className="font-medium">{(geneData.end_position - geneData.start_position).toLocaleString()} bp</p>
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
  );
}