"use client";
import { useState, useEffect } from "react";
import { getChromosomes, Chromosome } from "@/services/genomeApi";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export default function KaryotypeView() {
  const [chromosomes, setChromosomes] = useState<Chromosome[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // ... (The data fetching and sorting logic from before remains the same)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const allChromos = await getChromosomes();
        const primaryChromos = allChromos.filter(c => !c.name.includes('_'));
        const maxLength = Math.max(...primaryChromos.map(c => c.length));
        
        primaryChromos.sort((a, b) => {
            const aName = a.name.replace('chr', '');
            const bName = b.name.replace('chr', '');
            const aIsNumeric = !isNaN(parseInt(aName));
            const bIsNumeric = !isNaN(parseInt(bName));
            if (aIsNumeric && bIsNumeric) return parseInt(aName) - parseInt(bName);
            if (aIsNumeric) return -1;
            if (bIsNumeric) return 1;
            return aName.localeCompare(bName);
        });

        const scaledChromos = primaryChromos.map(c => ({ ...c, scale: (c.length / maxLength) * 100 }));
        setChromosomes(scaledChromos as any);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) {
    // ... (Skeleton loading state remains the same)
  }

  return (
    <TooltipProvider delayDuration={100}>
      <div className="group flex justify-center items-end gap-2 h-48 p-4 bg-[radial-gradient(var(--muted)_1px,transparent_1px)] [background-size:16px_16px]">
        {chromosomes.map((chromo) => {
          const colorClass = 
              chromo.name === 'chrX' ? 'bg-pink-400/80 hover:bg-pink-400' : 
              chromo.name === 'chrY' ? 'bg-sky-400/80 hover:bg-sky-400' : 
              'bg-slate-400/80 dark:bg-slate-600/80 hover:bg-slate-400 dark:hover:bg-slate-500';

          return (
            <Tooltip key={chromo.id}>
              <TooltipTrigger asChild>
                <div
                  className="relative h-full w-full flex flex-col items-center justify-end cursor-pointer transition-opacity duration-300 group-hover:opacity-50 hover:!opacity-100"
                >
                  <div 
                    className={cn("w-full rounded-t-sm transition-all duration-300 ease-in-out group-hover:scale-105", colorClass)}
                    style={{ height: `${chromo.scale}%` }}
                  />
                  <div className="mt-1 text-xs font-mono text-muted-foreground transition-colors group-hover:text-foreground">
                    {chromo.name.replace('chr', '')}
                  </div>
                </div>
              </TooltipTrigger>
              <TooltipContent>
                <p className="font-bold">{chromo.name}</p>
                <p>{chromo.length.toLocaleString()} bp</p>
              </TooltipContent>
            </Tooltip>
          );
        })}
      </div>
    </TooltipProvider>
  );
}