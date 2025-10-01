import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../lib/apiClient';

export interface OllamaStatus {
  ollama_status: string;
  models: string[];
  processed_documents: number;
  api_status: string;
}

export const useOllamaStatus = () => {
  return useQuery({
    queryKey: ['ollama-status'],
    queryFn: async (): Promise<OllamaStatus> => {
      const response = await apiClient.get('/status');
      return response.data as OllamaStatus;
    },
    refetchInterval: 10000,
  });
};