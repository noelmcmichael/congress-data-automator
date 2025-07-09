-- ====================================================================
-- FULL COMMITTEE EXPANSION DEPLOYMENT
-- ====================================================================
-- 
-- Generated: 2025-07-09T11:59:58.220763
-- Source: Strategic Pattern-Based Expansion
-- 
-- Deployment Summary:
--   • Existing Committees: 240
--   • New Committees: 135
--   • Total Projected: 375
--   • Target Coverage: 46.0%
-- 
-- Chamber Breakdown (New):
--   • House: 69
--   • Senate: 66
--   • Joint: 0
-- 
-- Type Breakdown (New):
--   • Standing: 7
--   • Subcommittee: 128
--   • Joint: 0
-- 
-- ====================================================================
-- DEPLOYMENT INSTRUCTIONS:
-- 
-- 1. Ensure Cloud SQL Proxy is running:
--    ./cloud-sql-proxy chefgavin:us-central1:congressional-db --port=5433
-- 
-- 2. Execute this script via proven deployment method:
--    python execute_committee_expansion_proxy_fixed.py
-- 
-- 3. Validate deployment:
--    python priority3_system_verification.py
-- 
-- ====================================================================


-- ====================================================================
-- MAIN COMMITTEES DEPLOYMENT (7 committees)
-- ====================================================================

BEGIN;


-- Committee: Committee on the Budget
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on the Budget',
    'House',
    'hsbu00',
    'hsbu00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsbu00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Committee on House Administration
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on House Administration',
    'House',
    'hsha00',
    'hsha00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsha00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Committee on Rules
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Rules',
    'House',
    'hsru00',
    'hsru00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsru00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Committee on Standards of Official Conduct
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Standards of Official Conduct',
    'House',
    'hsso00',
    'hsso00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/house/hsso00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Committee on the Budget
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on the Budget',
    'Senate',
    'ssbu00',
    'ssbu00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssbu00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Committee on Agriculture, Nutrition, and Forestry
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Agriculture, Nutrition, and Forestry',
    'Senate',
    'ssag00',
    'ssag00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssag00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Committee on Indian Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Committee on Indian Affairs',
    'Senate',
    'ssin00',
    'ssin00',
    'Standing',
    true,
    false,
    'https://www.congress.gov/committees/senate/ssin00',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;


-- ====================================================================
-- SUBCOMMITTEES DEPLOYMENT (128 committees in 3 batches)
-- ====================================================================

-- ====================================================================
-- Batch 1 of 3: Committee Deployment
-- Generated: 2025-07-09T11:59:58.220804
-- Committees in this batch: 50
-- ====================================================================

BEGIN;


