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
  Badge,
  Tooltip,
  Stack,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Person as PersonIcon,
  Group as GroupIcon,
  Event as EventIcon,
  Home as HomeIcon,
  NavigateNext as NavigateNextIcon,
  Gavel as GavelIcon,
  Schedule as ScheduleIcon,
  CalendarToday as CalendarIcon,
  HowToVote as VoteIcon,
  Star as StarIcon,
  AccountBalance as CapitolIcon,
  Assignment as AssignmentIcon,
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

interface EnhancedMemberData {
  member: Member;
  committee_memberships: {
    id: number;
    committee: {
      id: number;
      name: string;
      chamber: string;
      committee_type: string;
      is_subcommittee: boolean;
      parent_committee_id?: number;
    };
    position: string;
    is_current: boolean;
    start_date: string;
    end_date: string | null;
  }[];
  leadership_positions: {
    committee_name: string;
    position: string;
    is_current: boolean;
  }[];
  term_information: {
    current_term_start: string;
    current_term_end: string;
    is_current: boolean;
    senate_class?: string;
    next_election_year?: number;
  };
  statistics: {
    total_committees: number;
    current_committees: number;
    leadership_positions: number;
    current_leadership: number;
    standing_committees: number;
    subcommittees: number;
  };
}

const MemberDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [memberData, setMemberData] = useState<MemberDetailData | null>(null);
  const [enhancedData, setEnhancedData] = useState<EnhancedMemberData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMemberDetail = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        // First try to get enhanced data
        try {
          const enhancedResponse = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members/${id}/enhanced`);
          if (enhancedResponse.ok) {
            const enhancedData = await enhancedResponse.json();
            setEnhancedData(enhancedData);
          }
        } catch (enhancedError) {
          console.warn('Enhanced endpoint not available, using standard detail endpoint');
        }
        
        // Also get the standard detail data as fallback
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
  
  // Use enhanced data if available, otherwise use standard data
  const displayData = enhancedData || {
    member,
    committee_memberships: committee_memberships.map(cm => ({
      id: Math.random(),
      committee: {
        id: cm.committee.id,
        name: cm.committee.name,
        chamber: cm.committee.chamber,
        committee_type: 'Standing',
        is_subcommittee: cm.committee.is_subcommittee,
        parent_committee_id: cm.committee.parent_committee_id
      },
      position: cm.position,
      is_current: cm.is_current,
      start_date: cm.start_date,
      end_date: cm.end_date
    })),
    leadership_positions: committee_memberships
      .filter(cm => cm.position && ['Chair', 'Ranking Member', 'Chairwoman', 'Chairman'].includes(cm.position))
      .map(cm => ({
        committee_name: cm.committee.name,
        position: cm.position,
        is_current: cm.is_current
      })),
    term_information: {
      current_term_start: member.created_at,
      current_term_end: '2027-01-03',
      is_current: member.is_current,
      ...(member.chamber === 'Senate' && {
        senate_class: 'II',
        next_election_year: 2026
      })
    },
    statistics: {
      total_committees: statistics.total_committees,
      current_committees: statistics.current_memberships,
      leadership_positions: statistics.chair_positions,
      current_leadership: statistics.chair_positions,
      standing_committees: committee_memberships.filter(cm => !cm.committee.is_subcommittee).length,
      subcommittees: committee_memberships.filter(cm => cm.committee.is_subcommittee).length
    }
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

        {/* Enhanced Statistics */}
        <Grid item xs={12} md={4}>
          <Stack spacing={2}>
            {/* Committee Statistics */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  Committee Statistics
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="primary">
                        {displayData.statistics.total_committees}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Total Committees
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="success.main">
                        {displayData.statistics.current_committees}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Current
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="secondary">
                        {displayData.statistics.standing_committees}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Standing
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="info.main">
                        {displayData.statistics.subcommittees}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Subcommittees
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            {/* Leadership Positions */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <GavelIcon sx={{ mr: 1 }} />
                  Leadership
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" color="warning.main">
                      {displayData.statistics.leadership_positions}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Positions
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" color="success.main">
                      {displayData.statistics.current_leadership}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Current
                    </Typography>
                  </Box>
                </Box>
                
                {/* Leadership Position List */}
                {displayData.leadership_positions.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Divider sx={{ mb: 2 }} />
                    <Stack spacing={1}>
                      {displayData.leadership_positions.map((lp, index) => (
                        <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Badge
                            color={lp.is_current ? 'success' : 'default'}
                            variant="dot"
                          />
                          <Typography variant="body2">
                            <strong>{lp.position}</strong>
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {lp.committee_name}
                          </Typography>
                        </Box>
                      ))}
                    </Stack>
                  </Box>
                )}
              </CardContent>
            </Card>

            {/* Term Information */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <CalendarIcon sx={{ mr: 1 }} />
                  Term Information
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Current Term
                    </Typography>
                    <Typography variant="body1">
                      {new Date(displayData.term_information.current_term_start).getFullYear()} - {new Date(displayData.term_information.current_term_end).getFullYear()}
                    </Typography>
                  </Box>
                  
                  {member.chamber === 'Senate' && displayData.term_information.senate_class && (
                    <>
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          Senate Class
                        </Typography>
                        <Typography variant="body1">
                          Class {displayData.term_information.senate_class}
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          Next Election
                        </Typography>
                        <Typography variant="body1" color="primary">
                          {displayData.term_information.next_election_year}
                        </Typography>
                      </Box>
                    </>
                  )}
                  
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Status
                    </Typography>
                    <Chip
                      label={displayData.term_information.is_current ? 'Current' : 'Former'}
                      color={displayData.term_information.is_current ? 'success' : 'default'}
                      size="small"
                    />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Stack>
        </Grid>

        {/* Enhanced Committee Memberships */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  Committee Memberships
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip
                    label={`${displayData.statistics.standing_committees} Standing`}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                  <Chip
                    label={`${displayData.statistics.subcommittees} Subcommittees`}
                    size="small"
                    color="secondary"
                    variant="outlined"
                  />
                  {displayData.statistics.leadership_positions > 0 && (
                    <Chip
                      icon={<StarIcon />}
                      label={`${displayData.statistics.leadership_positions} Leadership`}
                      size="small"
                      color="warning"
                      variant="outlined"
                    />
                  )}
                </Box>
              </Box>
              
              {displayData.committee_memberships.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No committee memberships found.
                </Typography>
              ) : (
                <Box>
                  {/* Standing Committees */}
                  {displayData.committee_memberships.filter(cm => !cm.committee.is_subcommittee).length > 0 && (
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                        <CapitolIcon sx={{ mr: 1, fontSize: 20 }} />
                        Standing Committees
                      </Typography>
                      <List>
                        {displayData.committee_memberships
                          .filter(cm => !cm.committee.is_subcommittee)
                          .map((membership, index) => (
                            <ListItem
                              key={`standing-${index}`}
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
                                <Avatar sx={{ bgcolor: getPartyColor(member.party) }}>
                                  {membership.position === 'Chair' || membership.position === 'Chairwoman' || membership.position === 'Chairman' ? (
                                    <GavelIcon />
                                  ) : membership.position === 'Ranking Member' ? (
                                    <StarIcon />
                                  ) : (
                                    <GroupIcon />
                                  )}
                                </Avatar>
                              </ListItemAvatar>
                              <ListItemText
                                primary={
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Typography variant="subtitle1">
                                      {membership.committee.name}
                                    </Typography>
                                    {(membership.position === 'Chair' || membership.position === 'Chairwoman' || membership.position === 'Chairman') && (
                                      <Tooltip title="Committee Chair">
                                        <GavelIcon color="warning" fontSize="small" />
                                      </Tooltip>
                                    )}
                                    {membership.position === 'Ranking Member' && (
                                      <Tooltip title="Ranking Member">
                                        <StarIcon color="primary" fontSize="small" />
                                      </Tooltip>
                                    )}
                                  </Box>
                                }
                                secondary={
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1, flexWrap: 'wrap' }}>
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
                                      label={membership.committee.committee_type}
                                      size="small"
                                      variant="outlined"
                                    />
                                    <Chip
                                      label={membership.is_current ? 'Current' : 'Former'}
                                      size="small"
                                      color={membership.is_current ? 'success' : 'default'}
                                    />
                                    {membership.start_date && (
                                      <Typography variant="caption" color="text.secondary">
                                        Since {new Date(membership.start_date).toLocaleDateString()}
                                      </Typography>
                                    )}
                                  </Box>
                                }
                              />
                            </ListItem>
                          ))}
                      </List>
                    </Box>
                  )}

                  {/* Subcommittees */}
                  {displayData.committee_memberships.filter(cm => cm.committee.is_subcommittee).length > 0 && (
                    <Box>
                      <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                        <AssignmentIcon sx={{ mr: 1, fontSize: 20 }} />
                        Subcommittees
                      </Typography>
                      <List>
                        {displayData.committee_memberships
                          .filter(cm => cm.committee.is_subcommittee)
                          .map((membership, index) => (
                            <ListItem
                              key={`sub-${index}`}
                              sx={{
                                border: '1px solid #e0e0e0',
                                borderRadius: 1,
                                mb: 1,
                                ml: 2,
                                '&:hover': {
                                  backgroundColor: '#f5f5f5',
                                  cursor: 'pointer',
                                },
                              }}
                              onClick={() => navigate(`/committees/${membership.committee.id}`)}
                            >
                              <ListItemAvatar>
                                <Avatar sx={{ bgcolor: 'grey.300' }}>
                                  {membership.position === 'Chair' || membership.position === 'Chairwoman' || membership.position === 'Chairman' ? (
                                    <GavelIcon />
                                  ) : membership.position === 'Ranking Member' ? (
                                    <StarIcon />
                                  ) : (
                                    <AssignmentIcon />
                                  )}
                                </Avatar>
                              </ListItemAvatar>
                              <ListItemText
                                primary={
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Typography variant="body1">
                                      {membership.committee.name}
                                    </Typography>
                                    {(membership.position === 'Chair' || membership.position === 'Chairwoman' || membership.position === 'Chairman') && (
                                      <Tooltip title="Subcommittee Chair">
                                        <GavelIcon color="warning" fontSize="small" />
                                      </Tooltip>
                                    )}
                                    {membership.position === 'Ranking Member' && (
                                      <Tooltip title="Ranking Member">
                                        <StarIcon color="primary" fontSize="small" />
                                      </Tooltip>
                                    )}
                                  </Box>
                                }
                                secondary={
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1, flexWrap: 'wrap' }}>
                                    <Chip
                                      label={membership.position}
                                      size="small"
                                      color={getPositionColor(membership.position)}
                                    />
                                    <Chip
                                      label="Subcommittee"
                                      size="small"
                                      variant="outlined"
                                    />
                                    <Chip
                                      label={membership.is_current ? 'Current' : 'Former'}
                                      size="small"
                                      color={membership.is_current ? 'success' : 'default'}
                                    />
                                    {membership.start_date && (
                                      <Typography variant="caption" color="text.secondary">
                                        Since {new Date(membership.start_date).toLocaleDateString()}
                                      </Typography>
                                    )}
                                  </Box>
                                }
                              />
                            </ListItem>
                          ))}
                      </List>
                    </Box>
                  )}
                </Box>
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