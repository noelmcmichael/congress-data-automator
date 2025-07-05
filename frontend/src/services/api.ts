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
    const response = await api.post('/api/v1/update/all', { force_refresh: forceRefresh });
    return response.data;
  },

  // Data retrieval (placeholder for when we implement these endpoints)
  async getMembers(page = 1, limit = 50): Promise<Member[]> {
    try {
      const response = await api.get(`/api/v1/members?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.warn('Members endpoint not implemented yet');
      return [];
    }
  },

  async getCommittees(page = 1, limit = 50): Promise<Committee[]> {
    try {
      const response = await api.get(`/api/v1/committees?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.warn('Committees endpoint not implemented yet');
      return [];
    }
  },

  async getHearings(page = 1, limit = 50): Promise<Hearing[]> {
    try {
      const response = await api.get(`/api/v1/hearings?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.warn('Hearings endpoint not implemented yet');
      return [];
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