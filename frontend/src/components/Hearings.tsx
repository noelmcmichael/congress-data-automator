import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Alert,
  LinearProgress,
  Button,
  Grid,
  Chip,
  IconButton,
} from '@mui/material';
import { 
  Refresh as RefreshIcon, 
  PlayArrow as PlayArrowIcon,
  Description as DescriptionIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import { apiService, Hearing } from '../services/api';
import { format, parseISO } from 'date-fns';

const Hearings: React.FC = () => {
  const [hearings, setHearings] = useState<Hearing[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchHearings = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getHearings();
      setHearings(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch hearings');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    try {
      setUpdating(true);
      setError(null);
      await apiService.updateHearings(false);
      // Wait a bit for the background task to complete
      setTimeout(() => {
        fetchHearings();
        setUpdating(false);
      }, 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update hearings');
      setUpdating(false);
    }
  };

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'No date';
    try {
      return format(parseISO(dateString), 'PPp');
    } catch {
      return dateString;
    }
  };

  useEffect(() => {
    fetchHearings();
  }, []);

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Congressional Hearings
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Congressional Hearings
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchHearings}
            disabled={updating}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={handleUpdate}
            disabled={updating}
          >
            {updating ? 'Updating...' : 'Update Hearings'}
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {hearings.length === 0 ? (
        <Alert severity="info">
          No hearings data available. The hearings endpoint is not yet implemented in the API.
          Use the "Update Hearings" button to collect data, then refresh to see results.
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {hearings.map((hearing) => (
            <Grid item xs={12} sm={6} md={4} key={hearing.id}>
              <Card sx={{ height: '100%' }}>
                <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <Typography variant="h6" component="div" sx={{ mb: 2 }}>
                    {hearing.title || 'Untitled Hearing'}
                  </Typography>
                  
                  {hearing.description && (
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {hearing.description.length > 150 
                        ? `${hearing.description.substring(0, 150)}...` 
                        : hearing.description}
                    </Typography>
                  )}

                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                    <Chip
                      label={hearing.status}
                      size="small"
                      color={hearing.status === 'Completed' ? 'success' : 'info'}
                    />
                    {hearing.hearing_type && (
                      <Chip
                        label={hearing.hearing_type}
                        size="small"
                        variant="outlined"
                      />
                    )}
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    {hearing.scheduled_date && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <ScheduleIcon fontSize="small" />
                        <Typography variant="body2">
                          {formatDate(hearing.scheduled_date)}
                        </Typography>
                      </Box>
                    )}
                    
                    {hearing.location && (
                      <Typography variant="body2" color="text.secondary">
                        Location: {hearing.location.length > 100 
                          ? `${hearing.location.substring(0, 100)}...` 
                          : hearing.location}
                      </Typography>
                    )}
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1, mt: 'auto' }}>
                    {hearing.video_url && (
                      <IconButton
                        size="small"
                        href={hearing.video_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="Watch Video"
                      >
                        <PlayArrowIcon />
                      </IconButton>
                    )}
                    {hearing.webcast_url && (
                      <IconButton
                        size="small"
                        href={hearing.webcast_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="Watch Webcast"
                      >
                        <PlayArrowIcon />
                      </IconButton>
                    )}
                    {hearing.transcript_url && (
                      <IconButton
                        size="small"
                        href={hearing.transcript_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="View Transcript"
                      >
                        <DescriptionIcon />
                      </IconButton>
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default Hearings;