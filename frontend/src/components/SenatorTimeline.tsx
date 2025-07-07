import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Alert,
  LinearProgress,
  Grid,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  Stack,
  Paper,
} from '@mui/material';
import {
  Schedule as ScheduleIcon,
  HowToVote as VoteIcon,
  Person as PersonIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import { Member } from '../services/api';

interface SenatorByTermClass {
  class_i: {
    description: string;
    next_election_year: number;
    senators: Member[];
    count: number;
  };
  class_ii: {
    description: string;
    next_election_year: number;
    senators: Member[];
    count: number;
  };
  class_iii: {
    description: string;
    next_election_year: number;
    senators: Member[];
    count: number;
  };
}

interface SenatorTimelineData {
  term_classes: SenatorByTermClass;
  party_breakdown: {
    [party: string]: {
      total: number;
      class_i: number;
      class_ii: number;
      class_iii: number;
    };
  };
  statistics: {
    total_senators: number;
    elections_2024: number;
    elections_2026: number;
    elections_2028: number;
  };
}

const SenatorTimeline: React.FC = () => {
  const [timelineData, setTimelineData] = useState<SenatorTimelineData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSenatorTimeline = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/senators/by-term-class`);
        if (!response.ok) {
          throw new Error('Failed to fetch senator timeline data');
        }
        
        const data = await response.json();
        setTimelineData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch senator timeline data');
      } finally {
        setLoading(false);
      }
    };

    fetchSenatorTimeline();
  }, []);

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
          Loading senator timeline data...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      </Box>
    );
  }

  if (!timelineData) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Senator timeline data not found
        </Alert>
      </Box>
    );
  }

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

  const renderSenatorList = (senators: Member[], termClass: string, nextElection: number) => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
            <VoteIcon sx={{ mr: 1 }} />
            Class {termClass} - {nextElection} Election
          </Typography>
          <Chip
            label={`${senators.length} Senators`}
            color="primary"
            variant="outlined"
          />
        </Box>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Next election in {nextElection}
        </Typography>
        
        {senators.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            No senators in this class.
          </Typography>
        ) : (
          <List>
            {senators.map((senator, index) => (
              <ListItem
                key={index}
                sx={{
                  border: '1px solid #e0e0e0',
                  borderRadius: 1,
                  mb: 1,
                  '&:hover': {
                    backgroundColor: '#f5f5f5',
                    cursor: 'pointer',
                  },
                }}
                onClick={() => window.open(`#/members/${senator.id}`, '_blank')}
              >
                <ListItemAvatar>
                  <Avatar
                    src={senator.official_photo_url || undefined}
                    sx={{ bgcolor: getPartyColor(senator.party) }}
                  >
                    <PersonIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={`${senator.first_name} ${senator.last_name}`}
                  secondary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                      <Chip
                        label={senator.party}
                        size="small"
                        sx={{
                          backgroundColor: getPartyColor(senator.party),
                          color: 'white',
                        }}
                      />
                      <Chip
                        label={senator.state}
                        size="small"
                        variant="outlined"
                      />
                      <Typography variant="caption" color="text.secondary">
                        Next Election: {nextElection}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <CalendarIcon sx={{ mr: 2 }} />
        Senate Re-election Timeline
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        U.S. Senators serve six-year terms with elections staggered across three classes.
      </Typography>

      {/* Statistics Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="primary">
              {timelineData.statistics.total_senators}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Senators
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="error">
              {timelineData.statistics.elections_2024}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              2024 Elections
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="warning.main">
              {timelineData.statistics.elections_2026}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              2026 Elections
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h3" color="success.main">
              {timelineData.statistics.elections_2028}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              2028 Elections
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Party Breakdown */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Party Breakdown by Term Class
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(timelineData.party_breakdown).map(([party, data]) => (
              <Grid item xs={12} sm={6} md={4} key={party}>
                <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                  <Typography variant="subtitle1" sx={{ color: getPartyColor(party) }}>
                    {party}
                  </Typography>
                  <Typography variant="h4">{data.total}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Class I: {data.class_i} | Class II: {data.class_ii} | Class III: {data.class_iii}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Senator Lists by Term Class */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          {renderSenatorList(
            timelineData.term_classes.class_i.senators,
            'I',
            timelineData.term_classes.class_i.next_election_year
          )}
        </Grid>
        <Grid item xs={12} md={4}>
          {renderSenatorList(
            timelineData.term_classes.class_ii.senators,
            'II',
            timelineData.term_classes.class_ii.next_election_year
          )}
        </Grid>
        <Grid item xs={12} md={4}>
          {renderSenatorList(
            timelineData.term_classes.class_iii.senators,
            'III',
            timelineData.term_classes.class_iii.next_election_year
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default SenatorTimeline;