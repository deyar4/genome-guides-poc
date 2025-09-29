"use client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import GeneInfoPanel from "@/components/features/gene-info/GeneInfoPanel";
import KaryotypeView from "@/components/features/karyotype/KaryotypeView";

const StatsCard = () => (
    <Card>
        <CardHeader>
            <CardTitle>Genome Statistics</CardTitle>
            <CardDescription>Key metrics for the human genome (GRCh38)</CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
            <div className="text-center">
                <p className="text-2xl font-bold">24</p>
                <p className="text-sm text-muted-foreground">Chromosomes</p>
            </div>
            <div className="text-center">
                <p className="text-2xl font-bold">3.2B</p>
                <p className="text-sm text-muted-foreground">Base Pairs</p>
            </div>
        </CardContent>
    </Card>
);

export default function DashboardView({ selectedGeneSymbol }: { selectedGeneSymbol: string | null }) {
  return (
    // The main container with generous padding for a spacious feel
    <div className="p-4 md:p-8 lg:p-10">
      <div className="space-y-8">

        {/* This is the "Hero" section, just like the shadcn homepage */}
        <div className="p-6 md:p-10 lg:p-16 border rounded-lg bg-card text-center">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tighter">
            An Interactive Guide to the Human Genome
          </h1>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            Explore chromosomes, search for genes, and visualize genomic data in a clean, modern interface.
          </p>
        </div>

        {/* This is the main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <Card>
              <CardHeader>
                <CardTitle>Human Karyotype</CardTitle>
                <CardDescription>Proportional overview of human chromosomes.</CardDescription>
              </CardHeader>
              <CardContent>
                <KaryotypeView />
              </CardContent>
            </Card>
          </div>

          <div className="space-y-8">
            <GeneInfoPanel symbol={selectedGeneSymbol} />
            <StatsCard />
          </div>
        </div>
      </div>
    </div>
  );
}