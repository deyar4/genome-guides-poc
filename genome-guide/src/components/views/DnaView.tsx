"use client";
import { useState, useEffect } from "react";
import { ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { getChromosomes, Chromosome, Gene, getGeneByName } from "@/services/genomeApi";
import { Skeleton } from "@/components/ui/skeleton";
import ChromosomeVisualizer from "@/components/features/genome-browser/ChromosomeVisualizer";
import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";

// --- API Helper Function ---
async function getStatistic(statName: string) {
  const response = await fetch(`http://127.0.0.1:8000/api/v1/statistics/${statName}`);
  if (!response.ok) return null;
  const data = await response.json();
  return data.stat_value;
}

// --- Reusable Stats Card ---
const ChromosomeStats = ({ chromo, perChromoStats, gcStats, cpgStats }: { chromo: Chromosome, perChromoStats: any, gcStats: any, cpgStats: any }) => {
  if (!perChromoStats || !gcStats || !cpgStats) return <Skeleton className="h-48 w-full" />;

  const gc = gcStats[chromo.name] || 0;
  const cpg = cpgStats[chromo.name] || 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{chromo.name} Statistics</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between">
          <span className="text-muted-foreground">Length</span>
          <span className="font-medium">{chromo.length.toLocaleString()} bp</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">GC-Content</span>
          <span className="font-medium">{gc.toFixed(2)}%</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">CpG Frequency</span>
          <span className="font-medium">{cpg.toFixed(4)}%</span>
        </div>
      </CardContent>
    </Card>
  );
};

// --- Reusable Pie Chart Card ---
const ChromosomePieChart = ({ perChromoStats, chromoName }: { perChromoStats: any, chromoName: string }) => {
  const COLORS = { 'A': '#22c55e', 'C': '#3b82f6', 'G': '#f97316', 'T': '#ec4899', 'N': '#6b7280' };
  
  if (!perChromoStats || !perChromoStats[chromoName]) {
    return <Skeleton className="w-full h-64" />;
  }
  
  const counts = perChromoStats[chromoName];
  const chartData = Object.entries(counts)
    .map(([name, value]) => ({ name, value }))
    .sort((a,b) => a.name.localeCompare(b.name));
  
  const total = chartData.reduce((sum, entry) => sum + (entry.value as number), 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Base Composition</CardTitle>
        <CardDescription>{total.toLocaleString()} total bases</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS]} />
              ))}
            </Pie>
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};


// --- The Main DNA View ---
export default function DnaView({ selectedGeneSymbol }: { selectedGeneSymbol: string | null }) {
  const [chromosomes, setChromosomes] =useState<Chromosome[]>([]);
  const [selectedChromo, setSelectedChromo] = useState<Chromosome | null>(null);
  
  // State for all our calculated stats
  const [perChromoStats, setPerChromoStats] = useState(null);
  const [gcStats, setGcStats] = useState(null);
  const [cpgStats, setCpgStats] = useState(null);
  
  const [geneData, setGeneData] = useState<Gene | null>(null);
  const [isLoadingGene, setIsLoadingGene] = useState(true);

  // 1. Fetch all data on load
  useEffect(() => {
    async function loadAllData() {
      const [chromoData, perChromo, gc, cpg] = await Promise.all([
        getChromosomes(),
        getStatistic("per_chromosome_composition"),
        getStatistic("gc_content_per_chromosome"),
        getStatistic("cpg_frequency_per_chromosome")
      ]);

      const primaryChromos = chromoData.filter(c => !c.name.includes('_')).sort((a, b) => a.id - b.id);
      setChromosomes(primaryChromos);
      setSelectedChromo(primaryChromos[0]); // Select chr1 by default
      setPerChromoStats(perChromo);
      setGcStats(gc);
      setCpgStats(cpg);
    }
    loadAllData();
  }, []);

  // 2. Fetch gene data when the selected gene changes
  useEffect(() => {
    if (!selectedGeneSymbol) {
      setGeneData(null);
      return;
    }
    setIsLoadingGene(true);
    getGeneByName(selectedGeneSymbol).then(data => {
      setGeneData(data);
    }).finally(() => setIsLoadingGene(false));
  }, [selectedGeneSymbol]);

  return (
    <div className="h-full grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4 md:p-8">
      
      {/* --- Left Column: Chromosome List --- */}
      <div className="md:col-span-1 lg:col-span-1">
        <h2 className="text-2xl font-bold tracking-tight mb-4">Chromosomes</h2>
        <ScrollArea className="h-[75vh] rounded-md border">
          <div className="p-4 space-y-2">
            {chromosomes.map(chromo => (
              <button
                key={chromo.id}
                onClick={() => setSelectedChromo(chromo)}
                className={cn(
                  "w-full text-left p-2 rounded-md transition-colors",
                  selectedChromo?.id === chromo.id
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted"
                )}
              >
                <div className="flex justify-between">
                  <span className="font-semibold">{chromo.name}</span>
                  <span className="text-xs opacity-70">{(chromo.length / 1_000_000).toFixed(0)} Mbp</span>
                </div>
              </button>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* --- Right Column: Data Panels --- */}
      <div className="md:col-span-2 lg:col-span-3 space-y-6">
        
        {/* Gene Visualizer Card */}
        <Card>
          <CardHeader>
            <CardTitle>Gene Visualizer</CardTitle>
            <CardDescription>Visual location of the selected gene ({selectedGeneSymbol || "none"})</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoadingGene && <Skeleton className="w-full h-48" />}
            {geneData && geneData.chromosome ? (
              <ChromosomeVisualizer gene={geneData} chromosome={geneData.chromosome} />
            ) : (
              !isLoadingGene && <div className="h-48 flex items-center justify-center"><p className="text-center text-muted-foreground">Select a gene from the header search to see its visualization.</p></div>
            )}
          </CardContent>
        </Card>
        
        {/* Grid for selected chromosome stats */}
        {selectedChromo && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChromosomeStats 
              chromo={selectedChromo}
              perChromoStats={perChromoStats}
              gcStats={gcStats}
              cpgStats={cpgStats}
            />
            <ChromosomePieChart 
              perChromoStats={perChromoStats}
              chromoName={selectedChromo.name}
            />
          </div>
        )}
      </div>
    </div>
  );
}