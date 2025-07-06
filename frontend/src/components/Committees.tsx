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
import { Refresh as RefreshIcon, OpenInNew as OpenInNewIcon } from '@mui/icons-material';
import { apiService, Committee } from '../services/api';
import SearchFilter from './SearchFilter';

const Committees: React.FC = () => {
  const [committees, setCommittees] = useState<Committee[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Search and filter state
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    chamber: '',
  });
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');

  const fetchCommittees = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getCommittees({
        search: searchTerm || undefined,
        chamber: filters.chamber || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      setCommittees(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch committees');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    try {
      setUpdating(true);
      setError(null);
      await apiService.updateCommittees(false);
      // Wait a bit for the background task to complete
      setTimeout(() => {
        fetchCommittees();
        setUpdating(false);
      }, 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update committees');
      setUpdating(false);
    }
  };

  useEffect(() => {
    fetchCommittees();
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
          Congressional Committees
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Congressional Committees
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchCommittees}
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
            {updating ? 'Updating...' : 'Update Committees'}
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <SearchFilter
        searchPlaceholder="Search committees by name..."
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
        }}
        onFilterChange={handleFilterChange}
        sortOptions={[
          { value: 'name', label: 'Committee Name' },
          { value: 'chamber', label: 'Chamber' },
        ]}
        sortValue={sortBy}
        onSortChange={setSortBy}
        sortOrderValue={sortOrder}
        onSortOrderChange={setSortOrder}
      />

      {committees.length === 0 ? (
        <Alert severity="info">
          No committees data available. The committees endpoint is not yet implemented in the API.
          Use the "Update Committees" button to collect data, then refresh to see results.
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {committees.map((committee) => (
            <Grid item xs={12} sm={6} md={4} key={committee.id}>
              <Card sx={{ height: '100%' }}>
                <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                      {committee.name}
                    </Typography>
                    {committee.website_url && (
                      <IconButton
                        size="small"
                        href={committee.website_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <OpenInNewIcon />
                      </IconButton>
                    )}
                  </Box>
                  
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                    <Chip
                      label={committee.chamber}
                      size="small"
                      color={committee.chamber === 'House' ? 'primary' : 'secondary'}
                    />
                    {committee.is_subcommittee && (
                      <Chip
                        label="Subcommittee"
                        size="small"
                        variant="outlined"
                      />
                    )}
                    {committee.is_active && (
                      <Chip
                        label="Active"
                        size="small"
                        color="success"
                        variant="outlined"
                      />
                    )}
                  </Box>

                  {committee.committee_code && (
                    <Typography variant="body2" color="text.secondary">
                      Code: {committee.committee_code}
                    </Typography>
                  )}
                  
                  {committee.congress_gov_id && (
                    <Typography variant="body2" color="text.secondary">
                      Congress.gov ID: {committee.congress_gov_id}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default Committees;