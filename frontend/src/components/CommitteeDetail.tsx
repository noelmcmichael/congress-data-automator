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
} from '@mui/icons-material';
import { apiService, Member, Committee, Hearing } from '../services/api';
import { 
  getLeadershipPositionInfo, 
  getRepublicanMajoritySummary,
  getSessionDisplayString 
} from '../services/congressionalSession';

interface CommitteeMembership {
  member: Member;
  position: string;
  is_current: boolean;
  start_date: string;
  end_date: string | null;
}

interface CommitteeDetailData {
  committee: Committee;
  memberships: CommitteeMembership[];
  subcommittees: Committee[];
  recent_hearings: Hearing[];
  statistics: {
    total_members: number;
    current_members: number;
    total_hearings: number;
    subcommittee_count: number;
  };
}

const CommitteeDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [committeeData, setCommitteeData] = useState<CommitteeDetailData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCommitteeDetail = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/${id}/detail`);
        if (!response.ok) {
          throw new Error('Failed to fetch committee details');
        }
        
        const data = await response.json();
        setCommitteeData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch committee details');
      } finally {
        setLoading(false);
      }
    };

    fetchCommitteeDetail();
  }, [id]);

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
          Loading committee details...
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
          onClick={() => navigate('/committees')}
        >
          Back to Committees
        </Button>
      </Box>
    );
  }

  if (!committeeData) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Committee not found
        </Alert>
        <Button
          variant="contained"
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/committees')}
        >
          Back to Committees
        </Button>
      </Box>
    );
  }

  const { committee, memberships, subcommittees, recent_hearings, statistics } = committeeData;

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

  const getPositionColor = (position: string, chamber: string) => {
    const positionInfo = getLeadershipPositionInfo(position, chamber as 'House' | 'Senate' | 'Joint');
    return positionInfo.color;
  };

  const getPositionDisplayInfo = (position: string, chamber: string) => {
    return getLeadershipPositionInfo(position, chamber as 'House' | 'Senate' | 'Joint');
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
          onClick={() => navigate('/committees')}
        >
          Committees
        </Link>
        <Typography color="text.primary">
          {committee.name}
        </Typography>
      </Breadcrumbs>

      {/* Back Button */}
      <Button
        variant="outlined"
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/committees')}
        sx={{ mb: 3 }}
      >
        Back to Committees
      </Button>

      <Grid container spacing={3}>
        {/* Committee Information */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar
                  sx={{ width: 80, height: 80, mr: 2, backgroundColor: getChamberColor(committee.chamber) }}
                >
                  <GroupIcon sx={{ fontSize: 40 }} />
                </Avatar>
                <Box>
                  <Typography variant="h4" component="h1" gutterBottom>
                    {committee.name}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 1, flexWrap: 'wrap' }}>
                    <Chip
                      label={committee.chamber}
                      color={getChamberColor(committee.chamber)}
                    />
                    <Chip
                      label={committee.is_subcommittee ? 'Subcommittee' : 'Committee'}
                      variant="outlined"
                    />
                    <Chip
                      label={committee.is_active ? 'Active' : 'Inactive'}
                      color={committee.is_active ? 'success' : 'default'}
                    />
                    <Chip
                      label={getRepublicanMajoritySummary().committeeMajority + ' Controlled'}
                      color="error"
                      size="small"
                    />
                    <Chip
                      label={getSessionDisplayString()}
                      variant="outlined"
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {committee.committee_code || 'No code available'}
                  </Typography>
                </Box>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>
                Committee Details
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Chamber
                  </Typography>
                  <Typography variant="body1">
                    {committee.chamber}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Type
                  </Typography>
                  <Typography variant="body1">
                    {committee.is_subcommittee ? 'Subcommittee' : 'Committee'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Status
                  </Typography>
                  <Typography variant="body1">
                    {committee.is_active ? 'Active' : 'Inactive'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Committee Code
                  </Typography>
                  <Typography variant="body1">
                    {committee.committee_code || 'N/A'}
                  </Typography>
                </Grid>
              </Grid>

              {/* Official Resources Section */}
              {(committee.hearings_url || committee.members_url || committee.official_website_url || committee.website) && (
                <Box sx={{ mt: 3 }}>
                  <Divider sx={{ mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Official Resources
                  </Typography>
                  <Grid container spacing={2}>
                    {committee.hearings_url && (
                      <Grid item xs={12} sm={6}>
                        <Button
                          variant="outlined"
                          startIcon={<EventIcon />}
                          href={committee.hearings_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          fullWidth
                          sx={{ 
                            textTransform: 'none',
                            color: 'primary.main',
                            borderColor: 'primary.main'
                          }}
                        >
                          Official Hearings
                        </Button>
                      </Grid>
                    )}
                    {committee.members_url && (
                      <Grid item xs={12} sm={6}>
                        <Button
                          variant="outlined"
                          startIcon={<GroupIcon />}
                          href={committee.members_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          fullWidth
                          sx={{ 
                            textTransform: 'none',
                            color: 'secondary.main',
                            borderColor: 'secondary.main'
                          }}
                        >
                          Committee Members
                        </Button>
                      </Grid>
                    )}
                    {committee.official_website_url && (
                      <Grid item xs={12}>
                        <Button
                          variant="contained"
                          startIcon={<HomeIcon />}
                          href={committee.official_website_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          fullWidth
                          sx={{ 
                            textTransform: 'none',
                            backgroundColor: 'success.main',
                            '&:hover': {
                              backgroundColor: 'success.dark'
                            }
                          }}
                        >
                          Official Website
                        </Button>
                      </Grid>
                    )}
                    {committee.website && (
                      <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Additional Website
                        </Typography>
                        <Link href={committee.website} target="_blank" rel="noopener noreferrer">
                          {committee.website}
                        </Link>
                      </Grid>
                    )}
                  </Grid>
                  {committee.last_url_update && (
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      Resources updated: {new Date(committee.last_url_update).toLocaleDateString()}
                    </Typography>
                  )}
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
                    {statistics.total_members}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Members
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="secondary">
                    {statistics.current_members}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Current Members
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="success.main">
                    {statistics.total_hearings}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Hearings
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="info.main">
                    {statistics.subcommittee_count}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Subcommittees
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Committee Members */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <PersonIcon sx={{ mr: 1 }} />
                Committee Members
              </Typography>
              
              {memberships.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No members found.
                </Typography>
              ) : (
                <List>
                  {memberships.map((membership, index) => (
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
                      onClick={() => navigate(`/members/${membership.member.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar src={membership.member.official_photo_url || undefined}>
                          <PersonIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={`${membership.member.first_name} ${membership.member.last_name}`}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                            <Chip
                              label={getPositionDisplayInfo(membership.position, committee.chamber).displayName}
                              size="small"
                              color={getPositionColor(membership.position, committee.chamber)}
                            />
                            <Chip
                              label={getPositionDisplayInfo(membership.position, committee.chamber).description}
                              size="small"
                              variant="outlined"
                            />
                            <Chip
                              label={membership.member.party}
                              size="small"
                              sx={{
                                backgroundColor: getPartyColor(membership.member.party),
                                color: 'white',
                              }}
                            />
                            <Chip
                              label={membership.member.chamber}
                              size="small"
                              variant="outlined"
                            />
                            <Chip
                              label={membership.member.district 
                                ? `${membership.member.state}-${membership.member.district}` 
                                : membership.member.state}
                              size="small"
                              variant="outlined"
                            />
                            <Chip
                              label={membership.is_current ? 'Current' : 'Former'}
                              size="small"
                              color={membership.is_current ? 'success' : 'default'}
                            />
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

        {/* Subcommittees */}
        {subcommittees.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  Subcommittees
                </Typography>
                
                <List>
                  {subcommittees.map((subcommittee, index) => (
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
                      onClick={() => navigate(`/committees/${subcommittee.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <GroupIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={subcommittee.name}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                            <Chip
                              label={subcommittee.chamber}
                              size="small"
                              color={getChamberColor(subcommittee.chamber)}
                            />
                            <Chip
                              label={subcommittee.is_active ? 'Active' : 'Inactive'}
                              size="small"
                              color={subcommittee.is_active ? 'success' : 'default'}
                            />
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Recent Hearings */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <EventIcon sx={{ mr: 1 }} />
                Recent Hearings
              </Typography>
              
              {recent_hearings.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No recent hearings found.
                </Typography>
              ) : (
                <List>
                  {recent_hearings.map((hearing, index) => (
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
                            {hearing.location && (
                              <Typography variant="caption" color="text.secondary">
                                {hearing.location}
                              </Typography>
                            )}
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

export default CommitteeDetail;