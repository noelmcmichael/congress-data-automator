import React, { useState } from 'react';
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
} from '@mui/material';
import { 
  Settings as SettingsIcon,
  Api as ApiIcon,
  Storage as StorageIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const Settings: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [testResults, setTestResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

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

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings & Configuration
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* API Testing */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <ApiIcon />
                API Testing
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Test the various data sources and API endpoints.
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
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

              {loading && <LinearProgress sx={{ mb: 2 }} />}

              {testResults && (
                <Box sx={{ mt: 2 }}>
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
            </CardContent>
          </Card>
        </Grid>

        {/* Data Management */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <StorageIcon />
                Data Management
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Manage data collection settings and preferences.
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Auto-update data"
                />
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Enable web scraping"
                />
                <FormControlLabel
                  control={<Switch />}
                  label="Force refresh on update"
                />
                
                <Divider sx={{ my: 1 }} />
                
                <TextField
                  label="Update frequency (minutes)"
                  type="number"
                  defaultValue="60"
                  size="small"
                  helperText="How often to check for new data"
                />
                
                <TextField
                  label="Max items per request"
                  type="number"
                  defaultValue="50"
                  size="small"
                  helperText="Maximum items to fetch in one request"
                />
              </Box>
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
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Frontend Version
                  </Typography>
                  <Typography variant="body1">
                    1.0.0
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    API Base URL
                  </Typography>
                  <Typography variant="body1" sx={{ wordBreak: 'break-all' }}>
                    {process.env.REACT_APP_API_URL || 'https://congressional-data-api-1066017671167.us-central1.run.app'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Build Time
                  </Typography>
                  <Typography variant="body1">
                    {new Date().toLocaleString()}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Environment
                  </Typography>
                  <Typography variant="body1">
                    {process.env.NODE_ENV || 'development'}
                  </Typography>
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