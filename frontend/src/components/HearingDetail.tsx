import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Breadcrumbs,
  Link,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Paper,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Person as PersonIcon,
  Group as GroupIcon,
  Event as EventIcon,
  Home as HomeIcon,
  NavigateNext as NavigateNextIcon,
  Place as PlaceIcon,
  Schedule as ScheduleIcon,
  Description as DescriptionIcon,
} from '@mui/icons-material';
import { apiService, Member, Committee, Hearing } from '../services/api';

interface Witness {
  id: number;
  name: string;
  title: string;
  organization: string;
  testimony_url: string | null;
  witness_type: string;
  hearing_id: number;
}

interface HearingDocument {
  id: number;
  title: string;
  document_type: string;
  url: string;
  description: string | null;
  hearing_id: number;
}

interface HearingDetailData {
  hearing: Hearing;
  committee: Committee | null;
  witnesses: Witness[];
  documents: HearingDocument[];
  statistics: {
    total_witnesses: number;
    total_documents: number;
    duration_minutes: number | null;
  };
}

const HearingDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [hearingData, setHearingData] = useState<HearingDetailData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHearingDetail = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/hearings/${id}/detail`);
        if (!response.ok) {
          throw new Error('Failed to fetch hearing details');
        }
        
        const data = await response.json();
        setHearingData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch hearing details');
      } finally {
        setLoading(false);
      }
    };

    fetchHearingDetail();
  }, [id]);

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
          Loading hearing details...
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
        <Button
          variant="contained"
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/hearings')}
        >
          Back to Hearings
        </Button>
      </Box>
    );
  }

  if (!hearingData) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Hearing not found
        </Alert>
        <Button
          variant="contained"
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/hearings')}
        >
          Back to Hearings
        </Button>
      </Box>
    );
  }

  const { hearing, committee, witnesses, documents, statistics } = hearingData;

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'scheduled':
        return 'primary';
      case 'completed':
        return 'success';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
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

  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return 'Not scheduled';
    return new Date(dateString).toLocaleString();
  };

  const formatTime = (dateString: string | null | undefined) => {
    if (!dateString) return 'Not scheduled';
    return new Date(dateString).toLocaleTimeString();
  };

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
        <Link
          underline="hover"
          color="inherit"
          href="#"
          onClick={() => navigate('/hearings')}
        >
          Hearings
        </Link>
        <Typography color="text.primary">
          {hearing.title || 'Hearing Details'}
        </Typography>
      </Breadcrumbs>

      {/* Back Button */}
      <Button
        variant="outlined"
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/hearings')}
        sx={{ mb: 3 }}
      >
        Back to Hearings
      </Button>

      <Grid container spacing={3}>
        {/* Hearing Information */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar
                  sx={{ width: 80, height: 80, mr: 2, backgroundColor: getStatusColor(hearing.status) }}
                >
                  <EventIcon sx={{ fontSize: 40 }} />
                </Avatar>
                <Box>
                  <Typography variant="h4" component="h1" gutterBottom>
                    {hearing.title || 'Congressional Hearing'}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                    <Chip
                      label={hearing.status}
                      color={getStatusColor(hearing.status)}
                    />
                    {committee && (
                      <Chip
                        label={committee.chamber}
                        color={getChamberColor(committee.chamber)}
                      />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {hearing.congress_gov_id || 'No ID available'}
                  </Typography>
                </Box>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>
                Hearing Details
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ScheduleIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Scheduled Date & Time
                      </Typography>
                      <Typography variant="body1">
                        {formatDate(hearing.scheduled_date)}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <PlaceIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Location
                      </Typography>
                      <Typography variant="body1">
                        {hearing.location || 'Not specified'}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Room
                  </Typography>
                  <Typography variant="body1">
                    {hearing.room || 'Not specified'}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Status
                  </Typography>
                  <Typography variant="body1">
                    {hearing.status}
                  </Typography>
                </Grid>
              </Grid>

              {hearing.description && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Description
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    {hearing.description}
                  </Typography>
                </Box>
              )}

              {hearing.video_url && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Video Stream
                  </Typography>
                  <Link href={hearing.video_url} target="_blank" rel="noopener noreferrer">
                    {hearing.video_url}
                  </Link>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Statistics */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Statistics
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="h3" color="primary">
                    {statistics.total_witnesses}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Witnesses
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="secondary">
                    {statistics.total_documents}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Documents
                  </Typography>
                </Box>
                {statistics.duration_minutes && (
                  <Box>
                    <Typography variant="h3" color="success.main">
                      {statistics.duration_minutes}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Minutes
                    </Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Committee Information */}
        {committee && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  Committee
                </Typography>
                
                <ListItem
                  sx={{
                    border: '1px solid #e0e0e0',
                    borderRadius: 1,
                    '&:hover': {
                      backgroundColor: '#f5f5f5',
                      cursor: 'pointer',
                    },
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
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Witnesses */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <PersonIcon sx={{ mr: 1 }} />
                Witnesses
              </Typography>
              
              {witnesses.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No witnesses listed.
                </Typography>
              ) : (
                <List>
                  {witnesses.map((witness, index) => (
                    <ListItem
                      key={index}
                      sx={{
                        border: '1px solid #e0e0e0',
                        borderRadius: 1,
                        mb: 1,
                      }}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <PersonIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={witness.name}
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="body2" color="text.secondary">
                              {witness.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {witness.organization}
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                              <Chip
                                label={witness.witness_type}
                                size="small"
                                variant="outlined"
                              />
                              {witness.testimony_url && (
                                <Link
                                  href={witness.testimony_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  sx={{ fontSize: '0.875rem' }}
                                >
                                  View Testimony
                                </Link>
                              )}
                            </Box>
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Documents */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <DescriptionIcon sx={{ mr: 1 }} />
                Documents
              </Typography>
              
              {documents.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No documents available.
                </Typography>
              ) : (
                <List>
                  {documents.map((document, index) => (
                    <ListItem
                      key={index}
                      sx={{
                        border: '1px solid #e0e0e0',
                        borderRadius: 1,
                        mb: 1,
                      }}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <DescriptionIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={document.title}
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            {document.description && (
                              <Typography variant="body2" color="text.secondary">
                                {document.description}
                              </Typography>
                            )}
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                              <Chip
                                label={document.document_type}
                                size="small"
                                variant="outlined"
                              />
                              <Link
                                href={document.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                sx={{ fontSize: '0.875rem' }}
                              >
                                View Document
                              </Link>
                            </Box>
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default HearingDetail;