-- Committee: Subcommittee on Agriculture, Rural Development, Food and Drug Administration, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Agriculture, Rural Development, Food and Drug Administration, and Related Agencies',
    'House',
    'hsap01',
    'hsap01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Financial Services and General Government
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Financial Services and General Government',
    'House',
    'hsap05',
    'hsap05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Homeland Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Homeland Security',
    'House',
    'hsap06',
    'hsap06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Interior, Environment, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Interior, Environment, and Related Agencies',
    'House',
    'hsap07',
    'hsap07',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap07',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Labor, Health and Human Services, Education, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Labor, Health and Human Services, Education, and Related Agencies',
    'House',
    'hsap08',
    'hsap08',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap08',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Legislative Branch
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Legislative Branch',
    'House',
    'hsap09',
    'hsap09',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap09',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Military Construction, Veterans Affairs, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Military Construction, Veterans Affairs, and Related Agencies',
    'House',
    'hsap10',
    'hsap10',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap10',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on State, Foreign Operations, and Related Programs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on State, Foreign Operations, and Related Programs',
    'House',
    'hsap11',
    'hsap11',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap11',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Transportation, Housing and Urban Development, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Transportation, Housing and Urban Development, and Related Agencies',
    'House',
    'hsap12',
    'hsap12',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsap12',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Energy and Water Development
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy and Water Development',
    'Senate',
    'ssap04',
    'ssap04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Financial Services and General Government
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Financial Services and General Government',
    'Senate',
    'ssap05',
    'ssap05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Homeland Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Homeland Security',
    'Senate',
    'ssap06',
    'ssap06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Interior, Environment, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Interior, Environment, and Related Agencies',
    'Senate',
    'ssap07',
    'ssap07',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap07',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Labor, Health and Human Services, Education, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Labor, Health and Human Services, Education, and Related Agencies',
    'Senate',
    'ssap08',
    'ssap08',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap08',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Legislative Branch
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Legislative Branch',
    'Senate',
    'ssap09',
    'ssap09',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap09',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Military Construction, Veterans Affairs, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Military Construction, Veterans Affairs, and Related Agencies',
    'Senate',
    'ssap10',
    'ssap10',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap10',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on State, Foreign Operations, and Related Programs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on State, Foreign Operations, and Related Programs',
    'Senate',
    'ssap11',
    'ssap11',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap11',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Transportation, Housing and Urban Development, and Related Agencies
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Transportation, Housing and Urban Development, and Related Agencies',
    'Senate',
    'ssap12',
    'ssap12',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssap12',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Health
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Health',
    'House',
    'hswm01',
    'hswm01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hswm01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Social Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Social Security',
    'House',
    'hswm02',
    'hswm02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hswm02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Trade
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Trade',
    'House',
    'hswm03',
    'hswm03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hswm03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Worker and Family Support
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Worker and Family Support',
    'House',
    'hswm04',
    'hswm04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hswm04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Select Revenue Measures
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Select Revenue Measures',
    'House',
    'hswm05',
    'hswm05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hswm05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Oversight
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Oversight',
    'House',
    'hswm06',
    'hswm06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hswm06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Courts, Intellectual Property, and the Internet
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Courts, Intellectual Property, and the Internet',
    'House',
    'hsju01',
    'hsju01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsju01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Crime, Terrorism, and Homeland Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Crime, Terrorism, and Homeland Security',
    'House',
    'hsju02',
    'hsju02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsju02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Immigration and Citizenship
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Immigration and Citizenship',
    'House',
    'hsju03',
    'hsju03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsju03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Antitrust, Commercial, and Administrative Law
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Antitrust, Commercial, and Administrative Law',
    'House',
    'hsju04',
    'hsju04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsju04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Constitution, Civil Rights, and Civil Liberties
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Constitution, Civil Rights, and Civil Liberties',
    'House',
    'hsju05',
    'hsju05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsju05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Federal Courts, Oversight, Agency Action, and Federal Rights
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Federal Courts, Oversight, Agency Action, and Federal Rights',
    'Senate',
    'ssju01',
    'ssju01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Competition Policy, Antitrust, and Consumer Rights
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Competition Policy, Antitrust, and Consumer Rights',
    'Senate',
    'ssju02',
    'ssju02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Criminal Justice and Counterterrorism
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Criminal Justice and Counterterrorism',
    'Senate',
    'ssju03',
    'ssju03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Human Rights and the Law
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Human Rights and the Law',
    'Senate',
    'ssju04',
    'ssju04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Immigration, Citizenship, and Border Safety
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Immigration, Citizenship, and Border Safety',
    'Senate',
    'ssju05',
    'ssju05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Intellectual Property
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Intellectual Property',
    'Senate',
    'ssju06',
    'ssju06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Privacy, Technology, and the Law
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Privacy, Technology, and the Law',
    'Senate',
    'ssju07',
    'ssju07',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssju07',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Energy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy',
    'House',
    'hsif01',
    'hsif01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsif01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Environment and Climate Change
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Environment and Climate Change',
    'House',
    'hsif02',
    'hsif02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsif02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Health
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Health',
    'House',
    'hsif03',
    'hsif03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsif03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Innovation, Data, and Commerce
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Innovation, Data, and Commerce',
    'House',
    'hsif04',
    'hsif04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsif04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Oversight and Investigations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Oversight and Investigations',
    'House',
    'hsif05',
    'hsif05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsif05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Communications and Technology
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Communications and Technology',
    'House',
    'hsif06',
    'hsif06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsif06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Cyber, Information Technologies, and Innovation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Cyber, Information Technologies, and Innovation',
    'House',
    'hsas01',
    'hsas01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Intelligence and Special Operations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Intelligence and Special Operations',
    'House',
    'hsas02',
    'hsas02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Military Personnel
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Military Personnel',
    'House',
    'hsas03',
    'hsas03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Readiness
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Readiness',
    'House',
    'hsas04',
    'hsas04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Seapower and Projection Forces
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Seapower and Projection Forces',
    'House',
    'hsas05',
    'hsas05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Strategic Forces
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Strategic Forces',
    'House',
    'hsas06',
    'hsas06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Tactical Air and Land Forces
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Tactical Air and Land Forces',
    'House',
    'hsas07',
    'hsas07',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsas07',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Airland
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Airland',
    'Senate',
    'ssas01',
    'ssas01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;

