"use client"; // This marks the component as a Client Component

import { useEffect, useState } from "react";
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

// Define a TypeScript type for our chromosome data
type Chromosome = {
  id: number;
  name: string;
  length: number;
};

export function ChromosomeTable() {
  // State to store the chromosome data we fetch from the API
  const [chromosomes, setChromosomes] = useState<Chromosome[]>([]);
  // State to handle loading status
  const [isLoading, setIsLoading] = useState(true);
  // State to handle any potential errors
  const [error, setError] = useState<string | null>(null);

  // useEffect hook to fetch data when the component mounts
  useEffect(() => {
    async function fetchChromosomes() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/chromosomes/");
        if (!response.ok) {
          throw new Error("Failed to fetch data from the server.");
        }
        const data: Chromosome[] = await response.json();
        setChromosomes(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchChromosomes();
  }, []); // The empty array means this effect runs only once on mount

  return (
    <Card className="mt-8"> {/* Added margin-top for spacing */}
      <CardHeader>
        <CardTitle>Available Chromosomes</CardTitle>
        <CardDescription>
          A list of chromosomes retrieved from the Genome Guides API.
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
              {chromosomes.map((chromo) => (
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