import React, { useState, useEffect } from 'react';
import {
  Box,
  Drawer,
  Paper,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Button,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Checkbox,
  FormControlLabel,
  RadioGroup,
  Radio,
  Slider,
  Switch,
  IconButton,
  InputAdornment,
  Stack,
  Breadcrumbs,
  Link,
  Alert,
  LinearProgress,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Clear as ClearIcon,
  ExpandMore as ExpandMoreIcon,
  Person as PersonIcon,
  Group as GroupIcon,
  Event as EventIcon,
  Home as HomeIcon,
  Settings as SettingsIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Close as CloseIcon,
  Gavel as GavelIcon,
  AccountBalance as CapitolIcon,
  CalendarToday as CalendarIcon,
  LocationOn as LocationIcon,
  Star as StarIcon,
  HowToVote as VoteIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { apiService, Member, Committee, Hearing } from '../services/api';

interface SearchResults {
  members: Member[];
  committees: Committee[];
  hearings: Hearing[];
  total: number;
}

interface AdvancedFilters {
  // Member filters
  chamber: string;
  party: string;
  state: string;
  district: string;
  
  // Committee filters
  committee_type: string;
  is_subcommittee: boolean | null;
  is_active: boolean | null;
  
  // Hearing filters
  status: string;
  date_range: {
    start: string;
    end: string;
  };
  
  // General filters
  search_type: string; // 'all', 'members', 'committees', 'hearings'
  results_per_page: number;
  sort_by: string;
  sort_order: string;
}

const AdvancedSearch: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<AdvancedFilters>({
    chamber: '',
    party: '',
    state: '',
    district: '',
    committee_type: '',
    is_subcommittee: null,
    is_active: null,
    status: '',
    date_range: { start: '', end: '' },
    search_type: 'all',
    results_per_page: 20,
    sort_by: 'name',
    sort_order: 'asc',
  });
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [savedSearches, setSavedSearches] = useState<string[]>([]);

  // State and Party options
  const stateOptions = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
  ];

  const partyOptions = ['Democratic', 'Republican', 'Independent'];

  const performSearch = async () => {
    if (!searchQuery.trim() && Object.values(filters).every(v => !v || v === 'all' || v === '')) {
      setError('Please enter a search term or select at least one filter');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const results: SearchResults = { members: [], committees: [], hearings: [], total: 0 };
      
      // Search members
      if (filters.search_type === 'all' || filters.search_type === 'members') {
        const memberParams = new URLSearchParams();
        if (searchQuery) memberParams.append('search', searchQuery);
        if (filters.chamber) memberParams.append('chamber', filters.chamber);
        if (filters.party) memberParams.append('party', filters.party);
        if (filters.state) memberParams.append('state', filters.state);
        if (filters.district) memberParams.append('district', filters.district);
        memberParams.append('limit', filters.results_per_page.toString());
        
        const membersResponse = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members?${memberParams}`);
        if (membersResponse.ok) {
          const membersData = await membersResponse.json();
          results.members = membersData.slice(0, filters.results_per_page);
        }
      }
      
      // Search committees
      if (filters.search_type === 'all' || filters.search_type === 'committees') {
        const committeeParams = new URLSearchParams();
        if (searchQuery) committeeParams.append('search', searchQuery);
        if (filters.chamber) committeeParams.append('chamber', filters.chamber);
        if (filters.is_subcommittee !== null) committeeParams.append('is_subcommittee', filters.is_subcommittee.toString());
        if (filters.is_active !== null) committeeParams.append('is_active', filters.is_active.toString());
        committeeParams.append('limit', filters.results_per_page.toString());
        
        const committeesResponse = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees?${committeeParams}`);
        if (committeesResponse.ok) {
          const committeesData = await committeesResponse.json();
          results.committees = committeesData.slice(0, filters.results_per_page);
        }
      }
      
      // Search hearings
      if (filters.search_type === 'all' || filters.search_type === 'hearings') {
        const hearingParams = new URLSearchParams();
        if (searchQuery) hearingParams.append('search', searchQuery);
        if (filters.status) hearingParams.append('status', filters.status);
        hearingParams.append('limit', filters.results_per_page.toString());
        
        const hearingsResponse = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/hearings?${hearingParams}`);
        if (hearingsResponse.ok) {
          const hearingsData = await hearingsResponse.json();
          results.hearings = hearingsData.slice(0, filters.results_per_page);
        }
      }
      
      results.total = results.members.length + results.committees.length + results.hearings.length;
      setSearchResults(results);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSearchQuery('');
    setFilters({
      chamber: '',
      party: '',
      state: '',
      district: '',
      committee_type: '',
      is_subcommittee: null,
      is_active: null,
      status: '',
      date_range: { start: '', end: '' },
      search_type: 'all',
      results_per_page: 20,
      sort_by: 'name',
      sort_order: 'asc',
    });
    setSearchResults(null);
    setError(null);
  };

  const saveSearch = () => {
    const searchName = `${searchQuery || 'Advanced Search'} - ${new Date().toLocaleDateString()}`;
    setSavedSearches([...savedSearches, searchName]);
  };

  const getPartyColor = (party: string) => {
    switch (party.toLowerCase()) {
      case 'democratic':
        return '#1976d2';
      case 'republican':
        return '#d32f2f';
      case 'independent':
        return '#388e3c';
      default:
        return '#757575';
    }
  };

  const getChamberColor = (chamber: string) => {
    switch (chamber.toLowerCase()) {
      case 'house':
        return 'primary';
      case 'senate':
        return 'secondary';
      case 'joint':
        return 'success';
      default:
        return 'default';
    }
  };

  const FilterSidebar = () => (
    <Box sx={{ width: 350, p: 2, height: '100vh', overflow: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Advanced Search</Typography>
        <IconButton onClick={() => setDrawerOpen(false)}>
          <CloseIcon />
        </IconButton>
      </Box>
      
      <Divider sx={{ mb: 2 }} />
      
      {/* Search Type */}
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Search In</InputLabel>
        <Select
          value={filters.search_type}
          onChange={(e) => setFilters({ ...filters, search_type: e.target.value })}
        >
          <MenuItem value="all">All Categories</MenuItem>
          <MenuItem value="members">Members Only</MenuItem>
          <MenuItem value="committees">Committees Only</MenuItem>
          <MenuItem value="hearings">Hearings Only</MenuItem>
        </Select>
      </FormControl>
      
      {/* Member Filters */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Member Filters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Stack spacing={2}>
            <FormControl fullWidth>
              <InputLabel>Chamber</InputLabel>
              <Select
                value={filters.chamber}
                onChange={(e) => setFilters({ ...filters, chamber: e.target.value })}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="House">House</MenuItem>
                <MenuItem value="Senate">Senate</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl fullWidth>
              <InputLabel>Party</InputLabel>
              <Select
                value={filters.party}
                onChange={(e) => setFilters({ ...filters, party: e.target.value })}
              >
                <MenuItem value="">All</MenuItem>
                {partyOptions.map(party => (
                  <MenuItem key={party} value={party}>{party}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl fullWidth>
              <InputLabel>State</InputLabel>
              <Select
                value={filters.state}
                onChange={(e) => setFilters({ ...filters, state: e.target.value })}
              >
                <MenuItem value="">All</MenuItem>
                {stateOptions.map(state => (
                  <MenuItem key={state} value={state}>{state}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <TextField
              label="District"
              value={filters.district}
              onChange={(e) => setFilters({ ...filters, district: e.target.value })}
              placeholder="e.g., 01, 02, At Large"
            />
          </Stack>
        </AccordionDetails>
      </Accordion>
      
      {/* Committee Filters */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Committee Filters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Stack spacing={2}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.is_subcommittee === true}
                  onChange={(e) => setFilters({ 
                    ...filters, 
                    is_subcommittee: e.target.checked ? true : null 
                  })}
                />
              }
              label="Subcommittees Only"
            />
            
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.is_active === true}
                  onChange={(e) => setFilters({ 
                    ...filters, 
                    is_active: e.target.checked ? true : null 
                  })}
                />
              }
              label="Active Only"
            />
          </Stack>
        </AccordionDetails>
      </Accordion>
      
      {/* Hearing Filters */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Hearing Filters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Stack spacing={2}>
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Scheduled">Scheduled</MenuItem>
                <MenuItem value="Completed">Completed</MenuItem>
                <MenuItem value="Cancelled">Cancelled</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              label="Start Date"
              type="date"
              value={filters.date_range.start}
              onChange={(e) => setFilters({ 
                ...filters, 
                date_range: { ...filters.date_range, start: e.target.value } 
              })}
              InputLabelProps={{ shrink: true }}
            />
            
            <TextField
              label="End Date"
              type="date"
              value={filters.date_range.end}
              onChange={(e) => setFilters({ 
                ...filters, 
                date_range: { ...filters.date_range, end: e.target.value } 
              })}
              InputLabelProps={{ shrink: true }}
            />
          </Stack>
        </AccordionDetails>
      </Accordion>
      
      {/* Display Options */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Display Options</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Stack spacing={2}>
            <Box>
              <Typography gutterBottom>Results per page</Typography>
              <Slider
                value={filters.results_per_page}
                onChange={(e, value) => setFilters({ ...filters, results_per_page: value as number })}
                min={10}
                max={100}
                step={10}
                marks={[
                  { value: 10, label: '10' },
                  { value: 50, label: '50' },
                  { value: 100, label: '100' }
                ]}
                valueLabelDisplay="auto"
              />
            </Box>
            
            <FormControl fullWidth>
              <InputLabel>Sort By</InputLabel>
              <Select
                value={filters.sort_by}
                onChange={(e) => setFilters({ ...filters, sort_by: e.target.value })}
              >
                <MenuItem value="name">Name</MenuItem>
                <MenuItem value="party">Party</MenuItem>
                <MenuItem value="state">State</MenuItem>
                <MenuItem value="chamber">Chamber</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl>
              <RadioGroup
                value={filters.sort_order}
                onChange={(e) => setFilters({ ...filters, sort_order: e.target.value })}
              >
                <FormControlLabel value="asc" control={<Radio />} label="Ascending" />
                <FormControlLabel value="desc" control={<Radio />} label="Descending" />
              </RadioGroup>
            </FormControl>
          </Stack>
        </AccordionDetails>
      </Accordion>
      
      <Divider sx={{ my: 2 }} />
      
      {/* Action Buttons */}
      <Stack spacing={2}>
        <Button
          variant="contained"
          onClick={performSearch}
          disabled={loading}
          startIcon={<SearchIcon />}
        >
          {loading ? 'Searching...' : 'Search'}
        </Button>
        
        <Button
          variant="outlined"
          onClick={clearFilters}
          startIcon={<ClearIcon />}
        >
          Clear All
        </Button>
        
        <Button
          variant="outlined"
          onClick={saveSearch}
          startIcon={<SaveIcon />}
        >
          Save Search
        </Button>
      </Stack>
      
      {/* Saved Searches */}
      {savedSearches.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Saved Searches
          </Typography>
          <List dense>
            {savedSearches.map((search, index) => (
              <ListItem key={index} dense>
                <ListItemText 
                  primary={search}
                  primaryTypographyProps={{ variant: 'body2' }}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );

  return (
    <Box sx={{ p: 3 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 3 }}>
        <Link
          underline="hover"
          color="inherit"
          href="#"
          onClick={() => navigate('/')}
          sx={{ display: 'flex', alignItems: 'center' }}
        >
          <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
          Home
        </Link>
        <Typography color="text.primary">
          Advanced Search
        </Typography>
      </Breadcrumbs>

      {/* Main Search Interface */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Advanced Search
        </Typography>
        <Typography variant="h6" color="primary" sx={{ mb: 1, fontWeight: 600 }}>
          119th Congress (2025-2027)
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
          Search across all 119th Congress data with powerful filters and options.
        </Typography>
        
        <Paper sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search 119th Congress members, committees, hearings..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && performSearch()}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
            
            <Button
              variant="contained"
              onClick={performSearch}
              disabled={loading}
              sx={{ minWidth: 120 }}
            >
              {loading ? 'Searching...' : 'Search'}
            </Button>
            
            <Button
              variant="outlined"
              onClick={() => setDrawerOpen(true)}
              startIcon={<FilterIcon />}
            >
              Filters
            </Button>
          </Box>
        </Paper>
      </Box>

      {/* Loading State */}
      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {/* Error State */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Search Results */}
      {searchResults && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Search Results ({searchResults.total} total)
          </Typography>
          
          {/* Members Results */}
          {searchResults.members.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <PersonIcon sx={{ mr: 1 }} />
                  Members ({searchResults.members.length})
                </Typography>
                
                <List>
                  {searchResults.members.map((member, index) => (
                    <ListItem
                      key={index}
                      sx={{
                        border: '1px solid #e0e0e0',
                        borderRadius: 1,
                        mb: 1,
                        cursor: 'pointer',
                        '&:hover': { backgroundColor: '#f5f5f5' }
                      }}
                      onClick={() => navigate(`/members/${member.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar src={member.official_photo_url || undefined}>
                          <PersonIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={`${member.first_name} ${member.last_name}`}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                            <Chip
                              label={member.party}
                              size="small"
                              sx={{
                                backgroundColor: getPartyColor(member.party),
                                color: 'white',
                              }}
                            />
                            <Chip
                              label={member.chamber}
                              size="small"
                              color={getChamberColor(member.chamber)}
                            />
                            <Chip
                              label={member.district 
                                ? `${member.state}-${member.district}` 
                                : member.state}
                              size="small"
                              variant="outlined"
                            />
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}

          {/* Committees Results */}
          {searchResults.committees.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  Committees ({searchResults.committees.length})
                </Typography>
                
                <List>
                  {searchResults.committees.map((committee, index) => (
                    <ListItem
                      key={index}
                      sx={{
                        border: '1px solid #e0e0e0',
                        borderRadius: 1,
                        mb: 1,
                        cursor: 'pointer',
                        '&:hover': { backgroundColor: '#f5f5f5' }
                      }}
                      onClick={() => navigate(`/committees/${committee.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <GroupIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={committee.name}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                            <Chip
                              label={committee.chamber}
                              size="small"
                              color={getChamberColor(committee.chamber)}
                            />
                            <Chip
                              label={committee.is_subcommittee ? 'Subcommittee' : 'Committee'}
                              size="small"
                              variant="outlined"
                            />
                            <Chip
                              label={committee.is_active ? 'Active' : 'Inactive'}
                              size="small"
                              color={committee.is_active ? 'success' : 'default'}
                            />
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}

          {/* Hearings Results */}
          {searchResults.hearings.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <EventIcon sx={{ mr: 1 }} />
                  Hearings ({searchResults.hearings.length})
                </Typography>
                
                <List>
                  {searchResults.hearings.map((hearing, index) => (
                    <ListItem
                      key={index}
                      sx={{
                        border: '1px solid #e0e0e0',
                        borderRadius: 1,
                        mb: 1,
                        cursor: 'pointer',
                        '&:hover': { backgroundColor: '#f5f5f5' }
                      }}
                      onClick={() => navigate(`/hearings/${hearing.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <EventIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={hearing.title || 'Hearing'}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                            <Chip
                              label={hearing.status}
                              size="small"
                              color={hearing.status === 'Scheduled' ? 'primary' : 'default'}
                            />
                            {hearing.scheduled_date && (
                              <Typography variant="caption" color="text.secondary">
                                {new Date(hearing.scheduled_date).toLocaleDateString()}
                              </Typography>
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}

          {/* No Results */}
          {searchResults.total === 0 && (
            <Alert severity="info">
              No results found. Try adjusting your search terms or filters.
            </Alert>
          )}
        </Box>
      )}

      {/* Filter Drawer */}
      <Drawer
        anchor="right"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <FilterSidebar />
      </Drawer>
    </Box>
  );
};

export default AdvancedSearch;