-- ====================================================================
-- End of Batch
-- ====================================================================

-- ====================================================================
-- Batch 2 of 3: Committee Deployment
-- Generated: 2025-07-09T11:59:58.220878
-- Committees in this batch: 50
-- ====================================================================

BEGIN;


-- Committee: Subcommittee on Cybersecurity
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Cybersecurity',
    'Senate',
    'ssas02',
    'ssas02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Emerging Threats and Capabilities
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Emerging Threats and Capabilities',
    'Senate',
    'ssas03',
    'ssas03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Personnel
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Personnel',
    'Senate',
    'ssas04',
    'ssas04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Readiness and Management Support
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Readiness and Management Support',
    'Senate',
    'ssas05',
    'ssas05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Seapower
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Seapower',
    'Senate',
    'ssas06',
    'ssas06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Strategic Forces
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Strategic Forces',
    'Senate',
    'ssas07',
    'ssas07',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssas07',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Capital Markets
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Capital Markets',
    'House',
    'hsba01',
    'hsba01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsba01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Digital Assets, Financial Technology and Inclusion
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Digital Assets, Financial Technology and Inclusion',
    'House',
    'hsba02',
    'hsba02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsba02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Financial Institutions and Monetary Policy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Financial Institutions and Monetary Policy',
    'House',
    'hsba03',
    'hsba03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsba03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Housing and Insurance
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Housing and Insurance',
    'House',
    'hsba04',
    'hsba04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsba04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on National Security, Illicit Finance, and International Financial Institutions
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on National Security, Illicit Finance, and International Financial Institutions',
    'House',
    'hsba05',
    'hsba05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsba05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Oversight and Investigations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Oversight and Investigations',
    'House',
    'hsba06',
    'hsba06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsba06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Aviation Safety, Operations, and Innovation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Aviation Safety, Operations, and Innovation',
    'Senate',
    'sscm01',
    'sscm01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sscm01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Communications, Media, and Broadband
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Communications, Media, and Broadband',
    'Senate',
    'sscm02',
    'sscm02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sscm02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Consumer Protection, Product Safety, and Data Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Consumer Protection, Product Safety, and Data Security',
    'Senate',
    'sscm03',
    'sscm03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sscm03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Oceans, Fisheries, Climate Change, and Manufacturing
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Oceans, Fisheries, Climate Change, and Manufacturing',
    'Senate',
    'sscm04',
    'sscm04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sscm04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Space, Science, and Competitiveness
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Space, Science, and Competitiveness',
    'Senate',
    'sscm05',
    'sscm05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sscm05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Surface Transportation, Maritime, Freight, and Ports
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Surface Transportation, Maritime, Freight, and Ports',
    'Senate',
    'sscm06',
    'sscm06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sscm06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Biotechnology, Horticulture, and Research
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Biotechnology, Horticulture, and Research',
    'House',
    'hsag01',
    'hsag01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsag01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Commodity Exchanges, Energy, and Credit
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Commodity Exchanges, Energy, and Credit',
    'House',
    'hsag02',
    'hsag02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsag02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Conservation and Forestry
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Conservation and Forestry',
    'House',
    'hsag03',
    'hsag03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsag03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on General Farm Commodities and Risk Management
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on General Farm Commodities and Risk Management',
    'House',
    'hsag04',
    'hsag04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsag04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Livestock and Foreign Agriculture
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Livestock and Foreign Agriculture',
    'House',
    'hsag05',
    'hsag05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsag05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Aviation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Aviation',
    'House',
    'hspw01',
    'hspw01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hspw01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Coast Guard and Maritime Transportation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Coast Guard and Maritime Transportation',
    'House',
    'hspw02',
    'hspw02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hspw02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Economic Development, Public Buildings, and Emergency Management
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Economic Development, Public Buildings, and Emergency Management',
    'House',
    'hspw03',
    'hspw03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hspw03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Highways and Transit
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Highways and Transit',
    'House',
    'hspw04',
    'hspw04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hspw04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Railroads, Pipelines, and Hazardous Materials
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Railroads, Pipelines, and Hazardous Materials',
    'House',
    'hspw05',
    'hspw05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hspw05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Water Resources and Environment
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Water Resources and Environment',
    'House',
    'hspw06',
    'hspw06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hspw06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Energy and Mineral Resources
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy and Mineral Resources',
    'House',
    'hsii01',
    'hsii01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsii01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Federal Lands
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Federal Lands',
    'House',
    'hsii02',
    'hsii02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsii02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Indigenous Peoples of the United States
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Indigenous Peoples of the United States',
    'House',
    'hsii03',
    'hsii03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsii03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Oversight and Investigations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Oversight and Investigations',
    'House',
    'hsii04',
    'hsii04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsii04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Water, Wildlife and Fisheries
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Water, Wildlife and Fisheries',
    'House',
    'hsii05',
    'hsii05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hsii05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Energy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy',
    'House',
    'hssy01',
    'hssy01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hssy01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Environment
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Environment',
    'House',
    'hssy02',
    'hssy02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hssy02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Investigations and Oversight
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Investigations and Oversight',
    'House',
    'hssy03',
    'hssy03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hssy03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Research and Technology
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Research and Technology',
    'House',
    'hssy04',
    'hssy04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hssy04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Space and Aeronautics
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Space and Aeronautics',
    'House',
    'hssy05',
    'hssy05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hssy05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Border Security and Enforcement
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Border Security and Enforcement',
    'House',
    'hshm01',
    'hshm01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hshm01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Counterterrorism, Law Enforcement, and Intelligence
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Counterterrorism, Law Enforcement, and Intelligence',
    'House',
    'hshm02',
    'hshm02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hshm02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Cybersecurity and Infrastructure Protection
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Cybersecurity and Infrastructure Protection',
    'House',
    'hshm03',
    'hshm03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hshm03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Emergency Management and Technology
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Emergency Management and Technology',
    'House',
    'hshm04',
    'hshm04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hshm04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Transportation and Maritime Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Transportation and Maritime Security',
    'House',
    'hshm05',
    'hshm05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/house/hshm05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Commodities, Risk Management, and Trade
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Commodities, Risk Management, and Trade',
    'Senate',
    'ssag01',
    'ssag01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssag01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Conservation, Climate, Forestry, and Natural Resources
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Conservation, Climate, Forestry, and Natural Resources',
    'Senate',
    'ssag02',
    'ssag02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssag02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Food and Nutrition, Specialty Crops, Organics, and Research
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Food and Nutrition, Specialty Crops, Organics, and Research',
    'Senate',
    'ssag03',
    'ssag03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssag03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Livestock, Dairy, Poultry, Local Food Systems, and Food Safety
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Livestock, Dairy, Poultry, Local Food Systems, and Food Safety',
    'Senate',
    'ssag04',
    'ssag04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssag04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Energy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy',
    'Senate',
    'sseg01',
    'sseg01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sseg01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on National Parks
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on National Parks',
    'Senate',
    'sseg02',
    'sseg02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sseg02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;

