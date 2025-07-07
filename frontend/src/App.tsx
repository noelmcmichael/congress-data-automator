import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import Members from './components/Members';
import Committees from './components/Committees';
import Hearings from './components/Hearings';
import Settings from './components/Settings';
import MemberDetail from './components/MemberDetail';
import CommitteeDetail from './components/CommitteeDetail';
import HearingDetail from './components/HearingDetail';
import SenatorTimeline from './components/SenatorTimeline';
import CommitteeHierarchy from './components/CommitteeHierarchy';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', minHeight: '100vh' }}>
          <Navigation />
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              p: 3,
              ml: { sm: '240px' },
            }}
          >
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/members" element={<Members />} />
              <Route path="/members/:id" element={<MemberDetail />} />
              <Route path="/committees" element={<Committees />} />
              <Route path="/committees/:id" element={<CommitteeDetail />} />
              <Route path="/committee-hierarchy" element={<CommitteeHierarchy />} />
              <Route path="/hearings" element={<Hearings />} />
              <Route path="/hearings/:id" element={<HearingDetail />} />
              <Route path="/senator-timeline" element={<SenatorTimeline />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
