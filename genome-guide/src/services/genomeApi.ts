export type Gene = {
  id: number;
  gene_id: string;
  gene_name: string | null;
  start_pos: number;
  end_pos: number;
  strand: string;
  // This line has changed
  chromosome: { name: string }; // It's now an object with a name property
};

export type Chromosome = {
  id: number;
  name: string;
  length: number;
};

// The Base URL should NOT include /api/v1
const API_BASE_URL = "http://127.0.0.1:8000";

// Each function will add the correct, full path.

export async function getChromosomes(): Promise<Chromosome[]> {
  // Add "?limit=500" to the end of the URL to request more items
  const response = await fetch(`${API_BASE_URL}/api/v1/chromosomes/?limit=500`);
  
  if (!response.ok) {
    throw new Error("Failed to fetch chromosomes.");
  }
  return response.json();
}

export async function searchGenes(query: string): Promise<Gene[]> {
  if (!query) return [];
  const response = await fetch(`${API_BASE_URL}/api/v1/genes/search/${query}`);
  if (response.status === 404) return []; // It's okay if no genes are found
  if (!response.ok) {
    throw new Error("Failed to search for genes.");
  }
  return response.json();
}

// Add the function for fetching a single gene by its exact name
export async function getGeneByName(name: string): Promise<Gene | null> {
  const response = await fetch(`${API_BASE_URL}/api/v1/genes/${name}`);
  if (!response.ok) return null; // It's okay if a single gene isn't found
  return response.json();
}