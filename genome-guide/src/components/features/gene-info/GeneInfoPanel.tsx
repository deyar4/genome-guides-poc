"use client";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect, useState } from "react";
import { getGeneByName, Gene } from "@/services/genomeApi";

const InfoRow = ({ label, value }: { label: string, value: React.ReactNode }) => (
  <div className="flex justify-between items-center text-sm py-2 border-b">
    <span className="text-muted-foreground">{label}</span>
    <span className="font-medium text-right">{value}</span>
  </div>
);

const GeneInfoPanelSkeleton = () => (
  <div className="space-y-3">
    <Skeleton className="h-4 w-1/4" />
    <Skeleton className="h-4 w-3/4" />
    <Skeleton className="h-4 w-full" />
    <Skeleton className="h-4 w-2/3" />
  </div>
);

export default function GeneInfoPanel({ symbol }: { symbol: string | null }) {
  const [geneData, setGeneData] = useState<Gene | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!symbol) {
      setGeneData(null);
      setIsLoading(false);
      return;
    }
    
    const fetchData = async () => {
      setIsLoading(true);
      const data = await getGeneByName(symbol);
      setGeneData(data);
      setIsLoading(false);
    };

    fetchData();
  }, [symbol]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Gene Information</CardTitle>
        <CardDescription>{symbol || "No gene selected"}</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <GeneInfoPanelSkeleton />
        ) : geneData ? (
          <div className="space-y-1">
            <InfoRow label="Symbol" value={<span className="font-bold text-primary">{geneData.gene_name}</span>} />
            <InfoRow label="ID" value={<span className="font-mono text-xs">{geneData.gene_id}</span>} />
            <InfoRow 
              label="Location" 
              value={`${geneData.chromosome.name}: ${geneData.start_pos.toLocaleString()}-${geneData.end_pos.toLocaleString()}`} 
            />
            <InfoRow 
              label="Strand" 
              value={<Badge variant={geneData.strand === '+' ? 'default' : 'secondary'}>{geneData.strand}</Badge>} 
            />
          </div>
        ) : (
          <p className="text-sm text-muted-foreground text-center py-4">
            {symbol ? `Data not found for ${symbol}.` : "Select a gene to see its details."}
          </p>
        )}
      </CardContent>
    </Card>
  );
}