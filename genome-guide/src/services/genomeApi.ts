// Define the Chromosome type here so it can be reused
export type Chromosome = {
  id: number;
  name: string;
  length: number;
};

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function getChromosomes(): Promise<Chromosome[]> {
  const response = await fetch(`${API_BASE_URL}/chromosomes/`);

  if (!response.ok) {
    // You can add more sophisticated error handling here
    throw new Error("Failed to fetch chromosomes from the server.");
  }

  const data: Chromosome[] = await response.json();
  return data;
}

// You can add all your other API calls here later
// export async function searchGenes(query: string) { ... }
// export async function getGeneInfo(symbol: string) { ... }