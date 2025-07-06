import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  Typography,
  Collapse,
  Grid,
  Button,
  InputAdornment,
  SelectChangeEvent,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList,
  ExpandMore,
  ExpandLess,
  Clear,
  ArrowUpward,
  ArrowDownward,
} from '@mui/icons-material';

interface FilterOption {
  value: string;
  label: string;
}

interface SearchFilterProps {
  searchPlaceholder: string;
  searchValue: string;
  onSearchChange: (value: string) => void;
  filters: {
    [key: string]: {
      label: string;
      options: FilterOption[];
      value: string;
    };
  };
  onFilterChange: (filterKey: string, value: string) => void;
  sortOptions: FilterOption[];
  sortValue: string;
  onSortChange: (value: string) => void;
  sortOrderValue: string;
  onSortOrderChange: (value: string) => void;
}

const SearchFilter: React.FC<SearchFilterProps> = ({
  searchPlaceholder,
  searchValue,
  onSearchChange,
  filters,
  onFilterChange,
  sortOptions,
  sortValue,
  onSortChange,
  sortOrderValue,
  onSortOrderChange,
}) => {
  const [showFilters, setShowFilters] = useState(false);
  const [debounceTimer, setDebounceTimer] = useState<NodeJS.Timeout | null>(null);
  const [searchInput, setSearchInput] = useState(searchValue);

  // Debounced search
  const handleSearchChange = (value: string) => {
    setSearchInput(value);
    
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    
    const timer = setTimeout(() => {
      onSearchChange(value);
    }, 300);
    
    setDebounceTimer(timer);
  };

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }
    };
  }, [debounceTimer]);

  const hasActiveFilters = Object.values(filters).some(filter => filter.value !== '');
  const activeFilterCount = Object.values(filters).filter(f => f.value !== '').length;

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      {/* Search Bar */}
      <TextField
        fullWidth
        placeholder={searchPlaceholder}
        value={searchInput}
        onChange={(e) => handleSearchChange(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
        sx={{ mb: 2 }}
      />

      {/* Filter Toggle and Sort Controls */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Button
          onClick={() => setShowFilters(!showFilters)}
          startIcon={<FilterList />}
          endIcon={showFilters ? <ExpandLess /> : <ExpandMore />}
          sx={{ gap: 1 }}
        >
          Filters
          {hasActiveFilters && (
            <Chip
              label={activeFilterCount}
              size="small"
              color="primary"
              sx={{ ml: 1 }}
            />
          )}
        </Button>

        {/* Sort Controls */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="body2" color="textSecondary">
            Sort by:
          </Typography>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <Select
              value={sortValue}
              onChange={(e: SelectChangeEvent) => onSortChange(e.target.value)}
            >
              {sortOptions.map(option => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <IconButton
            onClick={() => onSortOrderChange(sortOrderValue === 'asc' ? 'desc' : 'asc')}
            size="small"
            title={sortOrderValue === 'asc' ? 'Sort descending' : 'Sort ascending'}
          >
            {sortOrderValue === 'asc' ? <ArrowUpward /> : <ArrowDownward />}
          </IconButton>
        </Box>
      </Box>

      {/* Filters Panel */}
      <Collapse in={showFilters}>
        <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
          <Grid container spacing={2}>
            {Object.entries(filters).map(([key, filter]) => (
              <Grid item xs={12} sm={6} md={4} key={key}>
                <FormControl fullWidth size="small">
                  <InputLabel>{filter.label}</InputLabel>
                  <Select
                    value={filter.value}
                    onChange={(e: SelectChangeEvent) => onFilterChange(key, e.target.value)}
                    label={filter.label}
                    endAdornment={
                      filter.value && (
                        <IconButton
                          onClick={() => onFilterChange(key, '')}
                          size="small"
                          sx={{ mr: 1 }}
                        >
                          <Clear />
                        </IconButton>
                      )
                    }
                  >
                    <MenuItem value="">All</MenuItem>
                    {filter.options.map(option => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            ))}
          </Grid>
          
          {/* Clear All Filters */}
          {hasActiveFilters && (
            <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
              <Button
                onClick={() => {
                  Object.keys(filters).forEach(key => onFilterChange(key, ''));
                }}
                size="small"
                variant="outlined"
              >
                Clear All Filters
              </Button>
            </Box>
          )}
        </Box>
      </Collapse>
    </Paper>
  );
};

export default SearchFilter;