// src/lib/api.ts
const API_BASE = "http://localhost:8000";

export async function getGene(symbol: string) {
  const response = await fetch(`${API_BASE}/genes/${symbol}`);
  if (!response.ok) {
    throw new Error('Failed to fetch gene data');
  }
  return response.json();
}

export async function searchGenes(query: string) {
  const response = await fetch(`${API_BASE}/genes/search/${query}`);
  if (!response.ok) {
    throw new Error('Failed to search genes');
  }
  return response.json();
}