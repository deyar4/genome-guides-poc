"use client";
import { useEffect, useState, useMemo } from "react";
import { getChromosomes, Chromosome } from "@/services/genomeApi"; 
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function ChromosomeTable() {
  const [chromosomes, setChromosomes] = useState<Chromosome[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getChromosomes();
        setChromosomes(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredChromosomes = useMemo(() => {
    return chromosomes.filter(chromo => !chromo.name.includes('_'));
  }, [chromosomes]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Available Chromosomes</CardTitle>
        <CardDescription>
          A list of primary chromosomes retrieved from the Genome Guides API.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading && <p>Loading data...</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        {!isLoading && !error && (
          // 1. We wrap the table in a div with a fixed height and overflow
          <div className="relative h-72 w-full overflow-auto">
            <Table>
              <TableHeader className="sticky top-0 bg-card">
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead className="text-right">Length (base pairs)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredChromosomes.map((chromo) => (
                  <TableRow key={chromo.id}>
                    <TableCell className="font-medium">{chromo.name}</TableCell>
                    <TableCell className="text-right">
                      {chromo.length.toLocaleString()}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}