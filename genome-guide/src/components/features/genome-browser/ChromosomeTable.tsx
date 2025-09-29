"use client";
import { useEffect, useState, useMemo } from "react"; // 1. Import useMemo
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

  // 2. Create a new, filtered list using useMemo
  const filteredChromosomes = useMemo(() => {
    // This keeps only the chromosomes that DO NOT include an underscore "_"
    return chromosomes.filter(chromo => !chromo.name.includes('_'));
  }, [chromosomes]); // This recalculates only when the 'chromosomes' state changes

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
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead className="text-right">Length (base pairs)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {/* 3. Map over the new 'filteredChromosomes' list */}
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
        )}
      </CardContent>
    </Card>
  );
}