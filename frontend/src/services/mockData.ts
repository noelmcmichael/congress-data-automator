/**
 * Mock data service for demonstration while API endpoints are being implemented
 */

// Generate mock members data based on known database stats (20 members: 16 House, 4 Senate)
export const mockMembers = [
  // House Members (16)
  {
    id: 1,
    bioguide_id: "A000001",
    first_name: "Nancy",
    last_name: "Pelosi",
    party: "D",
    chamber: "House",
    state: "CA",
    district: 11,
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 2,
    bioguide_id: "B000001",
    first_name: "Kevin",
    last_name: "McCarthy",
    party: "R",
    chamber: "House",
    state: "CA",
    district: 20,
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 3,
    bioguide_id: "C000001",
    first_name: "Alexandria",
    last_name: "Ocasio-Cortez",
    party: "D",
    chamber: "House",
    state: "NY",
    district: 14,
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 4,
    bioguide_id: "D000001",
    first_name: "Jim",
    last_name: "Jordan",
    party: "R",
    chamber: "House",
    state: "OH",
    district: 4,
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  // Add more House members (12 more to reach 16)
  ...Array.from({ length: 12 }, (_, i) => ({
    id: i + 5,
    bioguide_id: `H${String(i + 1).padStart(6, '0')}`,
    first_name: `Representative${i + 1}`,
    last_name: `LastName${i + 1}`,
    party: i % 2 === 0 ? "D" : "R",
    chamber: "House",
    state: ["TX", "FL", "NY", "CA", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA"][i],
    district: i + 1,
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  })),
  // Senate Members (4)
  {
    id: 17,
    bioguide_id: "S000001",
    first_name: "Chuck",
    last_name: "Schumer",
    party: "D",
    chamber: "Senate",
    state: "NY",
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 18,
    bioguide_id: "S000002",
    first_name: "Mitch",
    last_name: "McConnell",
    party: "R",
    chamber: "Senate",
    state: "KY",
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 19,
    bioguide_id: "S000003",
    first_name: "Bernie",
    last_name: "Sanders",
    party: "I",
    chamber: "Senate",
    state: "VT",
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 20,
    bioguide_id: "S000004",
    first_name: "Ted",
    last_name: "Cruz",
    party: "R",
    chamber: "Senate",
    state: "TX",
    is_current: true,
    created_at: "2025-01-04T12:00:00Z"
  }
];

// Generate mock committees data (41 committees: 17 House, 20 Senate)
export const mockCommittees = [
  // House Committees (17)
  {
    id: 1,
    name: "House Committee on Agriculture",
    chamber: "House",
    committee_code: "HSAG",
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 2,
    name: "House Committee on Appropriations",
    chamber: "House",
    committee_code: "HSAP",
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 3,
    name: "House Committee on Armed Services",
    chamber: "House",
    committee_code: "HSAS",
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  },
  // Add more House committees
  ...Array.from({ length: 14 }, (_, i) => ({
    id: i + 4,
    name: `House Committee ${i + 4}`,
    chamber: "House",
    committee_code: `HSC${i + 4}`,
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  })),
  // Senate Committees (20)
  {
    id: 18,
    name: "Senate Committee on Agriculture, Nutrition, and Forestry",
    chamber: "Senate",
    committee_code: "SSAF",
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  },
  {
    id: 19,
    name: "Senate Committee on Appropriations",
    chamber: "Senate",
    committee_code: "SSAP",
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  },
  // Add more Senate committees
  ...Array.from({ length: 18 }, (_, i) => ({
    id: i + 20,
    name: `Senate Committee ${i + 1}`,
    chamber: "Senate",
    committee_code: `SSC${i + 1}`,
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  })),
  // Add 4 more committees to reach 41 total
  ...Array.from({ length: 4 }, (_, i) => ({
    id: i + 38,
    name: `Joint Committee ${i + 1}`,
    chamber: "Joint",
    committee_code: `JTC${i + 1}`,
    is_active: true,
    is_subcommittee: false,
    created_at: "2025-01-04T12:00:00Z"
  }))
];

// Generate mock hearings data (47 hearings: all scheduled)
export const mockHearings = Array.from({ length: 47 }, (_, i) => ({
  id: i + 1,
  title: `Congressional Hearing ${i + 1}: Important Policy Discussion`,
  description: `This hearing addresses important policy matters affecting the American people. Topics include budget, healthcare, and national security.`,
  committee_id: Math.floor(Math.random() * 41) + 1,
  scheduled_date: new Date(Date.now() + (i * 24 * 60 * 60 * 1000)).toISOString(),
  location: `Hart Senate Office Building, Room ${100 + i}`,
  room: `${100 + i}`,
  status: "Scheduled",
  video_url: undefined,
  webcast_url: `https://senate.gov/hearings/hearing${i + 1}`,
  created_at: "2025-01-04T12:00:00Z"
}));