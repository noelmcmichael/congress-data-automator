-- Simple Committee Test Deployment
-- Testing committee insertion approach

BEGIN;

-- Test Committee 1: Joint Economic Committee
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
    'https://www.jec.senate.gov/',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Test Committee 2: House Committee on Agriculture
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'House Committee on Agriculture',
    'House',
    'hsag00',
    'hsag00',
    'Standing',
    true,
    false,
    'https://agriculture.house.gov/',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Test Committee 3: Senate Committee on Agriculture
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Senate Committee on Agriculture, Nutrition, and Forestry',
    'Senate',
    'ssaf00',
    'ssaf00',
    'Standing',
    true,
    false,
    'https://www.agriculture.senate.gov/',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;
