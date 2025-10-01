import { FormEvent, useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';

import { apiClient } from '../lib/apiClient';
import { toast } from '../ui/toast';

const DocumentUploadPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<'idle' | 'processing' | 'complete' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{ docId: string; filename: string } | null>(null);
  const queryClient = useQueryClient();
  const progressTimerRef = useRef<number | null>(null);

  const stopProgressTimer = () => {
    if (progressTimerRef.current) {
      window.clearInterval(progressTimerRef.current);
      progressTimerRef.current = null;
    }
  };

  const startProgressTimer = () => {
    stopProgressTimer();
    setProgress(12);
    progressTimerRef.current = window.setInterval(() => {
      setProgress((current) => {
        if (current >= 90) {
          return current;
        }
        const next = current + Math.random() * 10;
        return next > 90 ? 90 : next;
      });
    }, 450);
  };

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const response = await apiClient.post('/api/process-document', formData);
      return response.data as { success: boolean; doc_id?: string; error?: string };
    },
    onMutate: () => {
      setStatus('processing');
      setError(null);
      setResult(null);
      startProgressTimer();
    },
    onSuccess: (data, file) => {
      if (!data.success || !data.doc_id) {
        setStatus('error');
        setProgress(0);
        setError(data.error || 'Processing failed.');
        toast.error(data.error || 'Failed to process document');
        return;
      }
      setStatus('complete');
      setProgress(100);
      setResult({ docId: data.doc_id, filename: file.name });
      toast.success('Document processed successfully');
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
    onError: (err) => {
      setStatus('error');
      setProgress(0);
      setError(err instanceof Error ? err.message : 'Failed to process document');
      toast.error('Failed to process document');
    },
    onSettled: () => {
      stopProgressTimer();
    }
  });

  useEffect(() => {
    return () => {
      stopProgressTimer();
    };
  }, []);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedFile) {
      toast.error('Choose a document to upload');
      return;
    }
    uploadMutation.mutate(selectedFile);
  };

  const statusLabel = (() => {
    switch (status) {
      case 'processing':
        return 'Processing document…';
      case 'complete':
        return 'Processing complete';
      case 'error':
        return 'Processing failed';
      default:
        return '';
    }
  })();

  return (
<div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>      
      <header style={{ 
        background: 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
        color: 'white',
        padding: '0px 10px 5px 10px',
        borderRadius: '12px',
        marginBottom: '10px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '2.5rem', fontWeight: 'bold' }}>
            Upload & Process
          </h1>
          <p style={{ margin: '10px 0 0 0', fontSize: '1.1rem', opacity: 0.9 }}>
            Upload documents and generate MTL templates
          </p>
        </div>
        <Link 
          to="/"
          style={{ 
            background: 'rgba(255,255,255,0.2)',
            color: 'white',
            padding: '12px 24px',
            borderRadius: '8px',
            textDecoration: 'none'
          }}
        >
          Back to Home
        </Link>
      </header>

      <div style={{ 
        background: 'white',
        borderRadius: '12px',
        padding: '32px',
        border: '1px solid #e2e8f0',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
      }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div style={{
            border: '2px dashed #cbd5f5',
            borderRadius: '12px',
            padding: '30px',
            textAlign: 'center',
            background: '#f8fafc'
          }}>
            <p style={{ margin: '0 0 16px 0', color: '#475569', fontSize: '1rem' }}>
              Drag and drop a document here, or click to browse.
            </p>
            <label
              htmlFor="file-input"
              style={{
                display: 'inline-block',
                padding: '12px 24px',
                background: '#3b82f6',
                color: 'white',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600
              }}
            >
              Choose File
            </label>
            <input
              id="file-input"
              type="file"
              accept=".pdf,.doc,.docx,.txt,.md"
              style={{ display: 'none' }}
              onChange={(event) => {
                const file = event.target.files?.[0] ?? null;
                setSelectedFile(file);
                setResult(null);
                setError(null);
                setProgress(0);
                setStatus('idle');
              }}
            />
            {selectedFile && (
              <p style={{ marginTop: '16px', color: '#1e293b', fontWeight: 500 }}>
                Selected: {selectedFile.name}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={!selectedFile || uploadMutation.isPending}
            style={{
              alignSelf: 'flex-start',
              background: '#10b981',
              color: 'white',
              padding: '12px 28px',
              borderRadius: '8px',
              border: 'none',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: !selectedFile || uploadMutation.isPending ? 'not-allowed' : 'pointer',
              opacity: !selectedFile || uploadMutation.isPending ? 0.65 : 1,
              transition: 'background 0.2s'
            }}
            onMouseEnter={(event) => {
              if (selectedFile && !uploadMutation.isPending) {
                event.currentTarget.style.background = '#059669';
              }
            }}
            onMouseLeave={(event) => {
              event.currentTarget.style.background = '#10b981';
            }}
          >
            {uploadMutation.isPending ? 'Processing…' : 'Process Document'}
          </button>
        </form>

        {status !== 'idle' && (
          <div style={{ marginTop: '24px' }}>
            <div style={{
              height: '10px',
              borderRadius: '999px',
              background: '#e2e8f0',
              overflow: 'hidden'
            }}>
              <div
                style={{
                  width: `${progress}%`,
                  background: status === 'error' ? '#ef4444' : '#3b82f6',
                  height: '100%',
                  transition: 'width 0.3s ease'
                }}
              />
            </div>
            {statusLabel && (
              <p style={{ marginTop: '12px', color: '#475569' }}>{statusLabel}</p>
            )}
            {error && (
              <p style={{ marginTop: '8px', color: '#ef4444' }}>{error}</p>
            )}
          </div>
        )}

        {result && (
          <div style={{
            marginTop: '32px',
            padding: '24px',
            borderRadius: '12px',
            border: '1px solid #bbf7d0',
            background: '#ecfdf5'
          }}>
            <h3 style={{ margin: '0 0 12px 0', color: '#047857' }}>Document ready!</h3>
            <p style={{ margin: '0 0 16px 0', color: '#065f46' }}>
              <strong>{result.filename}</strong> has been processed. You can now review and edit the generated MTL template.
            </p>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <Link
                to={`/edit/${result.docId}`}
                style={{
                  background: '#3b82f6',
                  color: 'white',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  fontWeight: 600
                }}
              >
                Go to Editor
              </Link>
              <Link
                to="/library"
                style={{
                  background: '#1e293b',
                  color: 'white',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  fontWeight: 600
                }}
              >
                View Library
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentUploadPage;