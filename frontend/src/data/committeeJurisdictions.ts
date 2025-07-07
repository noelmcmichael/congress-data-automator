// Committee Jurisdiction Mapping Data
// Based on official House and Senate committee jurisdiction rules

export interface JurisdictionArea {
  id: string;
  name: string;
  description: string;
  agencies?: string[];
  departments?: string[];
  legislation_types?: string[];
}

export interface CommitteeJurisdiction {
  committee_name: string;
  chamber: string;
  jurisdiction_areas: JurisdictionArea[];
  primary_oversight: string[];
  key_agencies: string[];
  major_legislation: string[];
  overlap_committees?: string[];
}

export const jurisdictionAreas: JurisdictionArea[] = [
  {
    id: "agriculture",
    name: "Agriculture & Food",
    description: "Farm policy, food safety, rural development, and nutrition programs",
    agencies: ["USDA", "FDA (food safety)", "FSIS"],
    departments: ["Department of Agriculture"],
    legislation_types: ["Farm Bills", "Food Safety", "Rural Development"]
  },
  {
    id: "appropriations",
    name: "Federal Spending",
    description: "Government funding, budget allocations, and fiscal oversight",
    agencies: ["OMB", "GAO", "CBO"],
    departments: ["All Federal Departments"],
    legislation_types: ["Appropriations Bills", "Budget Resolutions", "Spending Bills"]
  },
  {
    id: "armed_services",
    name: "Defense & Military",
    description: "National defense, military operations, and defense contractors",
    agencies: ["DOD", "Joint Chiefs", "Defense Contractors"],
    departments: ["Department of Defense"],
    legislation_types: ["NDAA", "Military Authorization", "Defense Procurement"]
  },
  {
    id: "banking",
    name: "Financial Services",
    description: "Banking, securities, insurance, and financial regulation",
    agencies: ["Federal Reserve", "SEC", "FDIC", "OCC", "CFPB"],
    departments: ["Treasury Department"],
    legislation_types: ["Financial Reform", "Banking Regulation", "Securities Law"]
  },
  {
    id: "energy",
    name: "Energy & Environment",
    description: "Energy production, environmental protection, and climate policy",
    agencies: ["EPA", "DOE", "NRC", "FERC"],
    departments: ["Department of Energy", "Environmental Protection Agency"],
    legislation_types: ["Clean Energy", "Environmental Protection", "Nuclear Policy"]
  },
  {
    id: "foreign_affairs",
    name: "Foreign Relations",
    description: "International relations, diplomacy, and foreign aid",
    agencies: ["State Department", "USAID", "Peace Corps"],
    departments: ["Department of State"],
    legislation_types: ["Foreign Aid", "Diplomatic Relations", "International Treaties"]
  },
  {
    id: "healthcare",
    name: "Health & Human Services",
    description: "Healthcare policy, medical research, and public health",
    agencies: ["HHS", "CDC", "NIH", "FDA"],
    departments: ["Department of Health and Human Services"],
    legislation_types: ["Healthcare Reform", "Medical Research", "Public Health"]
  },
  {
    id: "homeland_security",
    name: "Homeland Security",
    description: "National security, border protection, and emergency management",
    agencies: ["DHS", "TSA", "CBP", "ICE", "FEMA"],
    departments: ["Department of Homeland Security"],
    legislation_types: ["Border Security", "Immigration", "Emergency Management"]
  },
  {
    id: "judiciary",
    name: "Justice & Courts",
    description: "Federal courts, civil rights, and law enforcement",
    agencies: ["DOJ", "FBI", "DEA", "ATF"],
    departments: ["Department of Justice"],
    legislation_types: ["Criminal Justice", "Civil Rights", "Court Administration"]
  },
  {
    id: "transportation",
    name: "Transportation & Infrastructure",
    description: "Transportation systems, infrastructure, and public works",
    agencies: ["DOT", "FAA", "FRA", "FHWA"],
    departments: ["Department of Transportation"],
    legislation_types: ["Infrastructure", "Transportation Policy", "Public Works"]
  },
  {
    id: "education",
    name: "Education & Labor",
    description: "Education policy, workforce development, and labor relations",
    agencies: ["Department of Education", "DOL", "NLRB"],
    departments: ["Department of Education", "Department of Labor"],
    legislation_types: ["Education Reform", "Labor Policy", "Workforce Development"]
  },
  {
    id: "veterans",
    name: "Veterans Affairs",
    description: "Veterans benefits, healthcare, and military family support",
    agencies: ["VA", "Veterans Benefits Administration"],
    departments: ["Department of Veterans Affairs"],
    legislation_types: ["Veterans Benefits", "Military Family Support", "VA Healthcare"]
  },
  {
    id: "small_business",
    name: "Small Business",
    description: "Small business development, entrepreneurship, and economic development",
    agencies: ["SBA", "SCORE", "Small Business Development Centers"],
    departments: ["Small Business Administration"],
    legislation_types: ["Small Business Support", "Entrepreneurship", "Economic Development"]
  },
  {
    id: "science_technology",
    name: "Science & Technology",
    description: "Scientific research, technology policy, and innovation",
    agencies: ["NSF", "NASA", "NIST", "OSTP"],
    departments: ["National Science Foundation"],
    legislation_types: ["Research Funding", "Technology Policy", "Innovation"]
  },
  {
    id: "intelligence",
    name: "Intelligence",
    description: "Intelligence community oversight and national security intelligence",
    agencies: ["CIA", "NSA", "DIA", "FBI Intelligence"],
    departments: ["Intelligence Community"],
    legislation_types: ["Intelligence Authorization", "Surveillance", "National Security"]
  }
];

