// Congressional Session Service
// Handles current Congressional session data and context

export interface CongressionalSession {
  sessionId: number;
  congressNumber: number;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
  partyControlHouse: 'Republican' | 'Democratic' | null;
  partyControlSenate: 'Republican' | 'Democratic' | null;
  displayName: string;
  dateRange: string;
}

export interface CongressionalSessionContextProps {
  currentSession: CongressionalSession;
  isUnifiedGovernment: boolean;
  majorityParty: 'Republican' | 'Democratic' | null;
  sessionTransition?: {
    nextCongress: number;
    transitionDate: string;
  };
}

// Current 119th Congress session data
export const CURRENT_CONGRESSIONAL_SESSION: CongressionalSession = {
  sessionId: 119,
  congressNumber: 119,
  startDate: '2025-01-03',
  endDate: '2027-01-03',
  isCurrent: true,
  partyControlHouse: 'Republican',
  partyControlSenate: 'Republican',
  displayName: '119th Congress',
  dateRange: '2025-2027'
};

// Get current Congressional session context
export const getCurrentSessionContext = (): CongressionalSessionContextProps => {
  const session = CURRENT_CONGRESSIONAL_SESSION;
  
  return {
    currentSession: session,
    isUnifiedGovernment: session.partyControlHouse === session.partyControlSenate,
    majorityParty: session.partyControlHouse, // Since both chambers are Republican
    sessionTransition: {
      nextCongress: 120,
      transitionDate: '2027-01-03'
    }
  };
};

// Get Congressional session display string
export const getSessionDisplayString = (): string => {
  const session = CURRENT_CONGRESSIONAL_SESSION;
  return `${session.displayName} (${session.dateRange})`;
};

// Get party control summary
export const getPartyControlSummary = (): string => {
  const session = CURRENT_CONGRESSIONAL_SESSION;
  if (session.partyControlHouse === session.partyControlSenate) {
    return `${session.partyControlHouse} Unified Control`;
  }
  return `${session.partyControlHouse} House, ${session.partyControlSenate} Senate`;
};

// Check if session is current
export const isCurrentSession = (congressNumber: number): boolean => {
  return congressNumber === CURRENT_CONGRESSIONAL_SESSION.congressNumber;
};

// Get leadership context based on party control
export const getLeadershipContext = () => {
  const session = CURRENT_CONGRESSIONAL_SESSION;
  return {
    houseMajority: session.partyControlHouse,
    senateMajority: session.partyControlSenate,
    isUnified: session.partyControlHouse === session.partyControlSenate,
    committeesControlledBy: session.partyControlSenate // Senate committees 
  };
};

const congressionalSessionService = {
  getCurrentSessionContext,
  getSessionDisplayString,
  getPartyControlSummary,
  isCurrentSession,
  getLeadershipContext,
  CURRENT_CONGRESSIONAL_SESSION
};

export default congressionalSessionService;