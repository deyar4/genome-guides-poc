"use client";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ChromosomeTable } from "@/components/features/genome-browser/ChromosomeTable";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function GenomeBrowserView() {
  return (
    <div className="p-6">
      <Tabs defaultValue="chromosome-list" className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-4">
          <TabsTrigger value="detailed-view">Detailed View</TabsTrigger>
          <TabsTrigger value="chromosome-list">Chromosome List</TabsTrigger>
        </TabsList>

        <TabsContent value="detailed-view">
          <Card>
            <CardHeader>
              <CardTitle>Detailed Gene Visualization</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">The interactive gene and chromosome visualization will be built here.</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="chromosome-list">
          <ChromosomeTable />
        </TabsContent>
      </Tabs>
    </div>
  );
}