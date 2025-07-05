import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  LinearProgress,
  Chip,
  Divider,
} from '@mui/material';
import {
  People as PeopleIcon,
  Group as GroupIcon,
  Event as EventIcon,
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { apiService, DatabaseStats, ApiStatus } from '../services/api';
import { format } from 'date-fns';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DatabaseStats | null>(null);
  const [status, setStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [statsData, statusData] = await Promise.all([
        apiService.getDatabaseStats(),
        apiService.getStatus(),
      ]);
      setStats(statsData);
      setStatus(statusData);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAll = async () => {
    try {
      setUpdating(true);
      setError(null);
      await apiService.updateAllData(false);
      // Wait a bit for the background task to complete
      setTimeout(() => {
        fetchData();
        setUpdating(false);
      }, 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update data');
      setUpdating(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchData}>
            Retry
          </Button>
        }>
          {error}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Congressional Data Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchData}
            disabled={updating}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={handleUpdateAll}
            disabled={updating}
          >
            {updating ? 'Updating...' : 'Update All Data'}
          </Button>
        </Box>
      </Box>

      {/* API Status */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            API Status
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {status?.api_status === 'active' ? (
                  <CheckCircleIcon color="success" />
                ) : (
                  <WarningIcon color="warning" />
                )}
                <Typography>
                  Service: <strong>{status?.api_status || 'Unknown'}</strong>
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {status?.database_status === 'connected' ? (
                  <CheckCircleIcon color="success" />
                ) : (
                  <WarningIcon color="warning" />
                )}
                <Typography>
                  Database: <strong>{status?.database_status || 'Unknown'}</strong>
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography>
                API Rate Limit: <strong>{status?.congress_api_rate_limit.remaining || 0} / {status?.congress_api_rate_limit.daily_limit || 0}</strong>
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography>
                Version: <strong>{status?.version || 'Unknown'}</strong>
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Data Statistics */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <PeopleIcon color="primary" sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" color="primary">
                    {stats?.members.total || 0}
                  </Typography>
                  <Typography variant="h6" color="text.secondary">
                    Members
                  </Typography>
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip
                  label={`House: ${stats?.members.house || 0}`}
                  size="small"
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`Senate: ${stats?.members.senate || 0}`}
                  size="small"
                  color="secondary"
                  variant="outlined"
                />
                <Chip
                  label={`Current: ${stats?.members.current || 0}`}
                  size="small"
                  color="success"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <GroupIcon color="primary" sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" color="primary">
                    {stats?.committees.total || 0}
                  </Typography>
                  <Typography variant="h6" color="text.secondary">
                    Committees
                  </Typography>
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip
                  label={`House: ${stats?.committees.house || 0}`}
                  size="small"
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`Senate: ${stats?.committees.senate || 0}`}
                  size="small"
                  color="secondary"
                  variant="outlined"
                />
                <Chip
                  label={`Active: ${stats?.committees.active || 0}`}
                  size="small"
                  color="success"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <EventIcon color="primary" sx={{ fontSize: 40 }} />
                <Box>
                  <Typography variant="h4" color="primary">
                    {stats?.hearings.total || 0}
                  </Typography>
                  <Typography variant="h6" color="text.secondary">
                    Hearings
                  </Typography>
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip
                  label={`Scheduled: ${stats?.hearings.scheduled || 0}`}
                  size="small"
                  color="info"
                  variant="outlined"
                />
                <Chip
                  label={`Completed: ${stats?.hearings.completed || 0}`}
                  size="small"
                  color="success"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Footer */}
      <Box sx={{ mt: 4, pt: 2, borderTop: '1px solid #e0e0e0' }}>
        <Typography variant="body2" color="text.secondary">
          Last updated: {format(lastUpdated, 'PPpp')}
        </Typography>
      </Box>
    </Box>
  );
};

export default Dashboard;