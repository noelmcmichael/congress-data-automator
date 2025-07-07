import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Group as GroupIcon,
  Person as PersonIcon,
  Star as StarIcon,
  AccountBalance as CapitolIcon,
  Visibility as VisibilityIcon,
  NavigateNext as NavigateNextIcon,
} from '@mui/icons-material';
import { apiService, Committee } from '../services/api';

interface CommitteeHierarchyMember {
  id: number;
  first_name: string;
  last_name: string;
  party: string;
  state: string;
  chamber: string;
  district: string | null;
  position: string;
  is_current: boolean;
  official_photo_url: string | null;
}

interface CommitteeHierarchyData {
  committee: Committee;
  members: CommitteeHierarchyMember[];
  subcommittees: Array<{
    id: number;
    name: string;
    chamber: string;
    committee_type: string;
    is_subcommittee: boolean;
    parent_committee_id: number;
    jurisdiction: string | null;
    chair_member_id: number | null;
    ranking_member_id: number | null;
    is_active: boolean;
    members: CommitteeHierarchyMember[];
    member_count: number;
  }>;
  statistics: {
    total_members: number;
    total_subcommittees: number;
    party_breakdown: Record<string, number>;
    leadership_positions: number;
    total_subcommittee_members: number;
  };
}

interface StandingCommittee {
  id: number;
  name: string;
  chamber: string;
  committee_type: string;
  is_subcommittee: boolean;
  is_active: boolean;
  member_count?: number;
  subcommittee_count?: number;
}

