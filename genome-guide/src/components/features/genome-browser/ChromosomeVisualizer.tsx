"use client";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Gene, Chromosome } from "@/services/genomeApi";

type ChromosomeVisualizerProps = {
  gene: Gene;
  chromosome: Chromosome;
};

export default function ChromosomeVisualizer({ gene, chromosome }: ChromosomeVisualizerProps) {
  // Calculate the position and width of the gene on the chromosome as percentages
  const geneStartPercent = (gene.start_pos / chromosome.length) * 100;
  const geneWidthPercent = ((gene.end_pos - gene.start_pos) / chromosome.length) * 100;

  // Ensure very small genes have a minimum visual width for the marker line
  const displayWidth = Math.max(geneWidthPercent, 0.2);
  // Center position for the callout line
  const geneCenterPercent = geneStartPercent + (geneWidthPercent / 2);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{gene.gene_name || gene.gene_id}</CardTitle>
        <CardDescription>
          Visual location on {chromosome.name}
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-8">
        <div className="relative">
          
          {/* Lollipop/Callout for the Gene Label */}
          <div 
            className="absolute bottom-full mb-2" 
            style={{ left: `${geneCenterPercent}%`, transform: 'translateX(-50%)' }}
          >
            <div className="bg-card border shadow-sm rounded-md px-2 py-1 text-xs font-semibold whitespace-nowrap">
              {gene.gene_name}
            </div>
            {/* The stick of the lollipop */}
            <div className="h-2 w-px bg-foreground mx-auto" />
          </div>

          {/* The Chromosome Bar */}
          <div className="relative h-4 bg-gradient-to-b from-muted via-background to-muted rounded-full border">
            
            {/* Centromere */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-5 w-2 bg-background border rounded-full" />
            
            {/* The Gene Marker on the chromosome */}
            <div
              className="absolute h-4 bg-primary rounded-full opacity-75"
              style={{
                left: `${geneStartPercent}%`,
                width: `${displayWidth}%`,
              }}
              title={`Gene: ${gene.gene_name}`}
            />
          </div>
          
          {/* Scale Markers */}
          <div className="relative mt-2 flex justify-between text-xs text-muted-foreground">
            <span>0 bp</span>
            <span>{chromosome.length.toLocaleString()} bp</span>
          </div>

        </div>
      </CardContent>
    </Card>
  );
}