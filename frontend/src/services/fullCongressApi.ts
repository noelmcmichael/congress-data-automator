/**
 * API service demonstrating full Congress functionality with 535 members
 */
import { Member, Committee, Hearing } from './api';

// Import the full Congress dataset
import fullCongressMembers from '../data/fullCongressMembers.json';
import realCommittees from '../data/realCommittees.json';
import realHearings from '../data/realHearings.json';

export const fullCongressApiService = {
  // Enhanced members data with full Congress (535 members)
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
    
    let members = fullCongressMembers as any[];
    
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
    
    let committees = realCommittees as any[];
    
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
    return committees.slice(start, end) as Committee[];
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
    
    let hearings = realHearings as any[];
    
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
    return hearings.slice(start, end) as Hearing[];
  },

  // Statistics for the full Congress
  async getDatabaseStats() {
    const allMembers = fullCongressMembers as any[];
    const allCommittees = realCommittees as any[];
    const allHearings = realHearings as any[];
    
    return {
      members: {
        total: allMembers.length,
        house: allMembers.filter(m => m.chamber === 'House').length,
        senate: allMembers.filter(m => m.chamber === 'Senate').length,
        current: allMembers.filter(m => m.is_current).length,
      },
      committees: {
        total: allCommittees.length,
        house: allCommittees.filter(c => c.chamber === 'House').length,
        senate: allCommittees.filter(c => c.chamber === 'Senate').length,
        active: allCommittees.filter(c => c.is_active).length,
        subcommittees: allCommittees.filter(c => c.is_subcommittee).length,
      },
      hearings: {
        total: allHearings.length,
        scheduled: allHearings.filter(h => h.status === 'Scheduled').length,
        completed: allHearings.filter(h => h.status === 'Completed').length,
      },
    };
  },

  // Enhanced statistics with party breakdowns
  async getDetailedStats() {
    const allMembers = fullCongressMembers as any[];
    
    const partyBreakdown = {
      house: {
        D: allMembers.filter((m: any) => m.chamber === 'House' && m.party === 'D').length,
        R: allMembers.filter((m: any) => m.chamber === 'House' && m.party === 'R').length,
        I: allMembers.filter((m: any) => m.chamber === 'House' && m.party === 'I').length,
      },
      senate: {
        D: allMembers.filter((m: any) => m.chamber === 'Senate' && m.party === 'D').length,
        R: allMembers.filter((m: any) => m.chamber === 'Senate' && m.party === 'R').length,
        I: allMembers.filter((m: any) => m.chamber === 'Senate' && m.party === 'I').length,
      }
    };

    const stateRepresentation: any = {};
    const uniqueStates = new Set(allMembers.map((m: any) => m.state));
    const states = Array.from(uniqueStates);
    states.forEach((state: any) => {
      stateRepresentation[state] = {
        house: allMembers.filter((m: any) => m.state === state && m.chamber === 'House').length,
        senate: allMembers.filter((m: any) => m.state === state && m.chamber === 'Senate').length,
      };
    });

    return {
      ...await this.getDatabaseStats(),
      partyBreakdown,
      stateRepresentation,
      totalStates: states.length,
    };
  },
};