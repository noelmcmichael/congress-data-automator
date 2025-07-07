import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Box,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Group as GroupIcon,
  Event as EventIcon,
  Settings as SettingsIcon,
  AccountBalance as CapitolIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

const navigationItems = [
  { path: '/', label: 'Dashboard', icon: <DashboardIcon /> },
  { path: '/members', label: 'Members', icon: <PeopleIcon /> },
  { path: '/committees', label: 'Committees', icon: <GroupIcon /> },
  { path: '/hearings', label: 'Hearings', icon: <EventIcon /> },
  { path: '/senator-timeline', label: 'Senator Timeline', icon: <ScheduleIcon /> },
  { path: '/settings', label: 'Settings', icon: <SettingsIcon /> },
];

const Navigation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CapitolIcon color="primary" />
          <Typography variant="h6" noWrap component="div">
            Congress Data
          </Typography>
        </Box>
      </Toolbar>
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {navigationItems.map((item) => (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => handleNavigation(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default Navigation;