import React, { useState, useEffect } from 'react';
import { Box, CssBaseline, AppBar, Toolbar, Typography, Container } from '@mui/material';
import axios from 'axios';
import './App.css';

// Import your existing components
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

type BackendStatus = 'checking' | 'connected' | 'error' | 'disconnected';
type PageType = 'home' | 'library' | 'teleconsultation' | 'profile';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<PageType>('home');
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('checking');

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/health');
        setBackendStatus(response.data.status === 'ok' ? 'connected' : 'error');
      } catch (err) {
        console.error('Backend health check failed:', err);
        setBackendStatus('disconnected');
      }
    };
    
    checkBackendHealth();
  }, []);

  const handleNavigate = (page: PageType) => {
    setCurrentPage(page);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            AI Health Diagnosis System
          </Typography>
          <Box sx={{ ml: 'auto', color: 'white' }}>
            Backend: {backendStatus}
          </Box>
        </Toolbar>
      </AppBar>
      
      <Sidebar onNavigate={(page: PageType) => handleNavigate(page)} />
      
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Container maxWidth="lg">
          <Dashboard page={currentPage} />
        </Container>
      </Box>
    </Box>
  );
};

export default App;