// File: ../services/catFactService.ts

import apiClient from './api-client';

// Define an interface for the response from the cat fact API.
interface CatFactResponse {
  fact: string;
  length: number;
}

// Function to fetch a single cat fact.
const getCatFact = async (): Promise<CatFactResponse> => {
  try {
    const response = await apiClient.get<CatFactResponse>('https://catfact.ninja/fact');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch cat fact: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

export default getCatFact;