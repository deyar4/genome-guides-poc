"use client";
import { useState, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ChromosomeTable } from "@/components/features/genome-browser/ChromosomeTable";
import ChromosomeVisualizer from "@/components/features/genome-browser/ChromosomeVisualizer";
import { getGeneByName, Gene } from "@/services/genomeApi";
import { Skeleton } from "../ui/skeleton";

export default function GenomeBrowserView({ selectedGeneSymbol }: { selectedGeneSymbol: string | null }) {
  const [geneData, setGeneData] = useState<Gene | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!selectedGeneSymbol) {
      setGeneData(null);
      return;
    }
    
    const fetchData = async () => {
      setIsLoading(true);
      const data = await getGeneByName(selectedGeneSymbol);
      setGeneData(data);
      setIsLoading(false);
    };

    fetchData();
  }, [selectedGeneSymbol]);

  return (
    <div className="p-6">
      <Tabs defaultValue="chromosome-list" className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-4">
          <TabsTrigger value="detailed-view">Detailed View</TabsTrigger>
          <TabsTrigger value="chromosome-list">Chromosome List</TabsTrigger>
        </TabsList>

        <TabsContent value="detailed-view">
          {isLoading && <Skeleton className="w-full h-48" />}
          {geneData && geneData.chromosome ? (
            <ChromosomeVisualizer gene={geneData} chromosome={geneData.chromosome} />
          ) : (
            !isLoading && <p className="text-center text-muted-foreground py-8">Select a gene to see its visualization.</p>
          )}
        </TabsContent>

        <TabsContent value="chromosome-list">
          <ChromosomeTable />
        </TabsContent>
      </Tabs>
    </div>
  );
}