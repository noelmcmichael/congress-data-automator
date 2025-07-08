import React, { useState } from 'react';
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
  IconButton,
  useTheme,
  useMediaQuery,
  AppBar,
} from '@mui/material';
import { getSessionDisplayString } from '../services/congressionalSession';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Group as GroupIcon,
  Event as EventIcon,
  Settings as SettingsIcon,
  AccountBalance as CapitolIcon,
  Schedule as ScheduleIcon,
  AccountTree as HierarchyIcon,
  Category as JurisdictionIcon,
  Search as SearchIcon,
  Menu as MenuIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

const navigationItems = [
  { path: '/', label: 'Dashboard', icon: <DashboardIcon /> },
  { path: '/members', label: 'Members', icon: <PeopleIcon /> },

  { path: '/committee-hierarchy', label: 'Committee Hierarchy', icon: <HierarchyIcon /> },
  { path: '/jurisdiction-mapping', label: 'Jurisdiction Mapping', icon: <JurisdictionIcon /> },
  { path: '/hearings', label: 'Hearings', icon: <EventIcon /> },

  { path: '/search', label: 'Advanced Search', icon: <SearchIcon /> },
  { path: '/settings', label: 'Settings', icon: <SettingsIcon /> },
];

interface NavigationProps {
  onMobileToggle?: () => void;
}

const Navigation: React.FC<NavigationProps> = ({ onMobileToggle }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('lg'));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawerContent = (
    <Box sx={{ height: '100%', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Toolbar sx={{ 
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.2)'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CapitolIcon sx={{ color: 'white', fontSize: 28 }} />
          <Box>
            <Typography variant="h6" noWrap component="div" sx={{ color: 'white', fontWeight: 600 }}>
              Congress Data
            </Typography>
            <Typography 
              variant="caption" 
              noWrap 
              component="div" 
              sx={{ 
                color: 'rgba(255, 255, 255, 0.9)', 
                fontWeight: 500,
                fontSize: '0.75rem',
                lineHeight: 1
              }}
            >
              {getSessionDisplayString()}
            </Typography>
          </Box>
        </Box>
      </Toolbar>
      <Box sx={{ overflow: 'auto', pt: 1 }}>
        <List sx={{ px: 1 }}>
          {navigationItems.map((item) => (
            <ListItem key={item.path} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => handleNavigation(item.path)}
                sx={{
                  borderRadius: 2,
                  color: 'rgba(255, 255, 255, 0.8)',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    color: 'white',
                    transform: 'translateX(4px)',
                    transition: 'all 0.3s ease-in-out',
                  },
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.25)',
                    },
                  },
                  transition: 'all 0.3s ease-in-out',
                }}
              >
                <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText 
                  primary={item.label} 
                  primaryTypographyProps={{ 
                    fontSize: 14,
                    fontWeight: location.pathname === item.path ? 600 : 500
                  }} 
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );

  return (
    <>
      {isMobile && (
        <AppBar 
          position="fixed" 
          sx={{ 
            zIndex: theme.zIndex.drawer + 1,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
          }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CapitolIcon />
              <Box>
                <Typography variant="h6" noWrap component="div">
                  Congress Data
                </Typography>
                <Typography 
                  variant="caption" 
                  noWrap 
                  component="div" 
                  sx={{ 
                    color: 'rgba(255, 255, 255, 0.9)', 
                    fontWeight: 500,
                    fontSize: '0.7rem',
                    lineHeight: 1,
                    mt: -0.5
                  }}
                >
                  {getSessionDisplayString()}
                </Typography>
              </Box>
            </Box>
          </Toolbar>
        </AppBar>
      )}
      
      <Drawer
        variant={isMobile ? 'temporary' : 'permanent'}
        open={isMobile ? mobileOpen : true}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            border: 'none',
            boxShadow: isMobile ? '0 8px 32px rgba(0, 0, 0, 0.3)' : '0 4px 20px rgba(0, 0, 0, 0.1)',
          },
        }}
      >
        {drawerContent}
      </Drawer>
    </>
  );
};

export default Navigation;