-- Strategic Committee Deployment
-- Key Congressional Committees for Production System
-- Generated: 2025-07-09T11:35:21.567416
-- Total Committees: 39

BEGIN;

-- Committee 1: Joint Economic Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Joint Economic Committee',
    'Joint',
    'jhje00',
    'jhje00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/joint/jhje00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 2: Joint Committee on Taxation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Joint Committee on Taxation',
    'Joint',
    'jhtx00',
    'jhtx00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/joint/jhtx00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 3: Joint Committee on the Library
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Joint Committee on the Library',
    'Joint',
    'jhla00',
    'jhla00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/joint/jhla00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 4: Joint Committee on Printing
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Joint Committee on Printing',
    'Joint',
    'jhpr00',
    'jhpr00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/joint/jhpr00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 5: Committee on Appropriations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Appropriations',
    'House',
    'hsap00',
    'hsap00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsap00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 6: Committee on Armed Services
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Armed Services',
    'House',
    'hsas00',
    'hsas00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsas00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 7: Committee on Education and the Workforce
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Education and the Workforce',
    'House',
    'hsed00',
    'hsed00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsed00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 8: Committee on Energy and Commerce
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Energy and Commerce',
    'House',
    'hsif00',
    'hsif00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsif00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 9: Committee on Financial Services
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Financial Services',
    'House',
    'hsba00',
    'hsba00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsba00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 10: Committee on Foreign Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Foreign Affairs',
    'House',
    'hsfa00',
    'hsfa00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsfa00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 11: Committee on Homeland Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Homeland Security',
    'House',
    'hshm00',
    'hshm00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hshm00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 12: Committee on the Judiciary
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on the Judiciary',
    'House',
    'hsju00',
    'hsju00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsju00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 13: Committee on Natural Resources
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Natural Resources',
    'House',
    'hsii00',
    'hsii00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsii00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 14: Committee on Oversight and Accountability
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Oversight and Accountability',
    'House',
    'hsgo00',
    'hsgo00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsgo00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 15: Committee on Science, Space, and Technology
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Science, Space, and Technology',
    'House',
    'hssy00',
    'hssy00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hssy00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 16: Committee on Small Business
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Small Business',
    'House',
    'hssm00',
    'hssm00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hssm00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 17: Committee on Transportation and Infrastructure
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Transportation and Infrastructure',
    'House',
    'hspw00',
    'hspw00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hspw00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 18: Committee on Veterans' Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Veterans' Affairs',
    'House',
    'hsvr00',
    'hsvr00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsvr00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 19: Committee on Ways and Means
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Ways and Means',
    'House',
    'hswm00',
    'hswm00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hswm00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 20: Committee on Appropriations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Appropriations',
    'Senate',
    'ssap00',
    'ssap00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssap00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 21: Committee on Armed Services
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Armed Services',
    'Senate',
    'ssas00',
    'ssas00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssas00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 22: Committee on Banking, Housing, and Urban Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Banking, Housing, and Urban Affairs',
    'Senate',
    'ssbk00',
    'ssbk00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssbk00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 23: Committee on Commerce, Science, and Transportation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Commerce, Science, and Transportation',
    'Senate',
    'sscm00',
    'sscm00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/sscm00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 24: Committee on Energy and Natural Resources
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Energy and Natural Resources',
    'Senate',
    'sseg00',
    'sseg00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/sseg00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 25: Committee on Environment and Public Works
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Environment and Public Works',
    'Senate',
    'ssev00',
    'ssev00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssev00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 26: Committee on Finance
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Finance',
    'Senate',
    'ssfi00',
    'ssfi00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssfi00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 27: Committee on Foreign Relations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Foreign Relations',
    'Senate',
    'ssfr00',
    'ssfr00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssfr00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 28: Committee on Health, Education, Labor and Pensions
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Health, Education, Labor and Pensions',
    'Senate',
    'sshr00',
    'sshr00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/sshr00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 29: Committee on Homeland Security and Governmental Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Homeland Security and Governmental Affairs',
    'Senate',
    'ssga00',
    'ssga00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssga00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 30: Committee on the Judiciary
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on the Judiciary',
    'Senate',
    'ssju00',
    'ssju00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssju00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 31: Committee on Rules and Administration
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Rules and Administration',
    'Senate',
    'ssra00',
    'ssra00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssra00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 32: Committee on Small Business and Entrepreneurship
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Small Business and Entrepreneurship',
    'Senate',
    'sssb00',
    'sssb00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/sssb00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 33: Committee on Veterans' Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Veterans' Affairs',
    'Senate',
    'ssvf00',
    'ssvf00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssvf00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 34: Subcommittee on Defense
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Defense',
    'House',
    'hsap02',
    'hsap02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 35: Subcommittee on Labor, Health and Human Services, Education
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Labor, Health and Human Services, Education',
    'House',
    'hsap03',
    'hsap03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 36: Subcommittee on State, Foreign Operations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on State, Foreign Operations',
    'House',
    'hsap04',
    'hsap04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 37: Subcommittee on Energy and Water Development
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy and Water Development',
    'Senate',
    'ssap01',
    'ssap01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 38: Subcommittee on Defense
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Defense',
    'Senate',
    'ssap02',
    'ssap02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Committee 39: Subcommittee on Labor, Health and Human Services, Education
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Labor, Health and Human Services, Education',
    'Senate',
    'ssap03',
    'ssap03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;

-- Deployment complete: 39 committees added