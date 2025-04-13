import React, { useState, useEffect } from 'react';
import { Box, CssBaseline, AppBar, Toolbar, Typography, Container, ThemeProvider, createTheme } from '@mui/material';
import axios from 'axios';
import './App.css';

import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import { Toaster } from './components/ui/toaster';
import { useToast } from './components/ui/use-toast';

type BackendStatus = 'checking' | 'connected' | 'error' | 'disconnected';
type PageType = 'home' | 'library' | 'teleconsultation' | 'profile';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<PageType>('home');
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('checking');
  const { toast } = useToast();

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/health');
        setBackendStatus(response.data.status === 'ok' ? 'connected' : 'error');
      } catch (err) {
        console.error('Backend health check failed:', err);
        setBackendStatus('disconnected');
        toast({
          title: 'Connection Error',
          description: 'Failed to connect to the backend server',
          variant: 'destructive',
        });
      }
    };
    
    checkBackendHealth();
    const interval = setInterval(checkBackendHealth, 30000);
    return () => clearInterval(interval);
  }, [toast]);

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <CssBaseline />
        
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              AI Health Diagnosis System
            </Typography>
            <Box sx={{ 
              ml: 'auto', 
              display: 'flex', 
              alignItems: 'center', 
              gap: 1 
            }}>
              <Box sx={{ 
                width: 10, 
                height: 10, 
                borderRadius: '50%', 
                backgroundColor: getStatusColor(backendStatus) 
              }} />
              <Typography variant="body2" sx={{ color: 'white' }}>
                {backendStatus.charAt(0).toUpperCase() + backendStatus.slice(1)}
              </Typography>
            </Box>
          </Toolbar>
        </AppBar>
        
        <Sidebar onNavigate={setCurrentPage} currentPage={currentPage} />
        
        <Box component="main" sx={{ 
          flexGrow: 1, 
          p: 3, 
          mt: 8,
          backgroundColor: 'background.default' 
        }}>
          <Container maxWidth="lg">
            <Dashboard currentPage={currentPage} />
          </Container>
        </Box>
      </Box>
      <Toaster />
    </ThemeProvider>
  );
};

export default App;