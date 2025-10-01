import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../lib/apiClient';

export const useJsonTemplate = (documentId?: string) => {
  return useQuery({
    queryKey: ['json-template', documentId],
    queryFn: async (): Promise<Record<string, unknown>> => {
      if (!documentId) throw new Error('Document ID required');
      const response = await apiClient.get(`/data/processed/${documentId}.json`);
      return response.data as Record<string, unknown>;
    },
    enabled: !!documentId,
  });
};