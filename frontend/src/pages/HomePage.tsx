import { Link } from 'react-router-dom';
import { useDocuments } from '../hooks/useDocuments';
import { useOllamaStatus } from '../hooks/useOllamaStatus';

const HomePage = () => {
  const { data: documents } = useDocuments();
  const { data: status } = useOllamaStatus();

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
            Local AI Workbench
          </h1>
          <p style={{ margin: '10px 0 0 0', fontSize: '1.1rem', opacity: 0.9 }}>
            Confidential MTL & Test Generation
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
      <div>

      {/* Navigation Cards */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '20px',
        marginBottom: '30px'
      }}>
        <Link 
          to="/upload" 
          style={{ 
            textDecoration: 'none',
            background: '#3b82f6',
            color: 'white',
            padding: '30px',
            borderRadius: '12px',
            display: 'block',
            transition: 'transform 0.2s',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0px)'}
        >
          <h3 style={{ margin: '0 0 10px 0', fontSize: '1.3rem' }}>Upload & Process</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Upload documents and generate MTL templates</p>
        </Link>

        <Link 
          to="/library" 
          style={{ 
            textDecoration: 'none',
            background: '#10b981',
            color: 'white',
            padding: '30px',
            borderRadius: '12px',
            display: 'block',
            transition: 'transform 0.2s',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0px)'}
        >
          <h3 style={{ margin: '0 0 10px 0', fontSize: '1.3rem' }}>Document Library</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>
            View and edit your processed documents ({documents?.documents?.length || 0} documents)
          </p>
        </Link>
      </div>

      {/* Status Panel */}
      <div style={{ 
        background: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        padding: '20px'
      }}>
        <h3 style={{ margin: '0 0 15px 0', color: '#1e293b' }}>Ollama Status</h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
          <span style={{ 
            color: status?.ollama_status?.includes('✅') ? '#10b981' : '#ef4444',
            fontWeight: 'bold'
          }}>
            {status?.ollama_status || '❌ Not available'}
          </span>
        </div>
        {status?.models && status.models.length > 0 && (
          <details style={{ marginTop: '10px' }}>
            <summary style={{ cursor: 'pointer', color: '#64748b' }}>
              Models loaded: {status.models.length}
            </summary>
            <ul style={{ marginTop: '10px', paddingLeft: '20px' }}>
              {status.models.map((model: string) => (
                <li key={model} style={{ color: '#475569', marginBottom: '5px' }}>
                  {model}
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
      </div>
    </div>
  );
};

export default HomePage;