export const committeeJurisdictions: CommitteeJurisdiction[] = [
  // House Committees
  {
    committee_name: "Committee on Agriculture",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "agriculture")!
    ],
    primary_oversight: ["USDA", "Food Safety", "Rural Development", "Farm Policy"],
    key_agencies: ["USDA", "FDA (food safety)", "FSIS"],
    major_legislation: ["Farm Bill", "Food Safety Modernization Act", "Rural Development Acts"],
    overlap_committees: ["Energy and Commerce (FDA)", "Natural Resources (forestry)"]
  },
  {
    committee_name: "Committee on Appropriations",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "appropriations")!
    ],
    primary_oversight: ["Federal Budget", "Government Spending", "Agency Funding"],
    key_agencies: ["OMB", "GAO", "CBO", "All Federal Agencies"],
    major_legislation: ["Annual Appropriations Bills", "Supplemental Spending", "Budget Resolutions"],
    overlap_committees: ["Budget Committee", "All other committees (funding oversight)"]
  },
  {
    committee_name: "Committee on Armed Services",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "armed_services")!
    ],
    primary_oversight: ["Department of Defense", "Military Operations", "Defense Contractors"],
    key_agencies: ["DOD", "Joint Chiefs of Staff", "Defense Contractors"],
    major_legislation: ["NDAA", "Military Construction", "Defense Authorization"],
    overlap_committees: ["Intelligence (military intelligence)", "Veterans' Affairs (military families)"]
  },
  {
    committee_name: "Committee on Financial Services",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "banking")!
    ],
    primary_oversight: ["Banking", "Securities", "Insurance", "Housing Finance"],
    key_agencies: ["Federal Reserve", "SEC", "FDIC", "OCC", "CFPB", "FHFA"],
    major_legislation: ["Dodd-Frank", "Banking Reform", "Housing Finance Reform"],
    overlap_committees: ["Ways and Means (tax policy)"]
  },
  {
    committee_name: "Committee on Energy and Commerce",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "energy")!,
      jurisdictionAreas.find(j => j.id === "healthcare")!
    ],
    primary_oversight: ["Energy", "Healthcare", "Commerce", "Communications"],
    key_agencies: ["EPA", "DOE", "HHS", "FDA", "FCC", "FTC"],
    major_legislation: ["Clean Air Act", "ACA", "Energy Policy", "Telecommunications"],
    overlap_committees: ["Natural Resources (energy)", "Ways and Means (healthcare)"]
  },
  {
    committee_name: "Committee on Foreign Affairs",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "foreign_affairs")!
    ],
    primary_oversight: ["Foreign Policy", "International Relations", "Foreign Aid"],
    key_agencies: ["State Department", "USAID", "Peace Corps", "Broadcasting Board of Governors"],
    major_legislation: ["Foreign Aid Authorization", "International Relations", "Diplomatic Relations"],
    overlap_committees: ["Armed Services (military aid)", "Intelligence (foreign intelligence)"]
  },
  {
    committee_name: "Committee on Homeland Security",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "homeland_security")!
    ],
    primary_oversight: ["DHS", "Border Security", "Immigration", "Emergency Management"],
    key_agencies: ["DHS", "TSA", "CBP", "ICE", "FEMA", "Secret Service"],
    major_legislation: ["Homeland Security Act", "Border Security", "Immigration Reform"],
    overlap_committees: ["Judiciary (immigration law)", "Transportation (TSA)"]
  },
  {
    committee_name: "Committee on the Judiciary",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "judiciary")!
    ],
    primary_oversight: ["Federal Courts", "Civil Rights", "Law Enforcement", "Immigration Law"],
    key_agencies: ["DOJ", "FBI", "DEA", "ATF", "Federal Courts"],
    major_legislation: ["Criminal Justice Reform", "Civil Rights", "Immigration", "Antitrust"],
    overlap_committees: ["Homeland Security (immigration)", "Oversight (DOJ oversight)"]
  },
  {
    committee_name: "Committee on Transportation and Infrastructure",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "transportation")!
    ],
    primary_oversight: ["Transportation", "Infrastructure", "Public Works", "Aviation"],
    key_agencies: ["DOT", "FAA", "FRA", "FHWA", "FTA", "MARAD"],
    major_legislation: ["Infrastructure Investment", "Transportation Authorization", "Aviation Policy"],
    overlap_committees: ["Energy and Commerce (pipeline safety)"]
  },
  {
    committee_name: "Committee on Education and the Workforce",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "education")!
    ],
    primary_oversight: ["Education", "Labor", "Workforce Development"],
    key_agencies: ["Department of Education", "DOL", "NLRB"],
    major_legislation: ["Education Reform", "Labor Policy", "Workforce Development"],
    overlap_committees: ["Ways and Means (education tax policy)"]
  },
  {
    committee_name: "Committee on Veterans' Affairs",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "veterans")!
    ],
    primary_oversight: ["Veterans Benefits", "VA Healthcare", "Military Family Support"],
    key_agencies: ["VA", "Veterans Benefits Administration", "Veterans Health Administration"],
    major_legislation: ["Veterans Benefits", "VA Healthcare", "Military Family Support"],
    overlap_committees: ["Armed Services (active duty)", "Energy and Commerce (VA healthcare)"]
  },
  {
    committee_name: "Committee on Small Business",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "small_business")!
    ],
    primary_oversight: ["Small Business", "Entrepreneurship", "Economic Development"],
    key_agencies: ["SBA", "SCORE", "Small Business Development Centers"],
    major_legislation: ["Small Business Support", "Entrepreneurship", "Economic Development"],
    overlap_committees: ["Financial Services (small business lending)"]
  },
  {
    committee_name: "Committee on Science, Space, and Technology",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "science_technology")!
    ],
    primary_oversight: ["Scientific Research", "Space", "Technology Policy"],
    key_agencies: ["NSF", "NASA", "NIST", "OSTP", "DOE (science)"],
    major_legislation: ["Research Authorization", "Space Policy", "Technology Innovation"],
    overlap_committees: ["Armed Services (military research)", "Energy and Commerce (technology)"]
  },
  {
    committee_name: "Committee on Ways and Means",
    chamber: "House",
    jurisdiction_areas: [
      // Tax policy spans multiple areas
    ],
    primary_oversight: ["Tax Policy", "Trade", "Social Security", "Medicare"],
    key_agencies: ["IRS", "Treasury", "USTR", "SSA", "CMS"],
    major_legislation: ["Tax Reform", "Trade Policy", "Social Security", "Medicare"],
    overlap_committees: ["Financial Services (tax policy)", "Energy and Commerce (Medicare)"]
  },

  // Senate Committees
  {
    committee_name: "Committee on Agriculture, Nutrition, and Forestry",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "agriculture")!
    ],
    primary_oversight: ["Agriculture", "Food and Nutrition", "Forestry", "Rural Development"],
    key_agencies: ["USDA", "FDA (food safety)", "FSIS", "Forest Service"],
    major_legislation: ["Farm Bill", "Food Safety", "Rural Development", "Forestry"],
    overlap_committees: ["Commerce (food safety)", "Environment (forestry)"]
  },
  {
    committee_name: "Committee on Appropriations",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "appropriations")!
    ],
    primary_oversight: ["Federal Budget", "Government Spending", "Agency Funding"],
    key_agencies: ["OMB", "GAO", "CBO", "All Federal Agencies"],
    major_legislation: ["Annual Appropriations Bills", "Supplemental Spending", "Budget Resolutions"],
    overlap_committees: ["Budget Committee", "All other committees (funding oversight)"]
  },
  {
    committee_name: "Committee on Armed Services",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "armed_services")!
    ],
    primary_oversight: ["Department of Defense", "Military Operations", "Defense Contractors"],
    key_agencies: ["DOD", "Joint Chiefs of Staff", "Defense Contractors"],
    major_legislation: ["NDAA", "Military Construction", "Defense Authorization"],
    overlap_committees: ["Intelligence (military intelligence)", "Veterans' Affairs (military families)"]
  },
  {
    committee_name: "Committee on Banking, Housing, and Urban Affairs",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "banking")!
    ],
    primary_oversight: ["Banking", "Securities", "Insurance", "Housing", "Urban Development"],
    key_agencies: ["Federal Reserve", "SEC", "FDIC", "OCC", "CFPB", "HUD"],
    major_legislation: ["Banking Reform", "Housing Policy", "Securities Regulation"],
    overlap_committees: ["Finance (tax policy)"]
  },
  {
    committee_name: "Committee on Commerce, Science, and Transportation",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "transportation")!,
      jurisdictionAreas.find(j => j.id === "science_technology")!
    ],
    primary_oversight: ["Commerce", "Transportation", "Science", "Technology", "Communications"],
    key_agencies: ["DOT", "FCC", "FTC", "NIST", "NOAA", "NASA"],
    major_legislation: ["Transportation Policy", "Telecommunications", "Science Authorization"],
    overlap_committees: ["Environment (transportation emissions)"]
  },
  {
    committee_name: "Committee on Energy and Natural Resources",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "energy")!
    ],
    primary_oversight: ["Energy", "Natural Resources", "Public Lands", "Water Resources"],
    key_agencies: ["DOE", "Interior", "Forest Service", "Bureau of Land Management"],
    major_legislation: ["Energy Policy", "Public Lands", "Water Resources"],
    overlap_committees: ["Environment (energy regulation)"]
  },
  {
    committee_name: "Committee on Environment and Public Works",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "energy")!
    ],
    primary_oversight: ["Environmental Protection", "Public Works", "Transportation Infrastructure"],
    key_agencies: ["EPA", "Army Corps of Engineers", "DOT (infrastructure)"],
    major_legislation: ["Clean Air Act", "Clean Water Act", "Infrastructure"],
    overlap_committees: ["Energy (environmental regulation)"]
  },
  {
    committee_name: "Committee on Finance",
    chamber: "Senate",
    jurisdiction_areas: [
      // Tax and fiscal policy
    ],
    primary_oversight: ["Tax Policy", "Trade", "Social Security", "Medicare", "Healthcare"],
    key_agencies: ["IRS", "Treasury", "USTR", "SSA", "CMS"],
    major_legislation: ["Tax Reform", "Trade Policy", "Social Security", "Medicare", "Healthcare"],
    overlap_committees: ["Banking (financial policy)", "HELP (healthcare)"]
  },
  {
    committee_name: "Committee on Foreign Relations",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "foreign_affairs")!
    ],
    primary_oversight: ["Foreign Policy", "International Relations", "Treaties", "Foreign Aid"],
    key_agencies: ["State Department", "USAID", "Peace Corps"],
    major_legislation: ["Foreign Aid Authorization", "Treaty Ratification", "International Relations"],
    overlap_committees: ["Armed Services (military aid)", "Intelligence (foreign intelligence)"]
  },
  {
    committee_name: "Committee on Health, Education, Labor and Pensions",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "healthcare")!,
      jurisdictionAreas.find(j => j.id === "education")!
    ],
    primary_oversight: ["Health", "Education", "Labor", "Pensions"],
    key_agencies: ["HHS", "Department of Education", "DOL", "NLRB"],
    major_legislation: ["Healthcare Reform", "Education Policy", "Labor Policy"],
    overlap_committees: ["Finance (healthcare)", "Judiciary (labor law)"]
  },
  {
    committee_name: "Committee on Homeland Security and Governmental Affairs",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "homeland_security")!
    ],
    primary_oversight: ["Homeland Security", "Government Operations", "Federal Workforce"],
    key_agencies: ["DHS", "OPM", "GSA", "GAO"],
    major_legislation: ["Homeland Security", "Government Reform", "Federal Workforce"],
    overlap_committees: ["Judiciary (immigration)", "Intelligence (homeland security)"]
  },
  {
    committee_name: "Committee on the Judiciary",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "judiciary")!
    ],
    primary_oversight: ["Federal Courts", "Civil Rights", "Law Enforcement", "Immigration"],
    key_agencies: ["DOJ", "FBI", "DEA", "ATF", "Federal Courts"],
    major_legislation: ["Criminal Justice", "Civil Rights", "Immigration", "Judicial Nominations"],
    overlap_committees: ["Homeland Security (immigration)", "Intelligence (law enforcement)"]
  },
  {
    committee_name: "Committee on Veterans' Affairs",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "veterans")!
    ],
    primary_oversight: ["Veterans Benefits", "VA Healthcare", "Military Family Support"],
    key_agencies: ["VA", "Veterans Benefits Administration", "Veterans Health Administration"],
    major_legislation: ["Veterans Benefits", "VA Healthcare", "Military Family Support"],
    overlap_committees: ["Armed Services (active duty)", "HELP (VA healthcare)"]
  },
  {
    committee_name: "Committee on Small Business and Entrepreneurship",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "small_business")!
    ],
    primary_oversight: ["Small Business", "Entrepreneurship", "Economic Development"],
    key_agencies: ["SBA", "SCORE", "Small Business Development Centers"],
    major_legislation: ["Small Business Support", "Entrepreneurship", "Economic Development"],
    overlap_committees: ["Banking (small business lending)"]
  },
  {
    committee_name: "Permanent Select Committee on Intelligence",
    chamber: "House",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "intelligence")!
    ],
    primary_oversight: ["Intelligence Community", "National Security Intelligence", "Surveillance"],
    key_agencies: ["CIA", "NSA", "DIA", "FBI Intelligence", "DNI"],
    major_legislation: ["Intelligence Authorization", "Surveillance", "National Security"],
    overlap_committees: ["Armed Services (military intelligence)", "Homeland Security (intelligence)"]
  },
  {
    committee_name: "Select Committee on Intelligence",
    chamber: "Senate",
    jurisdiction_areas: [
      jurisdictionAreas.find(j => j.id === "intelligence")!
    ],
    primary_oversight: ["Intelligence Community", "National Security Intelligence", "Surveillance"],
    key_agencies: ["CIA", "NSA", "DIA", "FBI Intelligence", "DNI"],
    major_legislation: ["Intelligence Authorization", "Surveillance", "National Security"],
    overlap_committees: ["Armed Services (military intelligence)", "Homeland Security (intelligence)"]
  }
];

