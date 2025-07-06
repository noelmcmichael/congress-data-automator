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
import SearchFilter from './SearchFilter';

const Members: React.FC = () => {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Search and filter state
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    chamber: '',
    state: '',
    party: '',
  });
  const [sortBy, setSortBy] = useState('last_name');
  const [sortOrder, setSortOrder] = useState('asc');

  const fetchMembers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getMembers({
        search: searchTerm || undefined,
        chamber: filters.chamber || undefined,
        state: filters.state || undefined,
        party: filters.party || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
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
  }, [searchTerm, filters, sortBy, sortOrder]);

  const handleFilterChange = (filterKey: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [filterKey]: value
    }));
  };

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

      <SearchFilter
        searchPlaceholder="Search members by name..."
        searchValue={searchTerm}
        onSearchChange={setSearchTerm}
        filters={{
          chamber: {
            label: 'Chamber',
            options: [
              { value: 'House', label: 'House' },
              { value: 'Senate', label: 'Senate' },
            ],
            value: filters.chamber,
          },
          state: {
            label: 'State',
            options: [
              { value: 'AL', label: 'Alabama' },
              { value: 'AK', label: 'Alaska' },
              { value: 'AZ', label: 'Arizona' },
              { value: 'AR', label: 'Arkansas' },
              { value: 'CA', label: 'California' },
              { value: 'CO', label: 'Colorado' },
              { value: 'CT', label: 'Connecticut' },
              { value: 'DE', label: 'Delaware' },
              { value: 'FL', label: 'Florida' },
              { value: 'GA', label: 'Georgia' },
              { value: 'HI', label: 'Hawaii' },
              { value: 'ID', label: 'Idaho' },
              { value: 'IL', label: 'Illinois' },
              { value: 'IN', label: 'Indiana' },
              { value: 'IA', label: 'Iowa' },
              { value: 'KS', label: 'Kansas' },
              { value: 'KY', label: 'Kentucky' },
              { value: 'LA', label: 'Louisiana' },
              { value: 'ME', label: 'Maine' },
              { value: 'MD', label: 'Maryland' },
              { value: 'MA', label: 'Massachusetts' },
              { value: 'MI', label: 'Michigan' },
              { value: 'MN', label: 'Minnesota' },
              { value: 'MS', label: 'Mississippi' },
              { value: 'MO', label: 'Missouri' },
              { value: 'MT', label: 'Montana' },
              { value: 'NE', label: 'Nebraska' },
              { value: 'NV', label: 'Nevada' },
              { value: 'NH', label: 'New Hampshire' },
              { value: 'NJ', label: 'New Jersey' },
              { value: 'NM', label: 'New Mexico' },
              { value: 'NY', label: 'New York' },
              { value: 'NC', label: 'North Carolina' },
              { value: 'ND', label: 'North Dakota' },
              { value: 'OH', label: 'Ohio' },
              { value: 'OK', label: 'Oklahoma' },
              { value: 'OR', label: 'Oregon' },
              { value: 'PA', label: 'Pennsylvania' },
              { value: 'RI', label: 'Rhode Island' },
              { value: 'SC', label: 'South Carolina' },
              { value: 'SD', label: 'South Dakota' },
              { value: 'TN', label: 'Tennessee' },
              { value: 'TX', label: 'Texas' },
              { value: 'UT', label: 'Utah' },
              { value: 'VT', label: 'Vermont' },
              { value: 'VA', label: 'Virginia' },
              { value: 'WA', label: 'Washington' },
              { value: 'WV', label: 'West Virginia' },
              { value: 'WI', label: 'Wisconsin' },
              { value: 'WY', label: 'Wyoming' },
            ],
            value: filters.state,
          },
          party: {
            label: 'Party',
            options: [
              { value: 'Democratic', label: 'Democrat' },
              { value: 'Republican', label: 'Republican' },
              { value: 'Independent', label: 'Independent' },
            ],
            value: filters.party,
          },
        }}
        onFilterChange={handleFilterChange}
        sortOptions={[
          { value: 'last_name', label: 'Last Name' },
          { value: 'first_name', label: 'First Name' },
          { value: 'state', label: 'State' },
          { value: 'party', label: 'Party' },
        ]}
        sortValue={sortBy}
        onSortChange={setSortBy}
        sortOrderValue={sortOrder}
        onSortOrderChange={setSortOrder}
      />

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