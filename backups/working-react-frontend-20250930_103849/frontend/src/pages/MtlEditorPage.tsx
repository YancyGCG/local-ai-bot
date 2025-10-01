import { useEffect, useMemo, useRef, useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';

import { useDocumentDetail } from '../hooks/useDocumentDetail';
import { useJsonTemplate } from '../hooks/useJsonTemplate';
import { toast } from '../ui/toast';
import { apiClient } from '../lib/apiClient';
import SimpleMtlEditor from '../components/mtl/SimpleMtlEditor';
import type { RegenerateResponse } from '../types/api';
import { sanitizeMtlTemplate } from '../utils/sanitizeMtlTemplate';

export type ValidationMessage = {
  path: string;
  message: string;
};

const MtlEditorPage = () => {
  const { documentId } = useParams();
  const { data: documentDetail, isLoading: loadingSummary } = useDocumentDetail(documentId);
  const {
    data: template,
    isLoading: loadingTemplate,
    refetch: refetchTemplate
  } = useJsonTemplate(documentId);
  const [loadedTemplate, setLoadedTemplate] = useState<Record<string, unknown> | null>(null);
  const [isValid, setIsValid] = useState(true);
  const [hasUserEdited, setHasUserEdited] = useState(false);
  const editorValueRef = useRef<Record<string, unknown> | null>(null);
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const templateError = useMemo(() => {
    if (hasUserEdited) {
      return null;
    }
    if (!template) {
      return null;
    }
    const rawError = (template as Record<string, unknown>).error;
    if (typeof rawError === 'string') {
      return rawError;
    }
    if (rawError && typeof rawError === 'object') {
      try {
        return JSON.stringify(rawError, null, 2);
      } catch (error) {
        return String(rawError);
      }
    }
    return null;
  }, [template, hasUserEdited]);

  useEffect(() => {
    if (!template) {
      return;
    }
    const sanitized = sanitizeMtlTemplate(template);
    setLoadedTemplate(sanitized);
    editorValueRef.current = sanitized;
    setIsValid(true);
    setHasUserEdited(false);
  }, [template]);

  const saveMutation = useMutation({
    mutationFn: async (payload: Record<string, unknown>) => {
      await apiClient.put(`/documents/${documentId}`, { json: payload });
      return payload;
    },
    onSuccess: () => {
      toast.success('MTL template saved');
      queryClient.invalidateQueries({ queryKey: ['json-template', documentId] });
    },
    onError: () => {
      toast.error('Failed to save template');
    }
  });

  // Autosave & optimistic undo support
  const autoSaveTimerRef = useRef<number | null>(null);
  const undoTimerRef = useRef<number | null>(null);
  const previousSavedRef = useRef<Record<string, unknown> | null>(null);
  const [autoSavePending, setAutoSavePending] = useState(false);
  const [autoSaving, setAutoSaving] = useState(false);
  const [lastSavedAt, setLastSavedAt] = useState<Date | null>(null);
  const [undoAvailable, setUndoAvailable] = useState(false);

  const [autosaveEnabled, setAutosaveEnabled] = useState<boolean>(() => {
    try {
      const raw = window.localStorage.getItem('mtl-autosave-enabled');
      return raw === null ? true : raw === '1';
    } catch {
      return true;
    }
  });
  const [autosaveIntervalSecs, setAutosaveIntervalSecs] = useState<number>(() => {
    try {
      const raw = window.localStorage.getItem('mtl-autosave-interval');
      return raw ? Number(raw) : 2;
    } catch {
      return 2;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem('mtl-autosave-enabled', autosaveEnabled ? '1' : '0');
      window.localStorage.setItem('mtl-autosave-interval', String(autosaveIntervalSecs));
    } catch {
      // noop
    }
  }, [autosaveEnabled, autosaveIntervalSecs]);

  const scheduleAutoSave = useCallback(() => {
    // Do nothing if autosave disabled
    if (!autosaveEnabled) {
      setAutoSavePending(false);
      if (autoSaveTimerRef.current) {
        window.clearTimeout(autoSaveTimerRef.current);
        autoSaveTimerRef.current = null;
      }
      return;
    }

    // Do not schedule autosave when template has an error or JSON invalid
    if (templateError || !isValid) {
      setAutoSavePending(false);
      if (autoSaveTimerRef.current) {
        window.clearTimeout(autoSaveTimerRef.current);
        autoSaveTimerRef.current = null;
      }
      return;
    }

    setAutoSavePending(true);
    if (autoSaveTimerRef.current) {
      window.clearTimeout(autoSaveTimerRef.current);
    }
    autoSaveTimerRef.current = window.setTimeout(() => {
      autoSaveTimerRef.current = null;
      const currentValue = editorValueRef.current;
      if (!currentValue || !isValid) {
        setAutoSavePending(false);
        return;
      }

      // Save snapshot for undo (optimistic)
      previousSavedRef.current = JSON.parse(JSON.stringify(currentValue));
      setAutoSavePending(false);
      setAutoSaving(true);
      setUndoAvailable(false);

      saveMutation.mutate(currentValue, {
        onSuccess: () => {
          setLastSavedAt(new Date());
          setHasUserEdited(false);
          setAutoSaving(false);
          // Make undo available for a short window
          setUndoAvailable(true);
          if (undoTimerRef.current) {
            window.clearTimeout(undoTimerRef.current);
          }
          undoTimerRef.current = window.setTimeout(() => {
            setUndoAvailable(false);
            undoTimerRef.current = null;
            previousSavedRef.current = null;
          }, 12_000);
        },
        onError: () => {
          // on error, keep previous snapshot so user can try undo/restore
          setAutoSaving(false);
        }
      });
    }, autosaveIntervalSecs * 1000);
  }, [autosaveEnabled, autosaveIntervalSecs, templateError, isValid, saveMutation]);

  const handleUndo = useCallback(() => {
    if (!previousSavedRef.current) return;
    const toRestore = JSON.parse(JSON.stringify(previousSavedRef.current));
    editorValueRef.current = toRestore;
    setHasUserEdited(true);
    setUndoAvailable(false);
    // Immediately persist the restored value
    setAutoSaving(true);
    saveMutation.mutate(toRestore, {
      onSuccess: () => {
        setLastSavedAt(new Date());
        setAutoSaving(false);
        toast.success('Reverted to previous saved version');
      },
      onError: () => {
        setAutoSaving(false);
        toast.error('Failed to revert to previous version');
      }
    });
    if (undoTimerRef.current) {
      window.clearTimeout(undoTimerRef.current);
      undoTimerRef.current = null;
    }
    previousSavedRef.current = null;
  }, [saveMutation]);

  // Cleanup timers
  useEffect(() => {
    return () => {
      if (autoSaveTimerRef.current) {
        window.clearTimeout(autoSaveTimerRef.current);
      }
      if (undoTimerRef.current) {
        window.clearTimeout(undoTimerRef.current);
      }
    };
  }, []);

  const regenerateMutation = useMutation({
    mutationFn: async () => {
      if (!documentId) {
        throw new Error('Document id missing');
      }
      const response = await apiClient.post<RegenerateResponse>(`/api/documents/${documentId}/regenerate`);
      return response.data;
    },
    onSuccess: async (payload) => {
      if (!payload.success || !payload.json_template) {
        toast.error(payload.error || 'Failed to regenerate template');
        return;
      }
      const sanitized = sanitizeMtlTemplate(payload.json_template);
      setLoadedTemplate(sanitized);
      editorValueRef.current = sanitized;
      setHasUserEdited(false);
      setIsValid(true);
      toast.success('Fresh AI template ready');
      await refetchTemplate();
    },
    onError: () => {
      toast.error('Failed to regenerate template');
    }
  });

  const generateMutation = useMutation({
    mutationFn: async (payload: Record<string, unknown>) => {
      const response = await apiClient.post('/api/generate-mtl', { json: payload }, { responseType: 'blob' });
      return response.data as Blob;
    },
    onSuccess: (blob) => {
      const url = URL.createObjectURL(blob);
      const anchor = window.document.createElement('a');
      anchor.href = url;
      anchor.download = `${documentDetail?.filename ?? 'MTL'}-Generated.docx`;
      anchor.click();
      URL.revokeObjectURL(url);
      toast.success('MTL downloaded');
    },
    onError: () => {
      toast.error('Failed to generate DOCX');
    }
  });

  const handleGenerate = () => {
    const currentValue = editorValueRef.current;
    if (!currentValue || !isValid) {
      toast.error('JSON is invalid');
      return;
    }
    generateMutation.mutate(currentValue);
  };

  if (loadingSummary || loadingTemplate) {
    return <p>Loading MTL editor…</p>;
  }

  if (!documentId || !documentDetail || !template) {
    return <p>Template not found.</p>;
  }

  const handleSave = () => {
    const currentValue = editorValueRef.current;
    if (!currentValue || !isValid) {
      toast.error('JSON is invalid');
      return;
    }
    saveMutation.mutate(currentValue);
  };



  const resetToServer = async () => {
    setHasUserEdited(false);
    setLoadedTemplate(null);
    editorValueRef.current = null;
    await refetchTemplate();
  };

  return (


      <section style={{ display: 'flex', gap: '16px', flex: 1, minHeight: 0 }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          {templateError && !hasUserEdited ? (
            <div
              style={{
                height: '100%',
                minHeight: '480px',
                borderRadius: '12px',
                border: '1px solid rgba(248,113,113,0.35)',
                background: 'rgba(248,113,113,0.12)',
                padding: '24px',
                display: 'flex',
                flexDirection: 'column',
                gap: '16px'
              }}
            >
              <div>
                <h3 style={{ margin: 0, color: '#fecaca' }}>MTL generation failed</h3>
                <p style={{ color: 'rgba(255,255,255,0.75)', marginTop: '8px' }}>
                  The AI returned an error instead of a template. Regenerate the JSON or edit manually below once a template is available.
                </p>
              </div>
              <div style={{ display: 'flex', gap: '12px' }}>
                <button
                  type="button"
                  onClick={() => regenerateMutation.mutate()}
                  disabled={regenerateMutation.isPending}
                >
                  {regenerateMutation.isPending ? 'Regenerating…' : 'Regenerate with AI'}
                </button>
                <button
                  type="button"
                  onClick={() => resetToServer()}
                  disabled={regenerateMutation.isPending}
                >
                  Reload saved JSON
                </button>
              </div>
              <pre
                style={{
                  flex: 1,
                  overflow: 'auto',
                  background: 'rgba(15,23,42,0.85)',
                  borderRadius: '8px',
                  padding: '16px',
                  border: '1px solid rgba(248,113,113,0.25)',
                  color: '#fca5a5'
                }}
              >
                {templateError}
              </pre>
              <small style={{ color: 'rgba(255,255,255,0.55)' }}>
                Tip: pull the required models from the sidebar first, then regenerate.
              </small>
            </div>
          ) : (
            <SimpleMtlEditor
              value={loadedTemplate ?? undefined}
              onChange={(json) => {
                editorValueRef.current = json;
                setHasUserEdited(true);
                // schedule autosave after each change
                scheduleAutoSave();
              }}
              onValidationChange={(valid) => {
                setIsValid(valid);
                // If validation toggles to valid, schedule autosave for new valid state
                if (valid) {
                  scheduleAutoSave();
                }
              }}
            />
          )}
        </div>
        <aside style={{ width: '280px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginTop: '8px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'rgba(255,255,255,0.8)' }}>
              <input
                type="checkbox"
                checked={autosaveEnabled}
                onChange={(e) => setAutosaveEnabled(e.target.checked)}
              />
              Autosave
            </label>
            <label style={{ color: 'rgba(255,255,255,0.7)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              Interval
              <input
                type="number"
                min={1}
                value={autosaveIntervalSecs}
                onChange={(e) => setAutosaveIntervalSecs(Math.max(1, Number(e.target.value) || 1))}
                style={{ width: '68px', padding: '6px 8px', borderRadius: '6px', border: '1px solid rgba(148,163,184,0.2)', background: 'rgba(15,23,42,0.05)', color: 'rgba(226,232,240,0.9)' }}
              />
              s
            </label>
          </div>

          <div style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.8)', marginTop: '8px' }}>
            {autoSavePending ? (
              <div>Autosave pending…</div>
            ) : autoSaving ? (
              <div>Autosaving…</div>
            ) : lastSavedAt ? (
              <div>Last saved: {lastSavedAt.toLocaleString()}</div>
            ) : (
              <div>Not saved yet</div>
            )}
            {undoAvailable && (
              <div style={{ marginTop: '8px' }}>
                <button type="button" onClick={handleUndo} style={{ padding: '6px 10px', borderRadius: '6px', background: 'rgba(148,163,184,0.12)', color: '#e2e8f0' }}>Undo save</button>
              </div>
            )}
          </div>
        </aside>
      </section>

      <footer style={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.85rem' }}>
        Document metadata: {JSON.stringify(documentDetail.metadata)}
      </footer>
    </div>
  );
};

export default MtlEditorPage;