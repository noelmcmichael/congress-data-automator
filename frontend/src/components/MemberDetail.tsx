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

interface MemberCommitteeMembership {
  committee: Committee;
  position: string;
  is_current: boolean;
  start_date: string;
  end_date: string | null;
}

interface MemberDetailData {
  member: Member;
  committee_memberships: MemberCommitteeMembership[];
  recent_hearings: Hearing[];
  statistics: {
    total_committees: number;
    chair_positions: number;
    current_memberships: number;
    total_hearings: number;
  };
}

const MemberDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [memberData, setMemberData] = useState<MemberDetailData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMemberDetail = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members/${id}/detail`);
        if (!response.ok) {
          throw new Error('Failed to fetch member details');
        }
        
        const data = await response.json();
        setMemberData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch member details');
      } finally {
        setLoading(false);
      }
    };

    fetchMemberDetail();
  }, [id]);

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
          Loading member details...
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
          onClick={() => navigate('/members')}
        >
          Back to Members
        </Button>
      </Box>
    );
  }

  if (!memberData) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Member not found
        </Alert>
        <Button
          variant="contained"
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/members')}
        >
          Back to Members
        </Button>
      </Box>
    );
  }

  const { member, committee_memberships, recent_hearings, statistics } = memberData;

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

  const getPositionColor = (position: string) => {
    switch (position.toLowerCase()) {
      case 'chair':
        return 'primary';
      case 'ranking member':
        return 'secondary';
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
          onClick={() => navigate('/members')}
        >
          Members
        </Link>
        <Typography color="text.primary">
          {member.first_name} {member.last_name}
        </Typography>
      </Breadcrumbs>

      {/* Back Button */}
      <Button
        variant="outlined"
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/members')}
        sx={{ mb: 3 }}
      >
        Back to Members
      </Button>

      <Grid container spacing={3}>
        {/* Member Information */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar
                  src={member.official_photo_url || undefined}
                  sx={{ width: 80, height: 80, mr: 2 }}
                >
                  <PersonIcon />
                </Avatar>
                <Box>
                  <Typography variant="h4" component="h1" gutterBottom>
                    {member.first_name} {member.middle_name} {member.last_name}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                    <Chip
                      label={member.party}
                      sx={{
                        backgroundColor: getPartyColor(member.party),
                        color: 'white',
                      }}
                    />
                    <Chip
                      label={member.chamber}
                      variant="outlined"
                    />
                    <Chip
                      label={member.district ? `${member.state}-${member.district}` : member.state}
                      variant="outlined"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {member.is_current ? 'Current Member' : 'Former Member'}
                  </Typography>
                </Box>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>
                Member Details
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Chamber
                  </Typography>
                  <Typography variant="body1">
                    {member.chamber}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    State
                  </Typography>
                  <Typography variant="body1">
                    {member.state}
                  </Typography>
                </Grid>
                {member.district && (
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      District
                    </Typography>
                    <Typography variant="body1">
                      {member.district}
                    </Typography>
                  </Grid>
                )}
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Party
                  </Typography>
                  <Typography variant="body1">
                    {member.party}
                  </Typography>
                </Grid>
              </Grid>
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
                    {statistics.total_committees}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Committees
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="secondary">
                    {statistics.chair_positions}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Chair Positions
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="success.main">
                    {statistics.current_memberships}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Current Memberships
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h3" color="info.main">
                    {statistics.total_hearings}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Recent Hearings
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Committee Memberships */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <GroupIcon sx={{ mr: 1 }} />
                Committee Memberships
              </Typography>
              
              {committee_memberships.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No committee memberships found.
                </Typography>
              ) : (
                <List>
                  {committee_memberships.map((membership, index) => (
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
                      onClick={() => navigate(`/committees/${membership.committee.id}`)}
                    >
                      <ListItemAvatar>
                        <Avatar>
                          <GroupIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={membership.committee.name}
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                            <Chip
                              label={membership.position}
                              size="small"
                              color={getPositionColor(membership.position)}
                            />
                            <Chip
                              label={membership.committee.chamber}
                              size="small"
                              variant="outlined"
                            />
                            <Chip
                              label={membership.is_current ? 'Current' : 'Former'}
                              size="small"
                              color={membership.is_current ? 'success' : 'default'}
                            />
                            <Typography variant="caption" color="text.secondary">
                              Since {new Date(membership.start_date).toLocaleDateString()}
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
        </Grid>

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

export default MemberDetail;