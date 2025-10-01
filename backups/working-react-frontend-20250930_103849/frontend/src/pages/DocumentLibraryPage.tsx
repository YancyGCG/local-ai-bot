import { Link } from 'react-router-dom';
import { useDocuments } from '../hooks/useDocuments';
import { useOllamaStatus } from '../hooks/useOllamaStatus';

const DocumentLibraryPage = () => {
  const { data: documentsData, isLoading } = useDocuments();
  const { data: status } = useOllamaStatus();
  const documents = documentsData?.documents || [];

  if (isLoading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>Loading documents...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <header style={{ 
        background: 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
        color: 'white',
        padding: '40px',
        borderRadius: '12px',
        marginBottom: '30px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '2.5rem', fontWeight: 'bold' }}>
            Document Library
          </h1>
          <p style={{ margin: '10px 0 0 0', fontSize: '1.1rem', opacity: 0.9 }}>
            Manage your processed documents and MTL templates
          </p>
        </div>
        <Link 
          to="/"
          style={{ 
            background: 'rgba(255,255,255,0.2)',
            color: 'white',
            padding: '12px 24px',
            borderRadius: '8px',
            textDecoration: 'none',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.3)'}
          onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
        >
          Back to Home
        </Link>
      </header>

      {/* Ollama Status */}
      <div style={{ 
        background: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        padding: '20px',
        marginBottom: '30px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h3 style={{ margin: '0 0 5px 0', color: '#1e293b' }}>Ollama Status</h3>
          <span style={{ 
            color: status?.ollama_status?.includes('✅') ? '#10b981' : '#ef4444',
            fontWeight: 'bold'
          }}>
            {status?.ollama_status || '❌ Not available'}
          </span>
          {status?.models && (
            <span style={{ marginLeft: '20px', color: '#64748b' }}>
              Models loaded: {status.models.length}
            </span>
          )}
        </div>
        <Link 
          to="/upload"
          style={{ 
            background: '#3b82f6',
            color: 'white',
            padding: '12px 24px',
            borderRadius: '8px',
            textDecoration: 'none',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = '#2563eb'}
          onMouseLeave={(e) => e.currentTarget.style.background = '#3b82f6'}
        >
          Upload Document
        </Link>
      </div>

      {/* Documents Grid */}
      <div>
        <h2 style={{ marginBottom: '20px', color: '#1e293b' }}>
          Your Documents ({documents.length})
        </h2>
        
        {documents.length === 0 ? (
          <div style={{ 
            textAlign: 'center',
            padding: '60px 20px',
            background: '#f8fafc',
            borderRadius: '12px',
            border: '2px dashed #e2e8f0'
          }}>
            <p style={{ fontSize: '1.1rem', color: '#64748b', marginBottom: '20px' }}>
              No documents uploaded yet
            </p>
            <Link 
              to="/upload"
              style={{ 
                background: '#3b82f6',
                color: 'white',
                padding: '14px 28px',
                borderRadius: '8px',
                textDecoration: 'none',
                fontSize: '1rem',
                fontWeight: '600'
              }}
            >
              Upload Your First Document
            </Link>
          </div>
        ) : (
          <div style={{ 
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '20px'
          }}>
            {documents.map((doc) => (
              <div
                key={doc.id}
                style={{
                  background: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '12px',
                  padding: '24px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  transition: 'transform 0.2s, box-shadow 0.2s'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0px)';
                  e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
                }}
              >
                <h3 style={{ 
                  margin: '0 0 12px 0',
                  color: '#1e293b',
                  fontSize: '1.1rem',
                  fontWeight: '600',
                  lineHeight: '1.4'
                }}>
                  {doc.filename}
                </h3>
                
                <div style={{ marginBottom: '16px' }}>
                  <p style={{ 
                    margin: '0 0 8px 0',
                    color: '#64748b',
                    fontSize: '0.875rem'
                  }}>
                    Processed: {new Date(doc.processed_at).toLocaleDateString()}
                  </p>
                  
                  {doc.metadata && (
                    <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
                      {doc.metadata.pages && (
                        <span style={{ marginRight: '12px' }}>
                          📄 {doc.metadata.pages} pages
                        </span>
                      )}
                      {doc.metadata.word_count && (
                        <span style={{ marginRight: '12px' }}>
                          📝 {doc.metadata.word_count.toLocaleString()} words
                        </span>
                      )}
                      {doc.metadata.chunks_count && (
                        <span>
                          🔗 {doc.metadata.chunks_count} chunks
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div style={{ 
                  display: 'flex',
                  gap: '8px',
                  flexWrap: 'wrap'
                }}>
                  <Link
                    to={`/edit/${doc.id}`}
                    style={{
                      background: '#10b981',
                      color: 'white',
                      padding: '8px 16px',
                      borderRadius: '6px',
                      textDecoration: 'none',
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#059669'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#10b981'}
                  >
                    ✏️ Edit MTL
                  </Link>
                  
                  <a
                    href={`/data/processed/${doc.id}.json`}
                    download={`${doc.filename.replace(/\.[^/.]+$/, '')}_MTL.json`}
                    style={{
                      background: '#6366f1',
                      color: 'white',
                      padding: '8px 16px',
                      borderRadius: '6px',
                      textDecoration: 'none',
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#4f46e5'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#6366f1'}
                  >
                    ⬇️ Download JSON
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentLibraryPage;
