import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../lib/apiClient';

export interface Document {
  id: string;
  filename: string;
  processed_at: string;
  metadata: Record<string, any>;
}

export interface DocumentsResponse {
  documents: Document[];
}

export const useDocuments = () => {
  return useQuery({
    queryKey: ['documents'],
    queryFn: async (): Promise<DocumentsResponse> => {
      const response = await apiClient.get('/documents');
      return response.data as DocumentsResponse;
    },
    refetchInterval: 5000,
  });
};