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
import { apiService, ApiStatus } from '../services/api';
import { fullCongressApiService } from '../services/fullCongressApi';
import UniversalSearch from './UniversalSearch';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<any>(null);
  const [status, setStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  const [useFullData, setUseFullData] = useState(false);
  const [upcomingHearings, setUpcomingHearings] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      let statsData;
      let statusData;
      let hearingsData;
      
      if (useFullData) {
        [statsData, statusData, hearingsData] = await Promise.all([
          fullCongressApiService.getDetailedStats(),
          apiService.getStatus().catch(() => null),
          apiService.getHearings({ page: 1, limit: 5, status: 'scheduled' }).catch(() => []),
        ]);
      } else {
        [statsData, statusData, hearingsData] = await Promise.all([
          apiService.getDatabaseStats(),
          apiService.getStatus(),
          apiService.getHearings({ page: 1, limit: 5, status: 'scheduled' }),
        ]);
      }
      
      setStats(statsData);
      setStatus(statusData);
      setUpcomingHearings(hearingsData);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [useFullData]);

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
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Congressional Data Platform
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
          Your authoritative source for congressional data, committee information, and legislative tracking.
        </Typography>
        <UniversalSearch />
      </Box>

      {/* Quick Navigation */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Quick Access
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Button 
                fullWidth 
                variant="contained" 
                size="large"
                onClick={() => navigate('/members')}
                sx={{ py: 2 }}
              >
                <Box sx={{ textAlign: 'center' }}>
                  <PeopleIcon sx={{ fontSize: 30, mb: 1 }} />
                  <Typography variant="body2">All Members</Typography>
                </Box>
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button 
                fullWidth 
                variant="contained" 
                size="large"
                onClick={() => navigate('/committees')}
                sx={{ py: 2 }}
              >
                <Box sx={{ textAlign: 'center' }}>
                  <GroupIcon sx={{ fontSize: 30, mb: 1 }} />
                  <Typography variant="body2">All Committees</Typography>
                </Box>
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button 
                fullWidth 
                variant="contained" 
                size="large"
                onClick={() => navigate('/hearings')}
                sx={{ py: 2 }}
              >
                <Box sx={{ textAlign: 'center' }}>
                  <EventIcon sx={{ fontSize: 30, mb: 1 }} />
                  <Typography variant="body2">All Hearings</Typography>
                </Box>
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button 
                fullWidth 
                variant="outlined" 
                size="large"
                onClick={() => navigate('/search')}
                sx={{ py: 2 }}
              >
                <Box sx={{ textAlign: 'center' }}>
                  <RefreshIcon sx={{ fontSize: 30, mb: 1 }} />
                  <Typography variant="body2">Advanced Search</Typography>
                </Box>
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Left Column */}
        <Grid item xs={12} md={8}>
          {/* Upcoming Hearings */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Upcoming Hearings
              </Typography>
              {upcomingHearings.length > 0 ? (
                <Box>
                  {upcomingHearings.map((hearing) => (
                    <Box key={hearing.id} sx={{ mb: 2, pb: 1, borderBottom: '1px solid #eee' }}>
                      <Typography variant="body1"><strong>{hearing.title}</strong></Typography>
                      <Typography variant="body2" color="text.secondary">
                        {hearing.committee.name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {format(new Date(hearing.scheduled_date), 'PPP p')}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              ) : (
                <Typography>No upcoming hearings scheduled.</Typography>
              )}
            </CardContent>
          </Card>

          {/* Key Committees */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Key Committees
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip label="Appropriations (House)" component="a" href="/committees/1" clickable />
                <Chip label="Appropriations (Senate)" component="a" href="/committees/2" clickable />
                <Chip label="Ways and Means (House)" component="a" href="/committees/3" clickable />
                <Chip label="Finance (Senate)" component="a" href="/committees/4" clickable />
                <Chip label="Rules (House)" component="a" href="/committees/5" clickable />
                <Chip label="Judiciary (Senate)" component="a" href="/committees/6" clickable />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Right Column */}
        <Grid item xs={12} md={4}>
          {/* API Status */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Platform Status
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                {status?.api_status === 'active' ? <CheckCircleIcon color="success" /> : <WarningIcon color="warning" />}
                <Typography>Service: <strong>{status?.api_status || 'Unknown'}</strong></Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                {status?.database_status === 'connected' ? <CheckCircleIcon color="success" /> : <WarningIcon color="warning" />}
                <Typography>Database: <strong>{status?.database_status || 'Unknown'}</strong></Typography>
              </Box>
              <Typography>
                API Rate Limit: <strong>{status?.congress_api_rate_limit.remaining || 0} / {status?.congress_api_rate_limit.daily_limit || 0}</strong>
              </Typography>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={fetchData}
                disabled={updating}
                sx={{ mt: 2 }}
              >
                Refresh Status
              </Button>
            </CardContent>
          </Card>

          {/* Data Stats */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Data Overview
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <PeopleIcon color="primary" />
                <Typography><strong>{stats?.members.total || 0}</strong> Members</Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <GroupIcon color="primary" />
                <Typography><strong>{stats?.committees.total || 0}</strong> Committees</Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <EventIcon color="primary" />
                <Typography><strong>{stats?.hearings.total || 0}</strong> Hearings</Typography>
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