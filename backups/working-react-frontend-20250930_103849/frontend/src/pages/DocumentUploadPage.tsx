import { Link } from 'react-router-dom';

const DocumentUploadPage = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>      
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
        padding: '40px',
        textAlign: 'center',
        border: '2px dashed #e2e8f0'
      }}>
        <h2>Document Upload Coming Soon</h2>
        <p>This page will contain the document upload functionality.</p>
        <Link to="/library" style={{ color: '#3b82f6' }}>Go to Library</Link>
      </div>
    </div>
  );
};

export default DocumentUploadPage;