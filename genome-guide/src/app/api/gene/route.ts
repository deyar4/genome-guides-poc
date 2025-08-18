import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const gene = searchParams.get('gene') || 'BRCA1';

  // Mock data - in real implementation, connect to UCSC/Ensembl APIs
  const geneData = {
    symbol: gene,
    name: `${gene} gene product`,
    description: "Tumor suppressor protein involved in DNA repair",
    location: "chr17:43,044,295-43,125,482",
    transcripts: 5,
    aliases: ["BRCA1", "BRCC1"],
    diseases: ["Breast cancer", "Ovarian cancer"]
  };

  return NextResponse.json(geneData);
}