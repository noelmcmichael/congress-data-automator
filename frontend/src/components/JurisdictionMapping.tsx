import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
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
  Tabs,
  Tab,
  TextField,
  InputAdornment,
  Alert,
  Divider,
  Stack,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Group as GroupIcon,
  Person as PersonIcon,
  AccountBalance as CapitolIcon,
  Search as SearchIcon,
  Gavel as GavelIcon,
  Business as BusinessIcon,
  Security as SecurityIcon,
  HealthAndSafety as HealthIcon,
  Bolt as EnergyIcon,
  School as EducationIcon,
  Agriculture as AgricultureIcon,
  Public as PublicIcon,
  Flight as TransportIcon,
  AccountTree as HierarchyIcon,
  Category as CategoryIcon,
} from '@mui/icons-material';
import {
  jurisdictionAreas,
  committeeJurisdictions,
  getCommitteeJurisdiction,
  getCommitteesByJurisdiction,
  getAllJurisdictionAreas,
  getOverlapAnalysis,
  type JurisdictionArea,
  type CommitteeJurisdiction,
} from '../data/committeeJurisdictions';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`jurisdiction-tabpanel-${index}`}
      aria-labelledby={`jurisdiction-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const JurisdictionMapping: React.FC = () => {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedJurisdiction, setSelectedJurisdiction] = useState<string | null>(null);
  const [committees, setCommittees] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCommittees();
  }, []);

  const fetchCommittees = async () => {
    try {
      setLoading(true);
      const response = await fetch('https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees?limit=200&active_only=true');
      if (response.ok) {
        const data = await response.json();
        setCommittees(data.filter((c: any) => !c.is_subcommittee));
      }
    } catch (error) {
      console.error('Error fetching committees:', error);
    } finally {
      setLoading(false);
    }
  };

  const getJurisdictionIcon = (jurisdictionId: string) => {
    switch (jurisdictionId) {
      case 'agriculture': return <AgricultureIcon />;
      case 'appropriations': return <BusinessIcon />;
      case 'armed_services': return <SecurityIcon />;
      case 'banking': return <BusinessIcon />;
      case 'energy': return <EnergyIcon />;
      case 'foreign_affairs': return <PublicIcon />;
      case 'healthcare': return <HealthIcon />;
      case 'homeland_security': return <SecurityIcon />;
      case 'judiciary': return <GavelIcon />;
      case 'transportation': return <TransportIcon />;
      case 'education': return <EducationIcon />;
      case 'veterans': return <SecurityIcon />;
      case 'small_business': return <BusinessIcon />;
      case 'science_technology': return <CategoryIcon />;
      case 'intelligence': return <SecurityIcon />;
      default: return <GroupIcon />;
    }
  };

  const getJurisdictionColor = (jurisdictionId: string) => {
    const colors: Record<string, string> = {
      agriculture: '#4caf50',
      appropriations: '#2196f3',
      armed_services: '#f44336',
      banking: '#ff9800',
      energy: '#8bc34a',
      foreign_affairs: '#9c27b0',
      healthcare: '#e91e63',
      homeland_security: '#607d8b',
      judiciary: '#795548',
      transportation: '#00bcd4',
      education: '#3f51b5',
      veterans: '#ff5722',
      small_business: '#ffc107',
      science_technology: '#673ab7',
      intelligence: '#424242',
    };
    return colors[jurisdictionId] || '#757575';
  };

  const getChamberColor = (chamber: string) => {
    switch (chamber.toLowerCase()) {
      case 'house': return 'primary';
      case 'senate': return 'secondary';
      case 'joint': return 'success';
      default: return 'default';
    }
  };

  const filteredJurisdictions = jurisdictionAreas.filter(ja =>
    ja.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ja.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredCommittees = committeeJurisdictions.filter(cj =>
    cj.committee_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    cj.primary_oversight.some(po => po.toLowerCase().includes(searchQuery.toLowerCase())) ||
    cj.key_agencies.some(ka => ka.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const overlapAnalysis = getOverlapAnalysis();

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setSearchQuery('');
    setSelectedJurisdiction(null);
  };

  const renderJurisdictionCard = (jurisdiction: JurisdictionArea) => {
    const relatedCommittees = getCommitteesByJurisdiction(jurisdiction.id);
    
    return (
      <Card key={jurisdiction.id} sx={{ height: '100%' }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar 
              sx={{ 
                backgroundColor: getJurisdictionColor(jurisdiction.id),
                mr: 2,
                width: 56,
                height: 56
              }}
            >
              {getJurisdictionIcon(jurisdiction.id)}
            </Avatar>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h6" component="h3">
                {jurisdiction.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {jurisdiction.description}
              </Typography>
            </Box>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Typography variant="subtitle2" gutterBottom>
            Key Agencies
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
            {jurisdiction.agencies?.slice(0, 4).map((agency, index) => (
              <Chip key={index} label={agency} size="small" variant="outlined" />
            ))}
            {jurisdiction.agencies && jurisdiction.agencies.length > 4 && (
              <Chip label={`+${jurisdiction.agencies.length - 4} more`} size="small" />
            )}
          </Box>

          <Typography variant="subtitle2" gutterBottom>
            Congressional Committees
          </Typography>
          <List dense>
            {relatedCommittees.slice(0, 2).map((committee, index) => (
              <ListItem 
                key={index}
                sx={{ 
                  px: 0,
                  '&:hover': { backgroundColor: '#f5f5f5', cursor: 'pointer' }
                }}
                onClick={() => {
                  const actualCommittee = committees.find(c => 
                    c.name.includes(committee.committee_name.replace('Committee on ', ''))
                  );
                  if (actualCommittee) {
                    navigate(`/committees/${actualCommittee.id}`);
                  }
                }}
              >
                <ListItemAvatar>
                  <Avatar sx={{ width: 32, height: 32 }}>
                    <GroupIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={committee.committee_name.replace('Committee on ', '')}
                  secondary={
                    <Chip 
                      label={committee.chamber} 
                      size="small" 
                      color={getChamberColor(committee.chamber)}
                    />
                  }
                />
              </ListItem>
            ))}
            {relatedCommittees.length > 2 && (
              <Typography variant="caption" sx={{ ml: 1 }}>
                +{relatedCommittees.length - 2} more committees
              </Typography>
            )}
          </List>
        </CardContent>
      </Card>
    );
  };

  const renderCommitteeJurisdiction = (committee: CommitteeJurisdiction) => {
    const actualCommittee = committees.find(c => 
      c.name.includes(committee.committee_name.replace('Committee on ', ''))
    );

    return (
      <Accordion key={`${committee.committee_name}-${committee.chamber}`}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
            <Avatar sx={{ mr: 2, width: 40, height: 40 }}>
              <GroupIcon />
            </Avatar>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h6">
                {committee.committee_name}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                <Chip 
                  label={committee.chamber} 
                  size="small" 
                  color={getChamberColor(committee.chamber)}
                />
                <Chip 
                  label={`${committee.jurisdiction_areas.length} jurisdiction areas`} 
                  size="small" 
                  variant="outlined"
                />
              </Box>
            </Box>
            {actualCommittee && (
              <IconButton
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/committees/${actualCommittee.id}`);
                }}
              >
                <GroupIcon />
              </IconButton>
            )}
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Primary Oversight Areas
              </Typography>
              <Stack spacing={1}>
                {committee.primary_oversight.map((area, index) => (
                  <Chip key={index} label={area} size="small" />
                ))}
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Key Agencies
              </Typography>
              <Stack spacing={1}>
                {committee.key_agencies.map((agency, index) => (
                  <Chip key={index} label={agency} size="small" variant="outlined" />
                ))}
              </Stack>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Major Legislation Types
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {committee.major_legislation.map((legislation, index) => (
                  <Chip key={index} label={legislation} size="small" color="primary" />
                ))}
              </Box>
            </Grid>
            {committee.overlap_committees && committee.overlap_committees.length > 0 && (
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom>
                  Jurisdiction Overlaps
                </Typography>
                <Alert severity="info" sx={{ mt: 1 }}>
                  <Typography variant="body2">
                    This committee shares jurisdiction with: {committee.overlap_committees.join(', ')}
                  </Typography>
                </Alert>
              </Grid>
            )}
          </Grid>
        </AccordionDetails>
      </Accordion>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <HierarchyIcon sx={{ mr: 2, fontSize: 32 }} color="primary" />
        <Typography variant="h4" component="h1">
          Committee Jurisdiction Mapping
        </Typography>
      </Box>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Explore committee jurisdictions, policy areas, and agency oversight responsibilities.
      </Typography>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="jurisdiction mapping tabs">
          <Tab label="Policy Areas" />
          <Tab label="Committee Overview" />
          <Tab label="Jurisdiction Overlaps" />
        </Tabs>
      </Paper>

      <TabPanel value={tabValue} index={0}>
        <TextField
          fullWidth
          placeholder="Search policy areas..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ mb: 3 }}
        />

        <Grid container spacing={3}>
          {filteredJurisdictions.map((jurisdiction) => (
            <Grid item xs={12} md={6} lg={4} key={jurisdiction.id}>
              {renderJurisdictionCard(jurisdiction)}
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <TextField
          fullWidth
          placeholder="Search committees, agencies, or oversight areas..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ mb: 3 }}
        />

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              House Committees
            </Typography>
            {filteredCommittees
              .filter(c => c.chamber === 'House')
              .map(committee => renderCommitteeJurisdiction(committee))
            }
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Senate Committees
            </Typography>
            {filteredCommittees
              .filter(c => c.chamber === 'Senate')
              .map(committee => renderCommitteeJurisdiction(committee))
            }
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Typography variant="h6" gutterBottom>
          Jurisdiction Overlap Analysis
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Areas where multiple committees share oversight responsibilities, potentially leading to coordination challenges or comprehensive coverage.
        </Typography>

        <Grid container spacing={2}>
          {overlapAnalysis.map((overlap, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {overlap.area}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {overlap.committees.length} committees share jurisdiction
                  </Typography>
                  <List dense>
                    {overlap.committees.map((committee, idx) => (
                      <ListItem key={idx} sx={{ px: 0 }}>
                        <ListItemAvatar>
                          <Avatar sx={{ width: 32, height: 32 }}>
                            <GroupIcon />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText 
                          primary={committee}
                          primaryTypographyProps={{ variant: 'body2' }}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Alert severity="info" sx={{ mt: 3 }}>
          <Typography variant="body2">
            Jurisdiction overlaps are common in Congress and often reflect the complex, interconnected nature of policy issues. 
            These overlaps can lead to more comprehensive oversight but may also require coordination between committees.
          </Typography>
        </Alert>
      </TabPanel>
    </Box>
  );
};

export default JurisdictionMapping;