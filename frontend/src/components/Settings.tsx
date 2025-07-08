import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  Alert,
  LinearProgress,
  Divider,
  TextField,
  Switch,
  FormControlLabel,
  Chip,
  Stack,
} from '@mui/material';
import { 
  Settings as SettingsIcon,
  Api as ApiIcon,
  Storage as StorageIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const Settings: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [testResults, setTestResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<any>(null);
  const [systemInfo, setSystemInfo] = useState<any>(null);

  useEffect(() => {
    fetchSystemInfo();
  }, []);

  const fetchSystemInfo = async () => {
    try {
      const status = await apiService.getStatus();
      setApiStatus(status);
      
      // Get system information
      const info = {
        apiBaseUrl: process.env.REACT_APP_API_URL || 'https://congressional-data-api-v2-1066017671167.us-central1.run.app',
        environment: process.env.NODE_ENV || 'development',
        buildTime: new Date().toISOString(),
        version: '1.0.0',
      };
      setSystemInfo(info);
    } catch (err) {
      console.error('Failed to fetch system info:', err);
    }
  };

  const handleTestCongressApi = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.testCongressApi();
      setTestResults({ type: 'congress-api', result });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to test Congress API');
    } finally {
      setLoading(false);
    }
  };

  const handleTestScrapers = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.testScrapers();
      setTestResults({ type: 'scrapers', result });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to test scrapers');
    } finally {
      setLoading(false);
    }
  };

  const handleTestApiConnection = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.getStatus();
      setTestResults({ type: 'api-connection', result });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to test API connection');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Configuration & Testing
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Monitor system health, test API connections, and view platform configuration.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* System Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <InfoIcon />
                System Status
              </Typography>
              
              <Stack spacing={2}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {apiStatus?.api_status === 'active' ? 
                    <CheckCircleIcon color="success" /> : 
                    <ErrorIcon color="error" />
                  }
                  <Typography>
                    API Service: <strong>{apiStatus?.api_status || 'Unknown'}</strong>
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {apiStatus?.database_status === 'connected' ? 
                    <CheckCircleIcon color="success" /> : 
                    <ErrorIcon color="error" />
                  }
                  <Typography>
                    Database: <strong>{apiStatus?.database_status || 'Unknown'}</strong>
                  </Typography>
                </Box>
                
                <Box>
                  <Typography color="text.secondary">
                    Congress.gov API Rate Limit: <strong>{apiStatus?.congress_api_rate_limit?.remaining || 0} / {apiStatus?.congress_api_rate_limit?.daily_limit || 0}</strong>
                  </Typography>
                </Box>
                
                <Box>
                  <Typography color="text.secondary">
                    Last Status Check: <strong>{new Date().toLocaleString()}</strong>
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* API Testing */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <ApiIcon />
                API Testing
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Test various API endpoints and data sources.
              </Typography>
              
              <Stack spacing={2}>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Button
                    variant="outlined"
                    onClick={handleTestApiConnection}
                    disabled={loading}
                    size="small"
                  >
                    Test API Connection
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={handleTestCongressApi}
                    disabled={loading}
                    size="small"
                  >
                    Test Congress API
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={handleTestScrapers}
                    disabled={loading}
                    size="small"
                  >
                    Test Scrapers
                  </Button>
                </Box>
                
                {loading && <LinearProgress />}
                
                {testResults && (
                  <Box>
                    <Typography variant="subtitle2" gutterBottom>
                      Test Results ({testResults.type}):
                    </Typography>
                    <Box
                      sx={{
                        backgroundColor: '#f5f5f5',
                        p: 2,
                        borderRadius: 1,
                        fontFamily: 'monospace',
                        fontSize: '0.8rem',
                        overflow: 'auto',
                        maxHeight: '200px',
                      }}
                    >
                      <pre>{JSON.stringify(testResults.result, null, 2)}</pre>
                    </Box>
                  </Box>
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* System Information */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <SettingsIcon />
                System Information
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Frontend Version
                  </Typography>
                  <Typography variant="body1">
                    {systemInfo?.version || '1.0.0'}
                  </Typography>
                  <Chip label="Current" size="small" color="primary" />
                </Grid>
                
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Environment
                  </Typography>
                  <Typography variant="body1">
                    {systemInfo?.environment || 'development'}
                  </Typography>
                  <Chip 
                    label={systemInfo?.environment === 'production' ? 'PROD' : 'DEV'} 
                    size="small" 
                    color={systemInfo?.environment === 'production' ? 'success' : 'warning'} 
                  />
                </Grid>
                
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Build Time
                  </Typography>
                  <Typography variant="body1">
                    {systemInfo?.buildTime ? new Date(systemInfo.buildTime).toLocaleString() : 'Unknown'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    API Base URL
                  </Typography>
                  <Typography variant="body1" sx={{ wordBreak: 'break-all', fontSize: '0.9rem' }}>
                    {systemInfo?.apiBaseUrl || 'Not configured'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Database Information
                  </Typography>
                  <Typography variant="body1">
                    PostgreSQL on Google Cloud SQL
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Connection: {apiStatus?.database_status || 'Unknown'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Data Sources
                  </Typography>
                  <Stack direction="row" spacing={1}>
                    <Chip label="Congress.gov API" size="small" color="primary" />
                    <Chip label="House.gov" size="small" color="secondary" />
                    <Chip label="Senate.gov" size="small" color="secondary" />
                  </Stack>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;