-- ====================================================================
-- End of Batch
-- ====================================================================

-- ====================================================================
-- Batch 3 of 3: Committee Deployment
-- Generated: 2025-07-09T11:59:58.220948
-- Committees in this batch: 28
-- ====================================================================

BEGIN;


-- Committee: Subcommittee on Public Lands, Forests, and Mining
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Public Lands, Forests, and Mining',
    'Senate',
    'sseg03',
    'sseg03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sseg03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Water and Power
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Water and Power',
    'Senate',
    'sseg04',
    'sseg04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sseg04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Economic Policy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Economic Policy',
    'Senate',
    'ssbk01',
    'ssbk01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssbk01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Financial Institutions and Consumer Protection
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Financial Institutions and Consumer Protection',
    'Senate',
    'ssbk02',
    'ssbk02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssbk02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Housing, Transportation, and Community Development
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Housing, Transportation, and Community Development',
    'Senate',
    'ssbk03',
    'ssbk03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssbk03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on National Security and International Trade and Finance
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on National Security and International Trade and Finance',
    'Senate',
    'ssbk04',
    'ssbk04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssbk04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Chemical Safety, Waste Management, Environmental Justice, and Regulatory Oversight
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Chemical Safety, Waste Management, Environmental Justice, and Regulatory Oversight',
    'Senate',
    'ssev01',
    'ssev01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssev01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Clean Air, Climate, and Nuclear Safety
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Clean Air, Climate, and Nuclear Safety',
    'Senate',
    'ssev02',
    'ssev02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssev02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Fisheries, Water, and Wildlife
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Fisheries, Water, and Wildlife',
    'Senate',
    'ssev03',
    'ssev03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssev03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Transportation and Infrastructure
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Transportation and Infrastructure',
    'Senate',
    'ssev04',
    'ssev04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssev04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Energy, Natural Resources, and Infrastructure
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Energy, Natural Resources, and Infrastructure',
    'Senate',
    'ssfi01',
    'ssfi01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfi01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Fiscal Responsibility and Economic Growth
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Fiscal Responsibility and Economic Growth',
    'Senate',
    'ssfi02',
    'ssfi02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfi02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Health Care
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Health Care',
    'Senate',
    'ssfi03',
    'ssfi03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfi03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on International Trade, Customs, and Global Competitiveness
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on International Trade, Customs, and Global Competitiveness',
    'Senate',
    'ssfi04',
    'ssfi04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfi04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Social Security, Pensions, and Family Policy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Social Security, Pensions, and Family Policy',
    'Senate',
    'ssfi05',
    'ssfi05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfi05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Taxation and IRS Oversight
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Taxation and IRS Oversight',
    'Senate',
    'ssfi06',
    'ssfi06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfi06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Africa and Global Health Policy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Africa and Global Health Policy',
    'Senate',
    'ssfr01',
    'ssfr01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfr01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on East Asia, the Pacific, and International Cybersecurity Policy
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on East Asia, the Pacific, and International Cybersecurity Policy',
    'Senate',
    'ssfr02',
    'ssfr02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfr02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Europe and Regional Security Cooperation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Europe and Regional Security Cooperation',
    'Senate',
    'ssfr03',
    'ssfr03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfr03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on International Development and Multilateral Institutions
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on International Development and Multilateral Institutions',
    'Senate',
    'ssfr04',
    'ssfr04',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfr04',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Near East, South Asia, Central Asia, and Counterterrorism
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Near East, South Asia, Central Asia, and Counterterrorism',
    'Senate',
    'ssfr05',
    'ssfr05',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfr05',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on State Department and USAID Management, International Operations, and Bilateral International Development
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on State Department and USAID Management, International Operations, and Bilateral International Development',
    'Senate',
    'ssfr06',
    'ssfr06',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssfr06',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Children and Families
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Children and Families',
    'Senate',
    'sshr01',
    'sshr01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sshr01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Employment and Workplace Safety
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Employment and Workplace Safety',
    'Senate',
    'sshr02',
    'sshr02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sshr02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Primary Health and Retirement Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Primary Health and Retirement Security',
    'Senate',
    'sshr03',
    'sshr03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/sshr03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Emerging Threats and Spending Oversight
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Emerging Threats and Spending Oversight',
    'Senate',
    'ssga01',
    'ssga01',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssga01',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Government Operations and Border Management
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Government Operations and Border Management',
    'Senate',
    'ssga02',
    'ssga02',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssga02',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;


-- Committee: Subcommittee on Investigations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Investigations',
    'Senate',
    'ssga03',
    'ssga03',
    'Subcommittee',
    true,
    true,
    'https://www.congress.gov/committees/senate/ssga03',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;

-- ====================================================================
-- End of Batch
-- ====================================================================


-- ====================================================================
-- DEPLOYMENT VALIDATION
-- ====================================================================

-- Check total committee count after deployment
SELECT 
    'Total Committees' as metric,
    COUNT(*) as count,
    '375' as expected
FROM committees;

-- Check chamber distribution
SELECT 
    chamber,
    COUNT(*) as count
FROM committees 
GROUP BY chamber 
ORDER BY chamber;

-- Check committee types
SELECT 
    committee_type,
    COUNT(*) as count
FROM committees 
GROUP BY committee_type 
ORDER BY committee_type;

-- Check for any committees with missing congress_gov_id
SELECT 
    'Missing congress_gov_id' as issue,
    COUNT(*) as count
FROM committees 
WHERE congress_gov_id IS NULL OR congress_gov_id = '';

-- ====================================================================
-- END OF DEPLOYMENT
-- ====================================================================