const CommitteeHierarchy: React.FC = () => {
  const navigate = useNavigate();
  const [standingCommittees, setStandingCommittees] = useState<StandingCommittee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedCommittees, setExpandedCommittees] = useState<Set<number>>(new Set());
  const [committeeHierarchyData, setCommitteeHierarchyData] = useState<Record<number, CommitteeHierarchyData>>({});

  useEffect(() => {
    fetchStandingCommittees();
  }, []);

  const fetchStandingCommittees = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get all committees and filter for standing committees (non-subcommittees)
      const response = await fetch('https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees?limit=200&active_only=true');
      if (!response.ok) {
        throw new Error('Failed to fetch committees');
      }
      
      const committees = await response.json();
      
      // Filter for standing committees (non-subcommittees) and sort by chamber and name
      const standing = committees
        .filter((committee: Committee) => !committee.is_subcommittee)
        .sort((a: Committee, b: Committee) => {
          if (a.chamber !== b.chamber) {
            return a.chamber.localeCompare(b.chamber);
          }
          return a.name.localeCompare(b.name);
        });
      
      setStandingCommittees(standing);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch standing committees');
    } finally {
      setLoading(false);
    }
  };

  const fetchCommitteeHierarchy = async (committeeId: number) => {
    try {
      // First, try the hierarchy endpoint
      let response = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/${committeeId}/hierarchy`);
      
      if (response.ok) {
        const data = await response.json();
        setCommitteeHierarchyData(prev => ({ ...prev, [committeeId]: data }));
        return;
      }
      
      // If hierarchy endpoint doesn't exist, build hierarchy data manually
      const [detailResponse, subcommitteesResponse, membersResponse] = await Promise.all([
        fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/${committeeId}`),
        fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/${committeeId}/subcommittees`),
        fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/${committeeId}/members`)
      ]);
      
      if (!detailResponse.ok || !subcommitteesResponse.ok || !membersResponse.ok) {
        throw new Error('Failed to fetch committee hierarchy data');
      }
      
      const [committee, subcommittees, members] = await Promise.all([
        detailResponse.json(),
        subcommitteesResponse.json(),
        membersResponse.json()
      ]);
      
      // Build enhanced subcommittees data
      const enhancedSubcommittees = await Promise.all(
        subcommittees.map(async (subcommittee: Committee) => {
          const subMembersResponse = await fetch(`https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/${subcommittee.id}/members`);
          const subMembers = subMembersResponse.ok ? await subMembersResponse.json() : [];
          
          return {
            ...subcommittee,
            members: subMembers.map((cm: any) => ({
              id: cm.member.id,
              first_name: cm.member.first_name,
              last_name: cm.member.last_name,
              party: cm.member.party,
              state: cm.member.state,
              chamber: cm.member.chamber,
              district: cm.member.district,
              position: cm.position,
              is_current: cm.is_current,
              official_photo_url: cm.member.official_photo_url
            })),
            member_count: subMembers.length
          };
        })
      );
      
      // Build statistics
      const allMembers = [
        ...members.map((cm: any) => cm.member),
        ...enhancedSubcommittees.flatMap(sub => sub.members)
      ];
      
      const partyBreakdown = allMembers.reduce((acc: Record<string, number>, member: any) => {
        acc[member.party] = (acc[member.party] || 0) + 1;
        return acc;
      }, {});
      
      const hierarchyData: CommitteeHierarchyData = {
        committee,
        members: members.map((cm: any) => ({
          id: cm.member.id,
          first_name: cm.member.first_name,
          last_name: cm.member.last_name,
          party: cm.member.party,
          state: cm.member.state,
          chamber: cm.member.chamber,
          district: cm.member.district,
          position: cm.position,
          is_current: cm.is_current,
          official_photo_url: cm.member.official_photo_url
        })),
        subcommittees: enhancedSubcommittees,
        statistics: {
          total_members: members.length,
          total_subcommittees: enhancedSubcommittees.length,
          party_breakdown: partyBreakdown,
          leadership_positions: members.filter((cm: any) => cm.position && ['Chair', 'Ranking Member', 'Chairwoman', 'Chairman'].includes(cm.position)).length,
          total_subcommittee_members: enhancedSubcommittees.reduce((sum, sub) => sum + sub.member_count, 0)
        }
      };
      
      setCommitteeHierarchyData(prev => ({ ...prev, [committeeId]: hierarchyData }));
    } catch (err) {
      console.error('Error fetching committee hierarchy:', err);
    }
  };

  const handleCommitteeExpand = (committeeId: number) => {
    const newExpanded = new Set(expandedCommittees);
    if (newExpanded.has(committeeId)) {
      newExpanded.delete(committeeId);
    } else {
      newExpanded.add(committeeId);
      if (!committeeHierarchyData[committeeId]) {
        fetchCommitteeHierarchy(committeeId);
      }
    }
    setExpandedCommittees(newExpanded);
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
      case 'chairman':
      case 'chairwoman':
        return 'primary';
      case 'ranking member':
        return 'secondary';
      default:
        return 'default';
    }
  };

  const renderMemberItem = (member: CommitteeHierarchyMember, isSubcommittee: boolean = false) => (
    <ListItem
      key={member.id}
      sx={{
        border: '1px solid #e0e0e0',
        borderRadius: 1,
        mb: 1,
        backgroundColor: isSubcommittee ? '#f9f9f9' : 'white',
        '&:hover': {
          backgroundColor: isSubcommittee ? '#f0f0f0' : '#f5f5f5',
          cursor: 'pointer',
        },
      }}
      onClick={() => navigate(`/members/${member.id}`)}
    >
      <ListItemAvatar>
        <Avatar src={member.official_photo_url || undefined} sx={{ width: 40, height: 40 }}>
          <PersonIcon />
        </Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={`${member.first_name} ${member.last_name}`}
        secondary={
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
            {member.position && (
              <Chip
                label={member.position}
                size="small"
                color={getPositionColor(member.position)}
                icon={member.position.toLowerCase().includes('chair') ? <StarIcon /> : undefined}
              />
            )}
            <Chip
              label={member.party}
              size="small"
              sx={{
                backgroundColor: getPartyColor(member.party),
                color: 'white',
              }}
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
      <IconButton
        size="small"
        onClick={(e) => {
          e.stopPropagation();
          navigate(`/members/${member.id}`);
        }}
      >
        <VisibilityIcon />
      </IconButton>
    </ListItem>
  );

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
          Loading committee hierarchy...
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

  // Group committees by chamber
  const houseCommittees = standingCommittees.filter(c => c.chamber === 'House');
  const senateCommittees = standingCommittees.filter(c => c.chamber === 'Senate');
  const jointCommittees = standingCommittees.filter(c => c.chamber === 'Joint');

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <CapitolIcon sx={{ mr: 2, fontSize: 32 }} color="primary" />
        <Typography variant="h4" component="h1">
          Committee Hierarchy
        </Typography>
      </Box>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Explore the complete structure of Congressional committees, their subcommittees, and member assignments.
      </Typography>

      <Grid container spacing={3}>
        {/* House Committees */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <GroupIcon sx={{ mr: 1 }} />
                House Committees
                <Chip label={houseCommittees.length} size="small" sx={{ ml: 1 }} />
              </Typography>
              
              {houseCommittees.map((committee) => (
                <Accordion 
                  key={committee.id}
                  expanded={expandedCommittees.has(committee.id)}
                  onChange={() => handleCommitteeExpand(committee.id)}
                >
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                      <Avatar sx={{ mr: 2, width: 32, height: 32 }}>
                        <GroupIcon />
                      </Avatar>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                          {committee.name}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                          <Chip label="House" size="small" color="primary" />
                          {committee.is_active && (
                            <Chip label="Active" size="small" color="success" />
                          )}
                        </Box>
                      </Box>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/committees/${committee.id}`);
                        }}
                      >
                        <VisibilityIcon />
                      </IconButton>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    {committeeHierarchyData[committee.id] ? (
                      <Box>
                        {/* Committee Statistics */}
                        <Grid container spacing={2} sx={{ mb: 2 }}>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="primary">
                                {committeeHierarchyData[committee.id].statistics.total_members}
                              </Typography>
                              <Typography variant="caption">Members</Typography>
                            </Paper>
                          </Grid>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="secondary">
                                {committeeHierarchyData[committee.id].statistics.total_subcommittees}
                              </Typography>
                              <Typography variant="caption">Subcommittees</Typography>
                            </Paper>
                          </Grid>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="success.main">
                                {committeeHierarchyData[committee.id].statistics.leadership_positions}
                              </Typography>
                              <Typography variant="caption">Leadership</Typography>
                            </Paper>
                          </Grid>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="info.main">
                                {committeeHierarchyData[committee.id].statistics.total_subcommittee_members}
                              </Typography>
                              <Typography variant="caption">Sub Members</Typography>
                            </Paper>
                          </Grid>
                        </Grid>

                        {/* Committee Members */}
                        <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                          Committee Members
                        </Typography>
                        <List dense sx={{ maxHeight: 300, overflow: 'auto' }}>
                          {committeeHierarchyData[committee.id].members.map((member) => 
                            renderMemberItem(member, false)
                          )}
                        </List>

                        {/* Subcommittees */}
                        {committeeHierarchyData[committee.id].subcommittees.length > 0 && (
                          <Box sx={{ mt: 2 }}>
                            <Typography variant="subtitle2" gutterBottom>
                              Subcommittees
                            </Typography>
                            {committeeHierarchyData[committee.id].subcommittees.map((subcommittee) => (
                              <Box key={subcommittee.id} sx={{ mb: 2, pl: 2, borderLeft: '2px solid #e0e0e0' }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                  <Typography variant="body2" sx={{ fontWeight: 'bold', flexGrow: 1 }}>
                                    {subcommittee.name}
                                  </Typography>
                                  <Chip label={`${subcommittee.member_count} members`} size="small" />
                                  <IconButton
                                    size="small"
                                    onClick={() => navigate(`/committees/${subcommittee.id}`)}
                                    sx={{ ml: 1 }}
                                  >
                                    <VisibilityIcon />
                                  </IconButton>
                                </Box>
                                <List dense>
                                  {subcommittee.members.slice(0, 3).map((member) => 
                                    renderMemberItem(member, true)
                                  )}
                                  {subcommittee.members.length > 3 && (
                                    <Typography variant="caption" sx={{ ml: 2 }}>
                                      ... and {subcommittee.members.length - 3} more members
                                    </Typography>
                                  )}
                                </List>
                              </Box>
                            ))}
                          </Box>
                        )}
                      </Box>
                    ) : (
                      <Box sx={{ textAlign: 'center', py: 2 }}>
                        <LinearProgress sx={{ mb: 2 }} />
                        <Typography variant="body2">Loading committee details...</Typography>
                      </Box>
                    )}
                  </AccordionDetails>
                </Accordion>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Senate Committees */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <GroupIcon sx={{ mr: 1 }} />
                Senate Committees
                <Chip label={senateCommittees.length} size="small" sx={{ ml: 1 }} />
              </Typography>
              
              {senateCommittees.map((committee) => (
                <Accordion 
                  key={committee.id}
                  expanded={expandedCommittees.has(committee.id)}
                  onChange={() => handleCommitteeExpand(committee.id)}
                >
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                      <Avatar sx={{ mr: 2, width: 32, height: 32 }}>
                        <GroupIcon />
                      </Avatar>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                          {committee.name}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                          <Chip label="Senate" size="small" color="secondary" />
                          {committee.is_active && (
                            <Chip label="Active" size="small" color="success" />
                          )}
                        </Box>
                      </Box>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/committees/${committee.id}`);
                        }}
                      >
                        <VisibilityIcon />
                      </IconButton>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    {committeeHierarchyData[committee.id] ? (
                      <Box>
                        {/* Committee Statistics */}
                        <Grid container spacing={2} sx={{ mb: 2 }}>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="primary">
                                {committeeHierarchyData[committee.id].statistics.total_members}
                              </Typography>
                              <Typography variant="caption">Members</Typography>
                            </Paper>
                          </Grid>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="secondary">
                                {committeeHierarchyData[committee.id].statistics.total_subcommittees}
                              </Typography>
                              <Typography variant="caption">Subcommittees</Typography>
                            </Paper>
                          </Grid>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="success.main">
                                {committeeHierarchyData[committee.id].statistics.leadership_positions}
                              </Typography>
                              <Typography variant="caption">Leadership</Typography>
                            </Paper>
                          </Grid>
                          <Grid item xs={3}>
                            <Paper sx={{ p: 1, textAlign: 'center' }}>
                              <Typography variant="h6" color="info.main">
                                {committeeHierarchyData[committee.id].statistics.total_subcommittee_members}
                              </Typography>
                              <Typography variant="caption">Sub Members</Typography>
                            </Paper>
                          </Grid>
                        </Grid>

                        {/* Committee Members */}
                        <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                          Committee Members
                        </Typography>
                        <List dense sx={{ maxHeight: 300, overflow: 'auto' }}>
                          {committeeHierarchyData[committee.id].members.map((member) => 
                            renderMemberItem(member, false)
                          )}
                        </List>

                        {/* Subcommittees */}
                        {committeeHierarchyData[committee.id].subcommittees.length > 0 && (
                          <Box sx={{ mt: 2 }}>
                            <Typography variant="subtitle2" gutterBottom>
                              Subcommittees
                            </Typography>
                            {committeeHierarchyData[committee.id].subcommittees.map((subcommittee) => (
                              <Box key={subcommittee.id} sx={{ mb: 2, pl: 2, borderLeft: '2px solid #e0e0e0' }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                  <Typography variant="body2" sx={{ fontWeight: 'bold', flexGrow: 1 }}>
                                    {subcommittee.name}
                                  </Typography>
                                  <Chip label={`${subcommittee.member_count} members`} size="small" />
                                  <IconButton
                                    size="small"
                                    onClick={() => navigate(`/committees/${subcommittee.id}`)}
                                    sx={{ ml: 1 }}
                                  >
                                    <VisibilityIcon />
                                  </IconButton>
                                </Box>
                                <List dense>
                                  {subcommittee.members.slice(0, 3).map((member) => 
                                    renderMemberItem(member, true)
                                  )}
                                  {subcommittee.members.length > 3 && (
                                    <Typography variant="caption" sx={{ ml: 2 }}>
                                      ... and {subcommittee.members.length - 3} more members
                                    </Typography>
                                  )}
                                </List>
                              </Box>
                            ))}
                          </Box>
                        )}
                      </Box>
                    ) : (
                      <Box sx={{ textAlign: 'center', py: 2 }}>
                        <LinearProgress sx={{ mb: 2 }} />
                        <Typography variant="body2">Loading committee details...</Typography>
                      </Box>
                    )}
                  </AccordionDetails>
                </Accordion>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Joint Committees */}
        {jointCommittees.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  Joint Committees
                  <Chip label={jointCommittees.length} size="small" sx={{ ml: 1 }} />
                </Typography>
                
                {jointCommittees.map((committee) => (
                  <Accordion 
                    key={committee.id}
                    expanded={expandedCommittees.has(committee.id)}
                    onChange={() => handleCommitteeExpand(committee.id)}
                  >
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <Avatar sx={{ mr: 2, width: 32, height: 32 }}>
                          <GroupIcon />
                        </Avatar>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                            {committee.name}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                            <Chip label="Joint" size="small" color="success" />
                            {committee.is_active && (
                              <Chip label="Active" size="small" color="success" />
                            )}
                          </Box>
                        </Box>
                        <IconButton
                          size="small"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/committees/${committee.id}`);
                          }}
                        >
                          <VisibilityIcon />
                        </IconButton>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      {committeeHierarchyData[committee.id] ? (
                        <Box>
                          {/* Committee Statistics */}
                          <Grid container spacing={2} sx={{ mb: 2 }}>
                            <Grid item xs={3}>
                              <Paper sx={{ p: 1, textAlign: 'center' }}>
                                <Typography variant="h6" color="primary">
                                  {committeeHierarchyData[committee.id].statistics.total_members}
                                </Typography>
                                <Typography variant="caption">Members</Typography>
                              </Paper>
                            </Grid>
                            <Grid item xs={3}>
                              <Paper sx={{ p: 1, textAlign: 'center' }}>
                                <Typography variant="h6" color="secondary">
                                  {committeeHierarchyData[committee.id].statistics.total_subcommittees}
                                </Typography>
                                <Typography variant="caption">Subcommittees</Typography>
                              </Paper>
                            </Grid>
                            <Grid item xs={3}>
                              <Paper sx={{ p: 1, textAlign: 'center' }}>
                                <Typography variant="h6" color="success.main">
                                  {committeeHierarchyData[committee.id].statistics.leadership_positions}
                                </Typography>
                                <Typography variant="caption">Leadership</Typography>
                              </Paper>
                            </Grid>
                            <Grid item xs={3}>
                              <Paper sx={{ p: 1, textAlign: 'center' }}>
                                <Typography variant="h6" color="info.main">
                                  {committeeHierarchyData[committee.id].statistics.total_subcommittee_members}
                                </Typography>
                                <Typography variant="caption">Sub Members</Typography>
                              </Paper>
                            </Grid>
                          </Grid>

                          {/* Committee Members */}
                          <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                            Committee Members
                          </Typography>
                          <List dense sx={{ maxHeight: 300, overflow: 'auto' }}>
                            {committeeHierarchyData[committee.id].members.map((member) => 
                              renderMemberItem(member, false)
                            )}
                          </List>

                          {/* Subcommittees */}
                          {committeeHierarchyData[committee.id].subcommittees.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="subtitle2" gutterBottom>
                                Subcommittees
                              </Typography>
                              {committeeHierarchyData[committee.id].subcommittees.map((subcommittee) => (
                                <Box key={subcommittee.id} sx={{ mb: 2, pl: 2, borderLeft: '2px solid #e0e0e0' }}>
                                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                    <Typography variant="body2" sx={{ fontWeight: 'bold', flexGrow: 1 }}>
                                      {subcommittee.name}
                                    </Typography>
                                    <Chip label={`${subcommittee.member_count} members`} size="small" />
                                    <IconButton
                                      size="small"
                                      onClick={() => navigate(`/committees/${subcommittee.id}`)}
                                      sx={{ ml: 1 }}
                                    >
                                      <VisibilityIcon />
                                    </IconButton>
                                  </Box>
                                  <List dense>
                                    {subcommittee.members.slice(0, 3).map((member) => 
                                      renderMemberItem(member, true)
                                    )}
                                    {subcommittee.members.length > 3 && (
                                      <Typography variant="caption" sx={{ ml: 2 }}>
                                        ... and {subcommittee.members.length - 3} more members
                                      </Typography>
                                    )}
                                  </List>
                                </Box>
                              ))}
                            </Box>
                          )}
                        </Box>
                      ) : (
                        <Box sx={{ textAlign: 'center', py: 2 }}>
                          <LinearProgress sx={{ mb: 2 }} />
                          <Typography variant="body2">Loading committee details...</Typography>
                        </Box>
                      )}
                    </AccordionDetails>
                  </Accordion>
                ))}
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default CommitteeHierarchy;