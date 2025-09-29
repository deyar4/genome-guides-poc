"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// A simple placeholder for the gene info panel for now
const GeneInfoCard = () => (
  <Card>
    <CardHeader>
      <CardTitle>Gene Information</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-muted-foreground">Select a gene to see details here.</p>
    </CardContent>
  </Card>
);

const StatsCard = () => (
    <Card>
        <CardHeader><CardTitle>Genome Statistics</CardTitle></CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
            <div className="bg-muted p-4 rounded-lg text-center">
                <p className="text-sm text-muted-foreground">Chromosomes</p>
                <p className="text-2xl font-bold">24</p>
            </div>
            <div className="bg-muted p-4 rounded-lg text-center">
                <p className="text-sm text-muted-foreground">Base Pairs</p>
                <p className="text-2xl font-bold">3.2B</p>
            </div>
        </CardContent>
    </Card>
);

export default function DashboardView() {
  return (
    <div className="p-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Column */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Welcome to Genome Guides</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Use the sidebar to navigate through the application. Start by exploring the Genome Browser.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Right Sidebar Column */}
        <div className="space-y-6">
          <GeneInfoCard />
          <StatsCard />
        </div>
      </div>
    </div>
  );
}