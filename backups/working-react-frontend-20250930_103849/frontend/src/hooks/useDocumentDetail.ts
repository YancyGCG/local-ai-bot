import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../lib/apiClient';

export interface DocumentDetail {
  id: string;
  filename: string;
  content: string;
  metadata: Record<string, any>;
  chunks_count: number;
  processed_at: string;
}

export const useDocumentDetail = (documentId?: string) => {
  return useQuery({
    queryKey: ['document-detail', documentId],
    queryFn: async (): Promise<DocumentDetail> => {
      if (!documentId) throw new Error('Document ID required');
      const response = await apiClient.get(`/documents/${documentId}`);
      return response.data as DocumentDetail;
    },
    enabled: !!documentId,
  });
};