export const getCommitteeJurisdiction = (committeeName: string, chamber: string): CommitteeJurisdiction | undefined => {
  return committeeJurisdictions.find(cj => 
    cj.committee_name === committeeName && cj.chamber === chamber
  );
};

export const getJurisdictionByArea = (areaId: string): JurisdictionArea | undefined => {
  return jurisdictionAreas.find(ja => ja.id === areaId);
};

export const getCommitteesByJurisdiction = (areaId: string): CommitteeJurisdiction[] => {
  return committeeJurisdictions.filter(cj => 
    cj.jurisdiction_areas.some(ja => ja.id === areaId)
  );
};

export const getAllJurisdictionAreas = (): JurisdictionArea[] => {
  return jurisdictionAreas;
};

export const getOverlapAnalysis = (): { area: string; committees: string[] }[] => {
  const overlapMap = new Map<string, Set<string>>();
  
  committeeJurisdictions.forEach(cj => {
    cj.jurisdiction_areas.forEach(ja => {
      if (!overlapMap.has(ja.id)) {
        overlapMap.set(ja.id, new Set());
      }
      overlapMap.get(ja.id)!.add(`${cj.committee_name} (${cj.chamber})`);
    });
  });
  
  return Array.from(overlapMap.entries())
    .filter(([_, committees]) => committees.size > 1)
    .map(([area, committees]) => ({
      area: jurisdictionAreas.find(ja => ja.id === area)?.name || area,
      committees: Array.from(committees)
    }));
};