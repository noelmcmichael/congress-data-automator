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
  Avatar,
} from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';
import { apiService, Member } from '../services/api';

const Members: React.FC = () => {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getMembers();
      setMembers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch members');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    try {
      setUpdating(true);
      setError(null);
      await apiService.updateMembers(false);
      // Wait a bit for the background task to complete
      setTimeout(() => {
        fetchMembers();
        setUpdating(false);
      }, 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update members');
      setUpdating(false);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, []);

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Congressional Members
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Congressional Members
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchMembers}
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
            {updating ? 'Updating...' : 'Update Members'}
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {members.length === 0 ? (
        <Alert severity="info">
          No members data available. The members endpoint is not yet implemented in the API.
          Use the "Update Members" button to collect data, then refresh to see results.
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {members.map((member) => (
            <Grid item xs={12} sm={6} md={4} key={member.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <Avatar
                      src={member.official_photo_url}
                      alt={`${member.first_name} ${member.last_name}`}
                      sx={{ width: 60, height: 60 }}
                    >
                      {member.first_name[0]}{member.last_name[0]}
                    </Avatar>
                    <Box>
                      <Typography variant="h6">
                        {member.first_name} {member.last_name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {member.party} - {member.state}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip
                      label={member.chamber}
                      size="small"
                      color={member.chamber === 'House' ? 'primary' : 'secondary'}
                    />
                    {member.district && (
                      <Chip
                        label={`District ${member.district}`}
                        size="small"
                        variant="outlined"
                      />
                    )}
                    {member.is_current && (
                      <Chip
                        label="Current"
                        size="small"
                        color="success"
                        variant="outlined"
                      />
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

export default Members;