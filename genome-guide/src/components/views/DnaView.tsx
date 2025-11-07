"use client";
import { useState, useEffect } from "react";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend } from "recharts";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { getChromosomes, Chromosome } from "@/services/genomeApi";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@radix-ui/react-tabs";
import { Skeleton } from "../ui/skeleton";
import ChromosomeVisualizer from "../features/genome-browser/ChromosomeVisualizer";
import { ChromosomeTable } from "../features/genome-browser/ChromosomeTable";

// New API function to get stats
async function getStatistic(statName: string) {
  const response = await fetch(`http://127.0.0.1:8000/api/v1/statistics/${statName}`);
  if (!response.ok) return null;
  const data = await response.json();
  return data.stat_value;
}


// A reusable Pie Chart component for base composition
const CompositionPieChart = ({ statName, title }: { statName: string, title: string }) => {
  const [data, setData] = useState<any>(null);
  const COLORS = { 'A': '#22c55e', 'C': '#3b82f6', 'G': '#f97316', 'T': '#ec4899', 'N': '#6b7280' };

  useEffect(() => {
    getStatistic(statName).then(statData => {
      if (statData) {
        const chartData = Object.entries(statData)
          .map(([name, value]) => ({ name, value }))
          .sort((a,b) => a.name.localeCompare(b.name)); // Sort A, C, G, T, N
        setData(chartData);
      }
    });
  }, [statName]);

  if (!data) return <p>Loading...</p>;

  const total = data.reduce((sum: number, entry: any) => sum + entry.value, 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{total.toLocaleString()} total bases</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
              {data.map((entry: any, index: number) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: number) => `${((value / total) * 100).toFixed(2)}%`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}


export default function DnaView({ selectedGeneSymbol }: { selectedGeneSymbol: string | null }) {
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
  // ... (The state and useEffect for the chromosome bar chart can remain the same)
  
  return (
    <div className="p-4 md:p-8 space-y-8">
      <h2 className="text-3xl font-bold tracking-tight">DNA & Chromosomes</h2>
      
      {/* New section for base composition */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <CompositionPieChart statName="nuclear_base_composition" title="What is the base composition of the Nuclear Genome?" />
        <CompositionPieChart statName="mitochondrial_base_composition" title="What is the base composition of the Mitochondrial Genome?" />
      </div>

      {/* The existing chromosome size chart */}
            <ChromosomeTable />

    </div>
  );
}