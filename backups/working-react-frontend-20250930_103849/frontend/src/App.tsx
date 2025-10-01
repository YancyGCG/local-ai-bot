import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import HomePage from './pages/HomePage';
import DocumentLibraryPage from './pages/DocumentLibraryPage';
import DocumentUploadPage from './pages/DocumentUploadPage';
import MtlEditorPage from './pages/MtlEditorPage';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="app">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/library" element={<DocumentLibraryPage />} />
            <Route path="/upload" element={<DocumentUploadPage />} />
            <Route path="/edit/:documentId" element={<MtlEditorPage />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
