/**
 * API service for Congressional Data Admin UI
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://congressional-data-api-1066017671167.us-central1.run.app';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Types
export interface ApiStatus {
  api_status: string;
  congress_api_rate_limit: {
    daily_limit: number;
    daily_count: number;
    remaining: number;
    reset_time: string;
  };
  database_status: string;
  version: string;
}

export interface DatabaseStats {
  members: {
    total: number;
    house: number;
    senate: number;
    current: number;
  };
  committees: {
    total: number;
    house: number;
    senate: number;
    active: number;
    subcommittees: number;
  };
  hearings: {
    total: number;
    scheduled: number;
    completed: number;
  };
}

export interface Member {
  id: number;
  bioguide_id: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  nickname?: string;
  party: string;
  chamber: string;
  state: string;
  district?: number;
  is_current: boolean;
  official_photo_url?: string;
  created_at: string;
  updated_at?: string;
  last_scraped_at?: string;
}

export interface Committee {
  id: number;
  name: string;
  chamber: string;
  committee_code?: string;
  congress_gov_id?: string;
  is_active: boolean;
  is_subcommittee: boolean;
  parent_committee_id?: number;
  website_url?: string;
  created_at: string;
  updated_at?: string;
}

export interface Hearing {
  id: number;
  congress_gov_id?: string;
  title: string;
  description?: string;
  committee_id?: number;
  scheduled_date?: string;
  start_time?: string;
  end_time?: string;
  location?: string;
  room?: string;
  hearing_type?: string;
  status: string;
  transcript_url?: string;
  video_url?: string;
  webcast_url?: string;
  congress_session?: number;
  congress_number?: number;
  scraped_video_urls?: string[];
  created_at: string;
  updated_at?: string;
  last_scraped_at?: string;
}

// API service functions
export const apiService = {
  // Health and status
  async getHealth() {
    const response = await api.get('/health');
    return response.data;
  },

  async getStatus(): Promise<ApiStatus> {
    const response = await api.get('/api/v1/status');
    return response.data;
  },

  async getDatabaseStats(): Promise<DatabaseStats> {
    const response = await api.get('/api/v1/stats/database');
    return response.data;
  },

  // Data updates
  async updateMembers(forceRefresh = false) {
    const response = await api.post('/api/v1/update/members', { force_refresh: forceRefresh });
    return response.data;
  },

  async updateCommittees(forceRefresh = false) {
    const response = await api.post('/api/v1/update/committees', { force_refresh: forceRefresh });
    return response.data;
  },

  async updateHearings(forceRefresh = false) {
    const response = await api.post('/api/v1/update/hearings', { force_refresh: forceRefresh });
    return response.data;
  },

  async updateAllData(forceRefresh = false) {
    const response = await api.post('/api/v1/update/full', { force_refresh: forceRefresh });
    return response.data;
  },

  // Data retrieval with fallback to real data from production database
  async getMembers(params: {
    page?: number;
    limit?: number;
    search?: string;
    chamber?: string;
    state?: string;
    party?: string;
    sort_by?: string;
    sort_order?: string;
  } = {}): Promise<Member[]> {
    const { page = 1, limit = 50, search, chamber, state, party, sort_by, sort_order } = params;
    
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('page', page.toString());
      queryParams.append('limit', limit.toString());
      if (search) queryParams.append('search', search);
      if (chamber) queryParams.append('chamber', chamber);
      if (state) queryParams.append('state', state);
      if (party) queryParams.append('party', party);
      if (sort_by) queryParams.append('sort_by', sort_by);
      if (sort_order) queryParams.append('sort_order', sort_order);
      
      const response = await api.get(`/api/v1/members?${queryParams}`);
      return response.data;
    } catch (error) {
      console.warn('Members endpoint not available, using full Congress data for demonstration');
      // Import full Congress data (535 members) for demonstration
      const fullMembers = await import('../data/fullCongressMembers.json');
      let members = fullMembers.default as any[];
      
      // Apply search filter
      if (search) {
        const searchTerm = search.toLowerCase();
        members = members.filter(member => 
          member.first_name.toLowerCase().includes(searchTerm) ||
          member.last_name.toLowerCase().includes(searchTerm) ||
          (member.middle_name && member.middle_name.toLowerCase().includes(searchTerm)) ||
          (member.nickname && member.nickname.toLowerCase().includes(searchTerm))
        );
      }
      
      // Apply filters
      if (chamber) {
        members = members.filter(member => member.chamber.toLowerCase() === chamber.toLowerCase());
      }
      if (state) {
        members = members.filter(member => member.state.toLowerCase() === state.toLowerCase());
      }
      if (party) {
        members = members.filter(member => member.party.toLowerCase() === party.toLowerCase());
      }
      
      // Apply sorting
      if (sort_by) {
        const sortField = sort_by as keyof Member;
        members.sort((a, b) => {
          const aVal = a[sortField] || '';
          const bVal = b[sortField] || '';
          const comparison = aVal.toString().localeCompare(bVal.toString());
          return sort_order === 'desc' ? -comparison : comparison;
        });
      }
      
      // Apply pagination
      const start = (page - 1) * limit;
      const end = start + limit;
      return members.slice(start, end) as Member[];
    }
  },

  async getCommittees(params: {
    page?: number;
    limit?: number;
    search?: string;
    chamber?: string;
    sort_by?: string;
    sort_order?: string;
  } = {}): Promise<Committee[]> {
    const { page = 1, limit = 50, search, chamber, sort_by, sort_order } = params;
    
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('page', page.toString());
      queryParams.append('limit', limit.toString());
      if (search) queryParams.append('search', search);
      if (chamber) queryParams.append('chamber', chamber);
      if (sort_by) queryParams.append('sort_by', sort_by);
      if (sort_order) queryParams.append('sort_order', sort_order);
      
      const response = await api.get(`/api/v1/committees?${queryParams}`);
      return response.data;
    } catch (error) {
      console.warn('Committees endpoint not available, using real data from production');
      // Import real data from production database
      const realCommittees = await import('../data/realCommittees.json');
      let committees = realCommittees.default as any as Committee[];
      
      // Apply search filter
      if (search) {
        const searchTerm = search.toLowerCase();
        committees = committees.filter(committee => 
          committee.name.toLowerCase().includes(searchTerm)
        );
      }
      
      // Apply filters
      if (chamber) {
        committees = committees.filter(committee => committee.chamber.toLowerCase() === chamber.toLowerCase());
      }
      
      // Apply sorting
      if (sort_by) {
        const sortField = sort_by as keyof Committee;
        committees.sort((a, b) => {
          const aVal = a[sortField] || '';
          const bVal = b[sortField] || '';
          const comparison = aVal.toString().localeCompare(bVal.toString());
          return sort_order === 'desc' ? -comparison : comparison;
        });
      }
      
      // Apply pagination
      const start = (page - 1) * limit;
      const end = start + limit;
      return committees.slice(start, end);
    }
  },

  async getHearings(params: {
    page?: number;
    limit?: number;
    search?: string;
    status?: string;
    committee_id?: number;
    sort_by?: string;
    sort_order?: string;
  } = {}): Promise<Hearing[]> {
    const { page = 1, limit = 50, search, status, committee_id, sort_by, sort_order } = params;
    
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('page', page.toString());
      queryParams.append('limit', limit.toString());
      if (search) queryParams.append('search', search);
      if (status) queryParams.append('status', status);
      if (committee_id) queryParams.append('committee_id', committee_id.toString());
      if (sort_by) queryParams.append('sort_by', sort_by);
      if (sort_order) queryParams.append('sort_order', sort_order);
      
      const response = await api.get(`/api/v1/hearings?${queryParams}`);
      return response.data;
    } catch (error) {
      console.warn('Hearings endpoint not available, using real data from production');
      // Import real data from production database
      const realHearings = await import('../data/realHearings.json');
      let hearings = realHearings.default as any as Hearing[];
      
      // Apply search filter
      if (search) {
        const searchTerm = search.toLowerCase();
        hearings = hearings.filter(hearing => 
          hearing.title.toLowerCase().includes(searchTerm) ||
          (hearing.description && hearing.description.toLowerCase().includes(searchTerm))
        );
      }
      
      // Apply filters
      if (status) {
        hearings = hearings.filter(hearing => hearing.status.toLowerCase() === status.toLowerCase());
      }
      if (committee_id) {
        hearings = hearings.filter(hearing => hearing.committee_id === committee_id);
      }
      
      // Apply sorting
      if (sort_by) {
        const sortField = sort_by as keyof Hearing;
        hearings.sort((a, b) => {
          const aVal = a[sortField] || '';
          const bVal = b[sortField] || '';
          const comparison = aVal.toString().localeCompare(bVal.toString());
          return sort_order === 'desc' ? -comparison : comparison;
        });
      }
      
      // Apply pagination
      const start = (page - 1) * limit;
      const end = start + limit;
      return hearings.slice(start, end);
    }
  },

  // Test endpoints
  async testCongressApi() {
    const response = await api.get('/api/v1/test/congress-api');
    return response.data;
  },

  async testScrapers() {
    const response = await api.get('/api/v1/test/scrapers');
    return response.data;
  },
};

export default apiService;