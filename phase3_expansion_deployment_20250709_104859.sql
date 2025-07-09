-- Phase 3: Committee Structure Deployment
-- Generated: 2025-07-09T09:18:46.798873
-- Total Committees: 815

-- Phase 3: Committee Structure Expansion Deployment
-- Modified: 2025-07-09T10:48:59.384367
-- Purpose: Allow insertion of new committees (changed DO UPDATE to DO NOTHING)
-- Original: phase3_full_deployment_20250709_091846.sql
-- Total Committees: 815


BEGIN;

-- Clear existing committees (commented out for safety)
-- DELETE FROM committees WHERE created_at < NOW() - INTERVAL '1 day';

-- Committee 1: Indian Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Indian Affairs Committee',
    'Senate',
    'n79043125',
    'https://api.congress.gov/v3/committee/senate/n79043125?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n79043125?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 2: Joint Economic Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Economic Committee',
    'Joint',
    'jhje00',
    'https://api.congress.gov/v3/committee/joint/jhje00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jhje00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 3: Territories and Insular Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Territories and Insular Affairs Committee',
    'Senate',
    'n79043126',
    'https://api.congress.gov/v3/committee/senate/n79043126?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n79043126?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 4: Select Committee on the Modernization of Congress
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on the Modernization of Congress',
    'House',
    'hlmh00',
    'https://api.congress.gov/v3/committee/house/hlmh00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hlmh00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 5: Digital Assets Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Digital Assets Subcommittee',
    'Senate',
    'ssbk13',
    'https://api.congress.gov/v3/committee/senate/ssbk13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 6: Congressional-Executive Commission on China
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Congressional-Executive Commission on China',
    'Joint',
    'jcpk00',
    'https://api.congress.gov/v3/committee/joint/jcpk00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jcpk00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 7: Open Source Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Open Source Subcommittee',
    'House',
    'hlig11',
    'https://api.congress.gov/v3/committee/house/hlig11?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlig11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 8: South and Central Asia  Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'South and Central Asia  Subcommittee',
    'House',
    'hsfa19',
    'https://api.congress.gov/v3/committee/house/hsfa19?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 9: Federal Law Enforcement Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Federal Law Enforcement Subcommittee',
    'House',
    'hsgo33',
    'https://api.congress.gov/v3/committee/house/hsgo33?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo33?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 10: Delivering on Government Efficiency Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Delivering on Government Efficiency Subcommittee',
    'House',
    'hsgo16',
    'https://api.congress.gov/v3/committee/house/hsgo16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 11: Select Subcommittee on the Weaponization of the Federal Government
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Subcommittee on the Weaponization of the Federal Government',
    'House',
    'hlfd00',
    'https://api.congress.gov/v3/committee/house/hlfd00?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlfd00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 12: Select Subcommittee on the Coronavirus Pandemic
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Subcommittee on the Coronavirus Pandemic',
    'House',
    'hlvc00',
    'https://api.congress.gov/v3/committee/house/hlvc00?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlvc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 13: Task Force on the Attempted Assassination of Donald J. Trump Task Force
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Task Force on the Attempted Assassination of Donald J. Trump Task Force',
    'House',
    'htzt00',
    'https://api.congress.gov/v3/committee/house/htzt00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/htzt00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 14: Veterans'' Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Veterans'' Affairs Committee',
    'Senate',
    'ssva00',
    'https://api.congress.gov/v3/committee/senate/ssva00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssva00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 15: Small Business and Entrepreneurship Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Small Business and Entrepreneurship Committee',
    'Senate',
    'sssb00',
    'https://api.congress.gov/v3/committee/senate/sssb00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/sssb00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 16: Rules and Administration Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rules and Administration Committee',
    'Senate',
    'ssra00',
    'https://api.congress.gov/v3/committee/senate/ssra00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssra00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 17: Health, Education, Labor, and Pensions Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health, Education, Labor, and Pensions Committee',
    'Senate',
    'sshr00',
    'https://api.congress.gov/v3/committee/senate/sshr00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/sshr00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 18: Constitution Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Constitution Subcommittee',
    'Senate',
    'ssju21',
    'https://api.congress.gov/v3/committee/senate/ssju21?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 19: Children and Families Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Children and Families Subcommittee',
    'Senate',
    'sshr09',
    'https://api.congress.gov/v3/committee/senate/sshr09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 20: Judiciary Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Judiciary Committee',
    'Senate',
    'ssju00',
    'https://api.congress.gov/v3/committee/senate/ssju00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssju00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 21: Governmental Operations and Border Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Governmental Operations and Border Management Subcommittee',
    'Senate',
    'ssga22',
    'https://api.congress.gov/v3/committee/senate/ssga22?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 22: Criminal Justice and Counterterrorism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Criminal Justice and Counterterrorism Subcommittee',
    'Senate',
    'ssju22',
    'https://api.congress.gov/v3/committee/senate/ssju22?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 23: Federal Courts, Oversight, Agency Action, and Federal Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Federal Courts, Oversight, Agency Action, and Federal Rights Subcommittee',
    'Senate',
    'ssju25',
    'https://api.congress.gov/v3/committee/senate/ssju25?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju25?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 24: Human Rights and the Law Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Human Rights and the Law Subcommittee',
    'Senate',
    'ssju27',
    'https://api.congress.gov/v3/committee/senate/ssju27?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 25: Intellectual Property Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intellectual Property Subcommittee',
    'Senate',
    'ssju26',
    'https://api.congress.gov/v3/committee/senate/ssju26?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju26?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 26: Employment and Workplace Safety Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Employment and Workplace Safety Subcommittee',
    'Senate',
    'sshr11',
    'https://api.congress.gov/v3/committee/senate/sshr11?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 27: Immigration, Citizenship, and Border Safety Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Immigration, Citizenship, and Border Safety Subcommittee',
    'Senate',
    'ssju04',
    'https://api.congress.gov/v3/committee/senate/ssju04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 28: Primary Health and Retirement Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Primary Health and Retirement Security Subcommittee',
    'Senate',
    'sshr12',
    'https://api.congress.gov/v3/committee/senate/sshr12?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 29: Competition Policy, Antitrust, and Consumer Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Competition Policy, Antitrust, and Consumer Rights Subcommittee',
    'Senate',
    'ssju01',
    'https://api.congress.gov/v3/committee/senate/ssju01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 30: Privacy, Technology, and the Law Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Privacy, Technology, and the Law Subcommittee',
    'Senate',
    'ssju28',
    'https://api.congress.gov/v3/committee/senate/ssju28?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju28?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 31: Western Hemisphere, Transnational Crime, Civilian Security, Democracy, Human Rights, and Global Women''s Issues Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Western Hemisphere, Transnational Crime, Civilian Security, Democracy, Human Rights, and Global Women''s Issues Subcommittee',
    'Senate',
    'ssfr06',
    'https://api.congress.gov/v3/committee/senate/ssfr06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 32: Permanent Subcommittee on Investigations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Permanent Subcommittee on Investigations',
    'Senate',
    'ssga01',
    'https://api.congress.gov/v3/committee/senate/ssga01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 33: Health Care Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health Care Subcommittee',
    'Senate',
    'ssfi10',
    'https://api.congress.gov/v3/committee/senate/ssfi10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 34: Near East, South Asia, Central Asia, and Counterterrorism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Near East, South Asia, Central Asia, and Counterterrorism Subcommittee',
    'Senate',
    'ssfr07',
    'https://api.congress.gov/v3/committee/senate/ssfr07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 35: Energy, Natural Resources, and Infrastructure Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy, Natural Resources, and Infrastructure Subcommittee',
    'Senate',
    'ssfi12',
    'https://api.congress.gov/v3/committee/senate/ssfi12?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 36: Europe and Regional Security Cooperation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Europe and Regional Security Cooperation Subcommittee',
    'Senate',
    'ssfr01',
    'https://api.congress.gov/v3/committee/senate/ssfr01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 37: Multilateral International Development, Multilateral Institutions, and International Economic, Energy, and Environmental Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Multilateral International Development, Multilateral Institutions, and International Economic, Energy, and Environmental Policy Subcommittee',
    'Senate',
    'ssfr15',
    'https://api.congress.gov/v3/committee/senate/ssfr15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 38: Foreign Relations Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Foreign Relations Committee',
    'Senate',
    'ssfr00',
    'https://api.congress.gov/v3/committee/senate/ssfr00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssfr00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 39: Finance Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Finance Committee',
    'Senate',
    'ssfi00',
    'https://api.congress.gov/v3/committee/senate/ssfi00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssfi00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 40: Homeland Security and Governmental Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Homeland Security and Governmental Affairs Committee',
    'Senate',
    'ssga00',
    'https://api.congress.gov/v3/committee/senate/ssga00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssga00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 41: State Department and USAID Management, International Operations, and Bilateral International Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'State Department and USAID Management, International Operations, and Bilateral International Development Subcommittee',
    'Senate',
    'ssfr14',
    'https://api.congress.gov/v3/committee/senate/ssfr14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 42: Fiscal Responsibility and Economic Growth Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fiscal Responsibility and Economic Growth Subcommittee',
    'Senate',
    'ssfi14',
    'https://api.congress.gov/v3/committee/senate/ssfi14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 43: Emerging Threats and Spending Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Emerging Threats and Spending Oversight Subcommittee',
    'Senate',
    'ssga20',
    'https://api.congress.gov/v3/committee/senate/ssga20?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 44: Africa and Global Health Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Africa and Global Health Policy Subcommittee',
    'Senate',
    'ssfr09',
    'https://api.congress.gov/v3/committee/senate/ssfr09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 45: International Trade, Customs, and Global Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Trade, Customs, and Global Competitiveness Subcommittee',
    'Senate',
    'ssfi13',
    'https://api.congress.gov/v3/committee/senate/ssfi13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 46: East Asia, the Pacific, and International Cybersecurity Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'East Asia, the Pacific, and International Cybersecurity Policy Subcommittee',
    'Senate',
    'ssfr02',
    'https://api.congress.gov/v3/committee/senate/ssfr02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 47: Taxation and IRS Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Taxation and IRS Oversight Subcommittee',
    'Senate',
    'ssfi11',
    'https://api.congress.gov/v3/committee/senate/ssfi11?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 48: Social Security, Pensions, and Family Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Social Security, Pensions, and Family Policy Subcommittee',
    'Senate',
    'ssfi02',
    'https://api.congress.gov/v3/committee/senate/ssfi02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 49: Superfund, Waste Management, and Regulatory Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Superfund, Waste Management, and Regulatory Oversight Subcommittee',
    'Senate',
    'ssev09',
    'https://api.congress.gov/v3/committee/senate/ssev09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 50: Tourism, Trade, and Export
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tourism, Trade, and Export',
    'Senate',
    'sscm39',
    'https://api.congress.gov/v3/committee/senate/sscm39?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm39?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 51: Energy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Subcommittee',
    'Senate',
    'sseg01',
    'https://api.congress.gov/v3/committee/senate/sseg01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 52: Consumer Protection, Product Safety, and Data Security
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer Protection, Product Safety, and Data Security',
    'Senate',
    'sscm35',
    'https://api.congress.gov/v3/committee/senate/sscm35?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm35?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 53: Water and Power Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Water and Power Subcommittee',
    'Senate',
    'sseg07',
    'https://api.congress.gov/v3/committee/senate/sseg07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 54: Transportation and Infrastructure Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation and Infrastructure Subcommittee',
    'Senate',
    'ssev08',
    'https://api.congress.gov/v3/committee/senate/ssev08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 55: Surface Transportation, Maritime, Freight, and Ports
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Surface Transportation, Maritime, Freight, and Ports',
    'Senate',
    'sscm38',
    'https://api.congress.gov/v3/committee/senate/sscm38?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm38?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 56: Environment and Public Works Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment and Public Works Committee',
    'Senate',
    'ssev00',
    'https://api.congress.gov/v3/committee/senate/ssev00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssev00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 57: Clean Air and Nuclear Safety Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Clean Air and Nuclear Safety Subcommittee',
    'Senate',
    'ssev10',
    'https://api.congress.gov/v3/committee/senate/ssev10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 58: Space and Science
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Space and Science',
    'Senate',
    'sscm37',
    'https://api.congress.gov/v3/committee/senate/sscm37?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm37?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 59: Oceans, Fisheries, Climate Change, and Manufacturing
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oceans, Fisheries, Climate Change, and Manufacturing',
    'Senate',
    'sscm36',
    'https://api.congress.gov/v3/committee/senate/sscm36?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm36?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 60: National Parks Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Parks Subcommittee',
    'Senate',
    'sseg04',
    'https://api.congress.gov/v3/committee/senate/sseg04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 61: Public Lands, Forests, and Mining Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Lands, Forests, and Mining Subcommittee',
    'Senate',
    'sseg03',
    'https://api.congress.gov/v3/committee/senate/sseg03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 62: Energy and Natural Resources Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Natural Resources Committee',
    'Senate',
    'sseg00',
    'https://api.congress.gov/v3/committee/senate/sseg00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/sseg00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 63: Fisheries, Water, and Wildlife Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fisheries, Water, and Wildlife Subcommittee',
    'Senate',
    'ssev15',
    'https://api.congress.gov/v3/committee/senate/ssev15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 64: Financial Institutions and Consumer Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Institutions and Consumer Protection Subcommittee',
    'Senate',
    'ssbk08',
    'https://api.congress.gov/v3/committee/senate/ssbk08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 65: Commerce, Science, and Transportation Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Science, and Transportation Committee',
    'Senate',
    'sscm00',
    'https://api.congress.gov/v3/committee/senate/sscm00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/sscm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 66: Communication, Media, and Broadband
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Communication, Media, and Broadband',
    'Senate',
    'sscm34',
    'https://api.congress.gov/v3/committee/senate/sscm34?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm34?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 67: Budget Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Budget Committee',
    'Senate',
    'ssbu00',
    'https://api.congress.gov/v3/committee/senate/ssbu00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssbu00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 68: Housing, Transportation, and Community Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Housing, Transportation, and Community Development Subcommittee',
    'Senate',
    'ssbk09',
    'https://api.congress.gov/v3/committee/senate/ssbk09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 69: Economic Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Policy Subcommittee',
    'Senate',
    'ssbk12',
    'https://api.congress.gov/v3/committee/senate/ssbk12?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 70: Aviation Safety, Operations, and Innovation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aviation Safety, Operations, and Innovation',
    'Senate',
    'sscm33',
    'https://api.congress.gov/v3/committee/senate/sscm33?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm33?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 71: Banking, Housing, and Urban Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Banking, Housing, and Urban Affairs Committee',
    'Senate',
    'ssbk00',
    'https://api.congress.gov/v3/committee/senate/ssbk00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssbk00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 72: National Security and International Trade and Finance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Security and International Trade and Finance Subcommittee',
    'Senate',
    'ssbk05',
    'https://api.congress.gov/v3/committee/senate/ssbk05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 73: Securities, Insurance, and Investment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Securities, Insurance, and Investment Subcommittee',
    'Senate',
    'ssbk04',
    'https://api.congress.gov/v3/committee/senate/ssbk04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 74: Agriculture, Rural Development, Food and Drug Administration, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Agriculture, Rural Development, Food and Drug Administration, and Related Agencies Subcommittee',
    'Senate',
    'ssap01',
    'https://api.congress.gov/v3/committee/senate/ssap01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 75: Appropriations Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Appropriations Committee',
    'Senate',
    'ssap00',
    'https://api.congress.gov/v3/committee/senate/ssap00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssap00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 76: Military Construction and Veterans Affairs, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Construction and Veterans Affairs, and Related Agencies Subcommittee',
    'Senate',
    'ssap19',
    'https://api.congress.gov/v3/committee/senate/ssap19?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 77: Airland Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Airland Subcommittee',
    'Senate',
    'ssas14',
    'https://api.congress.gov/v3/committee/senate/ssas14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 78: Financial Services and General Government Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Services and General Government Subcommittee',
    'Senate',
    'ssap23',
    'https://api.congress.gov/v3/committee/senate/ssap23?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 79: State, Foreign Operations, and Related Programs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'State, Foreign Operations, and Related Programs Subcommittee',
    'Senate',
    'ssap20',
    'https://api.congress.gov/v3/committee/senate/ssap20?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 80: SeaPower Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'SeaPower Subcommittee',
    'Senate',
    'ssas13',
    'https://api.congress.gov/v3/committee/senate/ssas13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 81: Commerce, Justice, Science, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Justice, Science, and Related Agencies Subcommittee',
    'Senate',
    'ssap16',
    'https://api.congress.gov/v3/committee/senate/ssap16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 82: Cybersecurity Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cybersecurity Subcommittee',
    'Senate',
    'ssas21',
    'https://api.congress.gov/v3/committee/senate/ssas21?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 83: Department of the Interior, Environment, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department of the Interior, Environment, and Related Agencies Subcommittee',
    'Senate',
    'ssap17',
    'https://api.congress.gov/v3/committee/senate/ssap17?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 84: Legislative Branch Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Legislative Branch Subcommittee',
    'Senate',
    'ssap08',
    'https://api.congress.gov/v3/committee/senate/ssap08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 85: Departments of Labor, Health and Human Services, and Education, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Departments of Labor, Health and Human Services, and Education, and Related Agencies Subcommittee',
    'Senate',
    'ssap18',
    'https://api.congress.gov/v3/committee/senate/ssap18?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 86: Transportation, Housing and Urban Development, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation, Housing and Urban Development, and Related Agencies Subcommittee',
    'Senate',
    'ssap24',
    'https://api.congress.gov/v3/committee/senate/ssap24?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 87: Emerging Threats and Capabilities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Emerging Threats and Capabilities Subcommittee',
    'Senate',
    'ssas20',
    'https://api.congress.gov/v3/committee/senate/ssas20?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 88: Armed Services Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Armed Services Committee',
    'Senate',
    'ssas00',
    'https://api.congress.gov/v3/committee/senate/ssas00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssas00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 89: Department of Homeland Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department of Homeland Security Subcommittee',
    'Senate',
    'ssap14',
    'https://api.congress.gov/v3/committee/senate/ssap14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 90: Readiness and Management Support Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Readiness and Management Support Subcommittee',
    'Senate',
    'ssas15',
    'https://api.congress.gov/v3/committee/senate/ssas15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 91: Strategic Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Strategic Forces Subcommittee',
    'Senate',
    'ssas16',
    'https://api.congress.gov/v3/committee/senate/ssas16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 92: Energy and Water Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Water Development Subcommittee',
    'Senate',
    'ssap22',
    'https://api.congress.gov/v3/committee/senate/ssap22?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 93: Department of Defense Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department of Defense Subcommittee',
    'Senate',
    'ssap02',
    'https://api.congress.gov/v3/committee/senate/ssap02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 94: Personnel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Personnel Subcommittee',
    'Senate',
    'ssas17',
    'https://api.congress.gov/v3/committee/senate/ssas17?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 95: Food and Nutrition, Specialty Crops, Organics, and Research Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Food and Nutrition, Specialty Crops, Organics, and Research Subcommittee',
    'Senate',
    'ssaf16',
    'https://api.congress.gov/v3/committee/senate/ssaf16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 96: Agriculture, Nutrition, and Forestry Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Agriculture, Nutrition, and Forestry Committee',
    'Senate',
    'ssaf00',
    'https://api.congress.gov/v3/committee/senate/ssaf00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/ssaf00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 97: Conservation, Climate, Forestry, and Natural Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Conservation, Climate, Forestry, and Natural Resources Subcommittee',
    'Senate',
    'ssaf14',
    'https://api.congress.gov/v3/committee/senate/ssaf14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 98: Aging (Special) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aging (Special) Committee',
    'Senate',
    'spag00',
    'https://api.congress.gov/v3/committee/senate/spag00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/spag00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 99: Intelligence (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intelligence (Select) Committee',
    'Senate',
    'slin00',
    'https://api.congress.gov/v3/committee/senate/slin00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/slin00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 100: Commodities, Risk Management, and Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commodities, Risk Management, and Trade Subcommittee',
    'Senate',
    'ssaf13',
    'https://api.congress.gov/v3/committee/senate/ssaf13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 100/815 committees processed

-- Committee 101: Livestock, Dairy, Poultry, Local Food Systems, and Food Safety and Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Livestock, Dairy, Poultry, Local Food Systems, and Food Safety and Security Subcommittee',
    'Senate',
    'ssaf17',
    'https://api.congress.gov/v3/committee/senate/ssaf17?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 102: Rural Development and Energy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rural Development and Energy Subcommittee',
    'Senate',
    'ssaf15',
    'https://api.congress.gov/v3/committee/senate/ssaf15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 103: Ethics (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ethics (Select) Committee',
    'Senate',
    'slet00',
    'https://api.congress.gov/v3/committee/senate/slet00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/slet00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 104: Joint Committee on Taxation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Committee on Taxation',
    'Joint',
    'jstx00',
    'https://api.congress.gov/v3/committee/joint/jstx00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jstx00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 105: Indian Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Indian Affairs Committee',
    'Senate',
    'slia00',
    'https://api.congress.gov/v3/committee/senate/slia00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/slia00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 106: United States Senate Caucus on International Narcotics Control
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'United States Senate Caucus on International Narcotics Control',
    'Senate',
    'scnc00',
    'https://api.congress.gov/v3/committee/senate/scnc00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/scnc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 107: Joint Committee on Printing
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Committee on Printing',
    'Joint',
    'jspr00',
    'https://api.congress.gov/v3/committee/joint/jspr00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jspr00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 108: Joint Committee on the Library
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Committee on the Library',
    'Joint',
    'jslc00',
    'https://api.congress.gov/v3/committee/joint/jslc00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jslc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 109: Commission on Security and Cooperation in Europe (U.S. Helsinki Commission)
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commission on Security and Cooperation in Europe (U.S. Helsinki Commission)',
    'Joint',
    'jcse00',
    'https://api.congress.gov/v3/committee/joint/jcse00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jcse00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 110: Joint Economic Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Economic Committee',
    'Joint',
    'jsec00',
    'https://api.congress.gov/v3/committee/joint/jsec00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jsec00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 111: Aviation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aviation Subcommittee',
    'House',
    'hspw05',
    'https://api.congress.gov/v3/committee/house/hspw05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspw05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 112: Work and Welfare Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Work and Welfare Subcommittee',
    'House',
    'hswm03',
    'https://api.congress.gov/v3/committee/house/hswm03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hswm03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 113: Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Trade Subcommittee',
    'House',
    'hswm04',
    'https://api.congress.gov/v3/committee/house/hswm04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hswm04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 114: Tax Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tax Subcommittee',
    'House',
    'hswm05',
    'https://api.congress.gov/v3/committee/house/hswm05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hswm05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 115: Social Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Social Security Subcommittee',
    'House',
    'hswm01',
    'https://api.congress.gov/v3/committee/house/hswm01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hswm01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 116: Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight Subcommittee',
    'House',
    'hswm06',
    'https://api.congress.gov/v3/committee/house/hswm06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hswm06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 117: Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health Subcommittee',
    'House',
    'hswm02',
    'https://api.congress.gov/v3/committee/house/hswm02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hswm02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 118: Technology Modernization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology Modernization Subcommittee',
    'House',
    'hsvr11',
    'https://api.congress.gov/v3/committee/house/hsvr11?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 119: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsvr08',
    'https://api.congress.gov/v3/committee/house/hsvr08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 120: Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health Subcommittee',
    'House',
    'hsvr03',
    'https://api.congress.gov/v3/committee/house/hsvr03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 121: Economic Opportunity Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Opportunity Subcommittee',
    'House',
    'hsvr10',
    'https://api.congress.gov/v3/committee/house/hsvr10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 122: Disability Assistance and Memorial Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Disability Assistance and Memorial Affairs Subcommittee',
    'House',
    'hsvr09',
    'https://api.congress.gov/v3/committee/house/hsvr09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 123: Water Resources and Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Water Resources and Environment Subcommittee',
    'House',
    'hspw02',
    'https://api.congress.gov/v3/committee/house/hspw02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspw02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 124: Railroads, Pipelines, and Hazardous Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Railroads, Pipelines, and Hazardous Materials Subcommittee',
    'House',
    'hspw14',
    'https://api.congress.gov/v3/committee/house/hspw14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspw14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 125: Highways and Transit Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Highways and Transit Subcommittee',
    'House',
    'hspw12',
    'https://api.congress.gov/v3/committee/house/hspw12?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspw12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 126: Economic Development, Public Buildings, and Emergency Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Development, Public Buildings, and Emergency Management Subcommittee',
    'House',
    'hspw13',
    'https://api.congress.gov/v3/committee/house/hspw13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspw13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 127: Coast Guard and Maritime Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Coast Guard and Maritime Transportation Subcommittee',
    'House',
    'hspw07',
    'https://api.congress.gov/v3/committee/house/hspw07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspw07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 128: Rural Development, Energy, and Supply Chains Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rural Development, Energy, and Supply Chains Subcommittee',
    'House',
    'hssm21',
    'https://api.congress.gov/v3/committee/house/hssm21?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssm21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 129: Oversight, Investigations, and Regulations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight, Investigations, and Regulations',
    'House',
    'hssm24',
    'https://api.congress.gov/v3/committee/house/hssm24?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssm24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 130: Innovation, Entrepreneurship, and Workforce Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Innovation, Entrepreneurship, and Workforce Development Subcommittee',
    'House',
    'hssm22',
    'https://api.congress.gov/v3/committee/house/hssm22?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssm22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 131: Economic Growth, Tax, and Capital Access Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Growth, Tax, and Capital Access Subcommittee',
    'House',
    'hssm27',
    'https://api.congress.gov/v3/committee/house/hssm27?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssm27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 132: Contracting and Infrastructure Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Contracting and Infrastructure Subcommittee',
    'House',
    'hssm23',
    'https://api.congress.gov/v3/committee/house/hssm23?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssm23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 133: Space and Aeronautics Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Space and Aeronautics Subcommittee',
    'House',
    'hssy16',
    'https://api.congress.gov/v3/committee/house/hssy16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssy16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 134: Research and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Research and Technology Subcommittee',
    'House',
    'hssy15',
    'https://api.congress.gov/v3/committee/house/hssy15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssy15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 135: Investigations and Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigations and Oversight Subcommittee',
    'House',
    'hssy21',
    'https://api.congress.gov/v3/committee/house/hssy21?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssy21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 136: Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment Subcommittee',
    'House',
    'hssy18',
    'https://api.congress.gov/v3/committee/house/hssy18?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssy18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 137: Energy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Subcommittee',
    'House',
    'hssy20',
    'https://api.congress.gov/v3/committee/house/hssy20?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hssy20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 138: Rules and Organization of the House Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rules and Organization of the House Subcommittee',
    'House',
    'hsru04',
    'https://api.congress.gov/v3/committee/house/hsru04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsru04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 139: Legislative and Budget Process Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Legislative and Budget Process Subcommittee',
    'House',
    'hsru02',
    'https://api.congress.gov/v3/committee/house/hsru02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsru02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 140: Military and Foreign Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military and Foreign Affairs Subcommittee',
    'House',
    'hsgo06',
    'https://api.congress.gov/v3/committee/house/hsgo06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 141: Health Care and Financial Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health Care and Financial Services Subcommittee',
    'House',
    'hsgo27',
    'https://api.congress.gov/v3/committee/house/hsgo27?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 142: Government Operations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Government Operations Subcommittee',
    'House',
    'hsgo24',
    'https://api.congress.gov/v3/committee/house/hsgo24?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 143: Economic Growth, Energy Policy, and Regulatory Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Growth, Energy Policy, and Regulatory Affairs Subcommittee',
    'House',
    'hsgo05',
    'https://api.congress.gov/v3/committee/house/hsgo05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 144: Cybersecurity, Information Technology, and Government Innovation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cybersecurity, Information Technology, and Government Innovation Subcommittee',
    'House',
    'hsgo12',
    'https://api.congress.gov/v3/committee/house/hsgo12?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 145: Water, Wildlife and Fisheries Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Water, Wildlife and Fisheries Subcommittee',
    'House',
    'hsii13',
    'https://api.congress.gov/v3/committee/house/hsii13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsii13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 146: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsii15',
    'https://api.congress.gov/v3/committee/house/hsii15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsii15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 147: Indian and Insular Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Indian and Insular Affairs Subcommittee',
    'House',
    'hsii24',
    'https://api.congress.gov/v3/committee/house/hsii24?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsii24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 148: Federal Lands Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Federal Lands Subcommittee',
    'House',
    'hsii10',
    'https://api.congress.gov/v3/committee/house/hsii10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsii10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 149: Energy and Mineral Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Mineral Resources Subcommittee',
    'House',
    'hsii06',
    'https://api.congress.gov/v3/committee/house/hsii06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsii06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 150: Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight Subcommittee',
    'House',
    'hsju13',
    'https://api.congress.gov/v3/committee/house/hsju13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 151: Immigration Integrity, Security, and Enforcement Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Immigration Integrity, Security, and Enforcement Subcommittee',
    'House',
    'hsju01',
    'https://api.congress.gov/v3/committee/house/hsju01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 152: Crime and Federal Government Surveillance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Crime and Federal Government Surveillance Subcommittee',
    'House',
    'hsju08',
    'https://api.congress.gov/v3/committee/house/hsju08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 153: Courts, Intellectual Property, Artificial Intelligence, and the Internet Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Courts, Intellectual Property, Artificial Intelligence, and the Internet Subcommittee',
    'House',
    'hsju03',
    'https://api.congress.gov/v3/committee/house/hsju03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 154: Constitution and Limited Government Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Constitution and Limited Government Subcommittee',
    'House',
    'hsju10',
    'https://api.congress.gov/v3/committee/house/hsju10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 155: Administrative State, Regulatory Reform, and Antitrust Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Administrative State, Regulatory Reform, and Antitrust Subcommittee',
    'House',
    'hsju05',
    'https://api.congress.gov/v3/committee/house/hsju05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 156: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hlig09',
    'https://api.congress.gov/v3/committee/house/hlig09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlig09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 157: National Security Agency and Cyber Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Security Agency and Cyber Subcommittee',
    'House',
    'hlig02',
    'https://api.congress.gov/v3/committee/house/hlig02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlig02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 158: National Intelligence Enterprise Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Intelligence Enterprise Subcommittee',
    'House',
    'hlig06',
    'https://api.congress.gov/v3/committee/house/hlig06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlig06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 159: Subcommittee on Defense Intelligence and Overhead Architecture
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Subcommittee on Defense Intelligence and Overhead Architecture',
    'House',
    'hlig04',
    'https://api.congress.gov/v3/committee/house/hlig04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlig04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 160: Central Intelligence Agency Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Central Intelligence Agency Subcommittee',
    'House',
    'hlig01',
    'https://api.congress.gov/v3/committee/house/hlig01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlig01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 161: Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight Subcommittee',
    'House',
    'hsha06',
    'https://api.congress.gov/v3/committee/house/hsha06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsha06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 162: Modernization and Innovation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Modernization and Innovation Subcommittee',
    'House',
    'hsha27',
    'https://api.congress.gov/v3/committee/house/hsha27?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsha27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 163: Elections Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Elections Subcommittee',
    'House',
    'hsha08',
    'https://api.congress.gov/v3/committee/house/hsha08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsha08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 164: Transportation and Maritime Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation and Maritime Security Subcommittee',
    'House',
    'hshm07',
    'https://api.congress.gov/v3/committee/house/hshm07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hshm07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 165: Oversight, Investigations, and Accountability Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight, Investigations, and Accountability Subcommittee',
    'House',
    'hshm09',
    'https://api.congress.gov/v3/committee/house/hshm09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hshm09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 166: Emergency Management and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Emergency Management and Technology Subcommittee',
    'House',
    'hshm12',
    'https://api.congress.gov/v3/committee/house/hshm12?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hshm12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 167: Cybersecurity and Infrastructure Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cybersecurity and Infrastructure Protection Subcommittee',
    'House',
    'hshm08',
    'https://api.congress.gov/v3/committee/house/hshm08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hshm08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 168: Counterterrorism and Intelligence Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Counterterrorism and Intelligence Subcommittee',
    'House',
    'hshm05',
    'https://api.congress.gov/v3/committee/house/hshm05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hshm05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 169: Border Security and Enforcement Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Border Security and Enforcement Subcommittee',
    'House',
    'hshm11',
    'https://api.congress.gov/v3/committee/house/hshm11?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hshm11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 170: Western Hemisphere Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Western Hemisphere Subcommittee',
    'House',
    'hsfa07',
    'https://api.congress.gov/v3/committee/house/hsfa07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 171: Oversight and Intelligence Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Intelligence Subcommittee',
    'House',
    'hsfa17',
    'https://api.congress.gov/v3/committee/house/hsfa17?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 172: Middle East and North Africa Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Middle East and North Africa Subcommittee',
    'House',
    'hsfa13',
    'https://api.congress.gov/v3/committee/house/hsfa13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 173: East Asia and Pacific Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'East Asia and Pacific Subcommittee',
    'House',
    'hsfa05',
    'https://api.congress.gov/v3/committee/house/hsfa05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 174: Global Health, Global Human Rights, and International Organizations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Global Health, Global Human Rights, and International Organizations Subcommittee',
    'House',
    'hsfa06',
    'https://api.congress.gov/v3/committee/house/hsfa06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 175: Europe Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Europe Subcommittee',
    'House',
    'hsfa14',
    'https://api.congress.gov/v3/committee/house/hsfa14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 176: Africa Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Africa Subcommittee',
    'House',
    'hsfa16',
    'https://api.congress.gov/v3/committee/house/hsfa16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 177: National Security, Illicit Finance, and International Financial Institutions Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Security, Illicit Finance, and International Financial Institutions Subcommittee',
    'House',
    'hsba10',
    'https://api.congress.gov/v3/committee/house/hsba10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsba10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 178: Housing and Insurance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Housing and Insurance Subcommittee',
    'House',
    'hsba04',
    'https://api.congress.gov/v3/committee/house/hsba04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsba04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 179: Financial Institutions and Monetary Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Institutions and Monetary Policy Subcommittee',
    'House',
    'hsba20',
    'https://api.congress.gov/v3/committee/house/hsba20?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsba20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 180: Digital Assets, Financial Technology, and Artificial Intelligence Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Digital Assets, Financial Technology, and Artificial Intelligence Subcommittee',
    'House',
    'hsba21',
    'https://api.congress.gov/v3/committee/house/hsba21?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsba21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 181: Capital Markets Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Capital Markets Subcommittee',
    'House',
    'hsba16',
    'https://api.congress.gov/v3/committee/house/hsba16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsba16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 182: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsif02',
    'https://api.congress.gov/v3/committee/house/hsif02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsif02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 183: Commerce, Manufacturing, and Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Manufacturing, and Trade Subcommittee',
    'House',
    'hsif17',
    'https://api.congress.gov/v3/committee/house/hsif17?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsif17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 184: Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health Subcommittee',
    'House',
    'hsif14',
    'https://api.congress.gov/v3/committee/house/hsif14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsif14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 185: Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment Subcommittee',
    'House',
    'hsif18',
    'https://api.congress.gov/v3/committee/house/hsif18?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsif18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 186: Energy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Subcommittee',
    'House',
    'hsif03',
    'https://api.congress.gov/v3/committee/house/hsif03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsif03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 187: Communications and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Communications and Technology Subcommittee',
    'House',
    'hsif16',
    'https://api.congress.gov/v3/committee/house/hsif16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsif16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 188: Workforce Protections Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Workforce Protections Subcommittee',
    'House',
    'hsed10',
    'https://api.congress.gov/v3/committee/house/hsed10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsed10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 189: Higher Education and Workforce Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Higher Education and Workforce Development Subcommittee',
    'House',
    'hsed13',
    'https://api.congress.gov/v3/committee/house/hsed13?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsed13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 190: Health, Employment, Labor, and Pensions Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health, Employment, Labor, and Pensions Subcommittee',
    'House',
    'hsed02',
    'https://api.congress.gov/v3/committee/house/hsed02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsed02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 191: Early Childhood, Elementary, and Secondary Education Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Early Childhood, Elementary, and Secondary Education Subcommittee',
    'House',
    'hsed14',
    'https://api.congress.gov/v3/committee/house/hsed14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsed14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 192: Tactical Air and Land Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tactical Air and Land Forces Subcommittee',
    'House',
    'hsas25',
    'https://api.congress.gov/v3/committee/house/hsas25?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas25?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 193: Strategic Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Strategic Forces Subcommittee',
    'House',
    'hsas29',
    'https://api.congress.gov/v3/committee/house/hsas29?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas29?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 194: Seapower and Projection Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Seapower and Projection Forces Subcommittee',
    'House',
    'hsas28',
    'https://api.congress.gov/v3/committee/house/hsas28?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas28?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 195: Readiness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Readiness Subcommittee',
    'House',
    'hsas03',
    'https://api.congress.gov/v3/committee/house/hsas03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 196: Military Personnel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Personnel Subcommittee',
    'House',
    'hsas02',
    'https://api.congress.gov/v3/committee/house/hsas02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 197: Intelligence and Special Operations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intelligence and Special Operations Subcommittee',
    'House',
    'hsas26',
    'https://api.congress.gov/v3/committee/house/hsas26?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas26?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 198: Cyber, Information Technologies, and Innovation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cyber, Information Technologies, and Innovation Subcommittee',
    'House',
    'hsas35',
    'https://api.congress.gov/v3/committee/house/hsas35?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsas35?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 199: National Security, Department of State, and Related Programs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Security, Department of State, and Related Programs Subcommittee',
    'House',
    'hsap04',
    'https://api.congress.gov/v3/committee/house/hsap04?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 200: Interior, Environment, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Interior, Environment, and Related Agencies Subcommittee',
    'House',
    'hsap06',
    'https://api.congress.gov/v3/committee/house/hsap06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 200/815 committees processed

-- Committee 201: Defense Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Subcommittee',
    'House',
    'hsap02',
    'https://api.congress.gov/v3/committee/house/hsap02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 202: Energy and Water Development, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Water Development, and Related Agencies Subcommittee',
    'House',
    'hsap10',
    'https://api.congress.gov/v3/committee/house/hsap10?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 203: Transportation, Treasury and Independent Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation, Treasury and Independent Agencies Subcommittee',
    'House',
    'hsap14',
    'https://api.congress.gov/v3/committee/house/hsap14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 204: Department of Homeland Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department of Homeland Security Subcommittee',
    'House',
    'hsap15',
    'https://api.congress.gov/v3/committee/house/hsap15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 205: Military Construction, Veterans Affairs, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Construction, Veterans Affairs, and Related Agencies Subcommittee',
    'House',
    'hsap18',
    'https://api.congress.gov/v3/committee/house/hsap18?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 206: Departments of Transportation, and Housing and Urban Development, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Departments of Transportation, and Housing and Urban Development, and Related Agencies Subcommittee',
    'House',
    'hsap20',
    'https://api.congress.gov/v3/committee/house/hsap20?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 207: Commerce, Justice, Science, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Justice, Science, and Related Agencies Subcommittee',
    'House',
    'hsap19',
    'https://api.congress.gov/v3/committee/house/hsap19?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 208: Legislative Branch Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Legislative Branch Subcommittee',
    'House',
    'hsap24',
    'https://api.congress.gov/v3/committee/house/hsap24?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 209: Financial Services and General Government Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Services and General Government Subcommittee',
    'House',
    'hsap23',
    'https://api.congress.gov/v3/committee/house/hsap23?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 210: General Farm Commodities, Risk Management, and Credit Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'General Farm Commodities, Risk Management, and Credit Subcommittee',
    'House',
    'hsag16',
    'https://api.congress.gov/v3/committee/house/hsag16?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsag16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 211: Forestry and Horticulture Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Forestry and Horticulture Subcommittee',
    'House',
    'hsag15',
    'https://api.congress.gov/v3/committee/house/hsag15?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsag15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 212: Conservation, Research, and Biotechnology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Conservation, Research, and Biotechnology Subcommittee',
    'House',
    'hsag14',
    'https://api.congress.gov/v3/committee/house/hsag14?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsag14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 213: Commodity Markets, Digital Assets, and Rural Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commodity Markets, Digital Assets, and Rural Development Subcommittee',
    'House',
    'hsag22',
    'https://api.congress.gov/v3/committee/house/hsag22?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsag22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 214: Livestock, Dairy, and Poultry Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Livestock, Dairy, and Poultry Subcommittee',
    'House',
    'hsag29',
    'https://api.congress.gov/v3/committee/house/hsag29?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsag29?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 215: Labor, Health and Human Services, and Education Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Labor, Health and Human Services, and Education Subcommittee',
    'Senate',
    'ssap07',
    'https://api.congress.gov/v3/committee/senate/ssap07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 216: Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment Subcommittee',
    'House',
    'hsgo28',
    'https://api.congress.gov/v3/committee/house/hsgo28?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo28?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 217: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsba09',
    'https://api.congress.gov/v3/committee/house/hsba09?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsba09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 218: Departments of Labor, Health and Human Services, Education, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Departments of Labor, Health and Human Services, Education, and Related Agencies Subcommittee',
    'House',
    'hsap07',
    'https://api.congress.gov/v3/committee/house/hsap07?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 219: Agriculture, Rural Development, Food and Drug Administration, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Agriculture, Rural Development, Food and Drug Administration, and Related Agencies Subcommittee',
    'House',
    'hsap01',
    'https://api.congress.gov/v3/committee/house/hsap01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsap01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 220: Nutrition and Foreign Agriculture Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Nutrition and Foreign Agriculture Subcommittee',
    'House',
    'hsag03',
    'https://api.congress.gov/v3/committee/house/hsag03?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsag03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 221: Senate Joint Deficit Reduction Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Senate Joint Deficit Reduction Committee',
    'Senate',
    'jtdr00',
    'https://api.congress.gov/v3/committee/senate/jtdr00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/jtdr00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 222: Joint Select Deficit Reduction Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Select Deficit Reduction Committee',
    'Joint',
    'jsdf00',
    'https://api.congress.gov/v3/committee/joint/jsdf00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jsdf00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 223: Joint Select Committee on Budget and Appropriations Process Reform
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Select Committee on Budget and Appropriations Process Reform',
    'Joint',
    'jsba00',
    'https://api.congress.gov/v3/committee/joint/jsba00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jsba00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 224: Year 2000 Technology Problem (Special) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Year 2000 Technology Problem (Special) Committee',
    'Senate',
    'sp2k00',
    'https://api.congress.gov/v3/committee/senate/sp2k00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/sp2k00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 225: Ethics Enforcement Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ethics Enforcement Committee',
    'House',
    'hsqa00',
    'https://api.congress.gov/v3/committee/house/hsqa00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hsqa00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 226: Task Force on the Rural Elderly Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Task Force on the Rural Elderly Subcommittee',
    'House',
    'hlse06',
    'https://api.congress.gov/v3/committee/house/hlse06?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlse06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 227: Task Force on Social Security and Women Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Task Force on Social Security and Women Subcommittee',
    'House',
    'hlse05',
    'https://api.congress.gov/v3/committee/house/hlse05?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlse05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 228: International Task Force Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Task Force Subcommittee',
    'House',
    'hlhn01',
    'https://api.congress.gov/v3/committee/house/hlhn01?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlhn01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 229: Domestic Task Force Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic Task Force Subcommittee',
    'House',
    'hlhn02',
    'https://api.congress.gov/v3/committee/house/hlhn02?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hlhn02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 230: Antitrust (Full Committee Task Force) Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Antitrust (Full Committee Task Force) Subcommittee',
    'House',
    'hsju11',
    'https://api.congress.gov/v3/committee/house/hsju11?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hsju11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 231: Ad Hoc Task Force on Presidential Pay Recommendation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ad Hoc Task Force on Presidential Pay Recommendation Subcommittee',
    'House',
    'hspo08',
    'https://api.congress.gov/v3/committee/house/hspo08?format=json',
    true,
    true,
    'https://api.congress.gov/v3/committee/house/hspo08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 232: Select Investigate the January 6th Attack on the United States Capitol
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Investigate the January 6th Attack on the United States Capitol',
    'House',
    'hlij00',
    'https://api.congress.gov/v3/committee/house/hlij00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hlij00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 233: Commerce Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce Committee',
    'Senate',
    'n81096146',
    'https://api.congress.gov/v3/committee/senate/n81096146?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n81096146?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 234: Expenditures in the Agriculture Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Agriculture Department Committee',
    'House',
    'n2006005584',
    'https://api.congress.gov/v3/committee/house/n2006005584?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2006005584?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 235: Mines and Mining
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Mines and Mining',
    'Senate',
    'n79043123',
    'https://api.congress.gov/v3/committee/senate/n79043123?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n79043123?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 236: Naval Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Naval Affairs',
    'Senate',
    'n50081225',
    'https://api.congress.gov/v3/committee/senate/n50081225?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n50081225?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 237: Pacific Railroads
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Pacific Railroads',
    'Senate',
    'no2013136533',
    'https://api.congress.gov/v3/committee/senate/no2013136533?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no2013136533?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 238: Pensions
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Pensions',
    'Senate',
    'nr92040127',
    'https://api.congress.gov/v3/committee/senate/nr92040127?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/nr92040127?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 239: Revolutionary Claims
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Revolutionary Claims',
    'Senate',
    'n2006083967',
    'https://api.congress.gov/v3/committee/senate/n2006083967?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2006083967?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 240: Rules
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rules',
    'Senate',
    'no2004044998',
    'https://api.congress.gov/v3/committee/senate/no2004044998?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no2004044998?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 241: Retrenchment
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Retrenchment',
    'Senate',
    'n2006083963',
    'https://api.congress.gov/v3/committee/senate/n2006083963?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2006083963?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 242: Printing
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Printing',
    'Senate',
    'no94026591',
    'https://api.congress.gov/v3/committee/senate/no94026591?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no94026591?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 243: Public Buildings and Grounds
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Buildings and Grounds',
    'Senate',
    'n85188720',
    'https://api.congress.gov/v3/committee/senate/n85188720?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n85188720?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 244: Public Health and National Quarantine
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Health and National Quarantine',
    'Senate',
    'n50083181',
    'https://api.congress.gov/v3/committee/senate/n50083181?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n50083181?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 245: Philippines
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Philippines',
    'Senate',
    'n50077731',
    'https://api.congress.gov/v3/committee/senate/n50077731?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n50077731?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 246: Railroads
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Railroads',
    'Senate',
    'no94032278',
    'https://api.congress.gov/v3/committee/senate/no94032278?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no94032278?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 247: Post Offices and Post Roads
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Post Offices and Post Roads',
    'Senate',
    'n50083180',
    'https://api.congress.gov/v3/committee/senate/n50083180?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n50083180?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 248: Manufactures
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Manufactures',
    'Senate',
    'n81096147',
    'https://api.congress.gov/v3/committee/senate/n81096147?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n81096147?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 249: Military Affairs
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Affairs',
    'Senate',
    'n79055978',
    'https://api.congress.gov/v3/committee/senate/n79055978?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n79055978?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 250: Industrial Expositions
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Industrial Expositions',
    'Senate',
    'n2011037996',
    'https://api.congress.gov/v3/committee/senate/n2011037996?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2011037996?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 251: Forest Reservations and the Protection of Game
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Forest Reservations and the Protection of Game',
    'Senate',
    'n2008076716',
    'https://api.congress.gov/v3/committee/senate/n2008076716?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2008076716?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 252: Indian Depredations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Indian Depredations',
    'Senate',
    'no96026568',
    'https://api.congress.gov/v3/committee/senate/no96026568?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no96026568?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 253: Industrial Expositions
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Industrial Expositions',
    'Senate',
    'n2011037996',
    'https://api.congress.gov/v3/committee/senate/n2011037996?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2011037996?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 254: Interstate Commerce
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Interstate Commerce',
    'Senate',
    'n81096149',
    'https://api.congress.gov/v3/committee/senate/n81096149?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n81096149?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 255: Manufactures
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Manufactures',
    'Senate',
    'n81096147',
    'https://api.congress.gov/v3/committee/senate/n81096147?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n81096147?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 256: Irrigation and Reclamation
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Irrigation and Reclamation',
    'Senate',
    'n79043122',
    'https://api.congress.gov/v3/committee/senate/n79043122?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n79043122?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 257: Civil Service and Retrenchment
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Service and Retrenchment',
    'Senate',
    'n2005025889',
    'https://api.congress.gov/v3/committee/senate/n2005025889?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2005025889?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 258: Cuban Relations
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cuban Relations',
    'Senate',
    'n2006083954',
    'https://api.congress.gov/v3/committee/senate/n2006083954?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2006083954?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 259: Expenditures in the Executive Departments
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Executive Departments',
    'Senate',
    'n88030116',
    'https://api.congress.gov/v3/committee/senate/n88030116?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n88030116?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 260: Civil Service
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Service',
    'Senate',
    'n2005026015',
    'https://api.congress.gov/v3/committee/senate/n2005026015?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2005026015?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 261: Census
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Census',
    'Senate',
    'n2006083948',
    'https://api.congress.gov/v3/committee/senate/n2006083948?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2006083948?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 262: Audit and Control of the Contingent Expenses of the Senate
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Audit and Control of the Contingent Expenses of the Senate',
    'Senate',
    'nr93031597',
    'https://api.congress.gov/v3/committee/senate/nr93031597?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/nr93031597?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 263: Coast Defenses
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Coast Defenses',
    'Senate',
    'n2005042729',
    'https://api.congress.gov/v3/committee/senate/n2005042729?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2005042729?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 264: Coastal and Insular Survey
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Coastal and Insular Survey',
    'Senate',
    'n2007025578',
    'https://api.congress.gov/v3/committee/senate/n2007025578?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n2007025578?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 265: Claims
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Claims',
    'Senate',
    'nr92039132',
    'https://api.congress.gov/v3/committee/senate/nr92039132?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/nr92039132?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 266: Commerce and Manufactures
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce and Manufactures',
    'Senate',
    'n81096145',
    'https://api.congress.gov/v3/committee/senate/n81096145?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n81096145?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 267: Privileges and Elections Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Privileges and Elections Committee',
    'Senate',
    'n85113718',
    'https://api.congress.gov/v3/committee/senate/n85113718?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n85113718?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 268: Patents Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Patents Committee',
    'Senate',
    'no2004111834',
    'https://api.congress.gov/v3/committee/senate/no2004111834?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no2004111834?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 269: Immigration Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Immigration Committee',
    'Senate',
    'no00001702',
    'https://api.congress.gov/v3/committee/senate/no00001702?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/no00001702?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 270: Mileage Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Mileage Committee',
    'House',
    'nr97009062',
    'https://api.congress.gov/v3/committee/house/nr97009062?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr97009062?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 271: World War Veterans'' Legislation Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'World War Veterans'' Legislation Committee',
    'House',
    'n81096142',
    'https://api.congress.gov/v3/committee/house/n81096142?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n81096142?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 272: Woman Suffrage Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Woman Suffrage Committee',
    'House',
    'n95033314',
    'https://api.congress.gov/v3/committee/house/n95033314?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n95033314?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 273: War Claims Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'War Claims Committee',
    'House',
    'no94029614',
    'https://api.congress.gov/v3/committee/house/no94029614?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no94029614?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 274: Ventilation and Acoustics Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ventilation and Acoustics Committee',
    'House',
    'no2010049600',
    'https://api.congress.gov/v3/committee/house/no2010049600?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no2010049600?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 275: Territories Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Territories Committee',
    'House',
    'n50080783',
    'https://api.congress.gov/v3/committee/house/n50080783?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n50080783?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 276: Roads Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Roads Committee',
    'House',
    'no99051135',
    'https://api.congress.gov/v3/committee/house/no99051135?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no99051135?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 277: Rivers and Harbors Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rivers and Harbors Committee',
    'House',
    'n85185939',
    'https://api.congress.gov/v3/committee/house/n85185939?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n85185939?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 278: Revolutionary Pensions Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Revolutionary Pensions Committee',
    'House',
    'nr93007702',
    'https://api.congress.gov/v3/committee/house/nr93007702?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr93007702?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 279: Revision of the Laws Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Revision of the Laws Committee',
    'House',
    'n79036853',
    'https://api.congress.gov/v3/committee/house/n79036853?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n79036853?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 280: Reform in the Civil Service Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Reform in the Civil Service Committee',
    'House',
    'no2003106805',
    'https://api.congress.gov/v3/committee/house/no2003106805?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no2003106805?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 281: Railways and Canals Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Railways and Canals Committee',
    'House',
    'nr2004025444',
    'https://api.congress.gov/v3/committee/house/nr2004025444?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr2004025444?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 282: Public Expenditures Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Expenditures Committee',
    'House',
    'nr93025509',
    'https://api.congress.gov/v3/committee/house/nr93025509?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr93025509?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 283: Public Buildings and Grounds Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Buildings and Grounds Committee',
    'House',
    'n88156927',
    'https://api.congress.gov/v3/committee/house/n88156927?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n88156927?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 284: Private Land Claims Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Private Land Claims Committee',
    'House',
    'n88636576',
    'https://api.congress.gov/v3/committee/house/n88636576?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n88636576?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 285: Post Office and Post Roads Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Post Office and Post Roads Committee',
    'House',
    'n88256891',
    'https://api.congress.gov/v3/committee/house/n88256891?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n88256891?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 286: Pensions Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Pensions Committee',
    'House',
    'n81096143',
    'https://api.congress.gov/v3/committee/house/n81096143?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n81096143?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 287: Patents Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Patents Committee',
    'House',
    'n79036852',
    'https://api.congress.gov/v3/committee/house/n79036852?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n79036852?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 288: Pacific Railroad Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Pacific Railroad Committee',
    'House',
    'no2009135915',
    'https://api.congress.gov/v3/committee/house/no2009135915?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no2009135915?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 289: Naval Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Naval Affairs Committee',
    'House',
    'n81038422',
    'https://api.congress.gov/v3/committee/house/n81038422?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n81038422?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 290: Mines and Mining Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Mines and Mining Committee',
    'House',
    'no94034726',
    'https://api.congress.gov/v3/committee/house/no94034726?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no94034726?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 291: Military Pensions Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Pensions Committee',
    'House',
    'nr95003115',
    'https://api.congress.gov/v3/committee/house/nr95003115?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr95003115?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 292: Military Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Affairs Committee',
    'House',
    'n81038421',
    'https://api.congress.gov/v3/committee/house/n81038421?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n81038421?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 293: Militia Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Militia Committee',
    'House',
    'nr95012879',
    'https://api.congress.gov/v3/committee/house/nr95012879?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr95012879?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 294: Manufactures Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Manufactures Committee',
    'House',
    'n79047544',
    'https://api.congress.gov/v3/committee/house/n79047544?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n79047544?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 295: Levees and Improvements of the Mississippi River Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Levees and Improvements of the Mississippi River Committee',
    'House',
    'no2009049242',
    'https://api.congress.gov/v3/committee/house/no2009049242?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no2009049242?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 296: Labor Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Labor Committee',
    'House',
    'n79049131',
    'https://api.congress.gov/v3/committee/house/n79049131?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n79049131?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 297: Irrigation of Arid Lands Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Irrigation of Arid Lands Committee',
    'House',
    'n2005041565',
    'https://api.congress.gov/v3/committee/house/n2005041565?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2005041565?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 298: Irrigation and Reclamation Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Irrigation and Reclamation Committee',
    'House',
    'no94034730',
    'https://api.congress.gov/v3/committee/house/no94034730?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no94034730?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 299: Invalid Pensions Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Invalid Pensions Committee',
    'House',
    'n81096141',
    'https://api.congress.gov/v3/committee/house/n81096141?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n81096141?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 300: Insular Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Insular Affairs Committee',
    'House',
    'no94034735',
    'https://api.congress.gov/v3/committee/house/no94034735?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no94034735?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 300/815 committees processed

-- Committee 301: Industrial Arts and Expositions Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Industrial Arts and Expositions Committee',
    'House',
    'no2003009975',
    'https://api.congress.gov/v3/committee/house/no2003009975?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no2003009975?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 302: Indian Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Indian Affairs Committee',
    'House',
    'n80146651',
    'https://api.congress.gov/v3/committee/house/n80146651?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n80146651?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 303: Immigration and Naturalization Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Immigration and Naturalization Committee',
    'House',
    'n79036851',
    'https://api.congress.gov/v3/committee/house/n79036851?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n79036851?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 304: Freedmen''s Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Freedmen''s Affairs Committee',
    'House',
    'nr00013789',
    'https://api.congress.gov/v3/committee/house/nr00013789?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr00013789?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 305: Flood Control Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Flood Control Committee',
    'House',
    'n85053458',
    'https://api.congress.gov/v3/committee/house/n85053458?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n85053458?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 306: Expenditures on the Public Buildings Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures on the Public Buildings Committee',
    'House',
    'nr93024937',
    'https://api.congress.gov/v3/committee/house/nr93024937?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr93024937?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 307: Expenditures in the War Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the War Department Committee',
    'House',
    'n88663430',
    'https://api.congress.gov/v3/committee/house/n88663430?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n88663430?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 308: Expenditures in the Treasury Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Treasury Department Committee',
    'House',
    'nr93017700',
    'https://api.congress.gov/v3/committee/house/nr93017700?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr93017700?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 309: Expenditures in the State Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the State Department Committee',
    'House',
    'nr94041327',
    'https://api.congress.gov/v3/committee/house/nr94041327?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr94041327?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 310: Expenditures in the Post-Office Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Post-Office Department Committee',
    'House',
    'n2005089915',
    'https://api.congress.gov/v3/committee/house/n2005089915?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2005089915?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 311: Expenditures in the Navy Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Navy Department Committee',
    'House',
    'nr93007908',
    'https://api.congress.gov/v3/committee/house/nr93007908?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr93007908?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 312: Expenditures in the Justice Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Justice Department Committee',
    'House',
    'n2006005638',
    'https://api.congress.gov/v3/committee/house/n2006005638?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2006005638?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 313: Expenditures in the Department of Commerce Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in the Department of Commerce Committee',
    'House',
    'n2006005654',
    'https://api.congress.gov/v3/committee/house/n2006005654?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2006005654?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 314: Elections no. 2 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Elections no. 2 Committee',
    'House',
    'n2007069112',
    'https://api.congress.gov/v3/committee/house/n2007069112?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2007069112?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 315: Elections no. 1 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Elections no. 1 Committee',
    'House',
    'n2007069138',
    'https://api.congress.gov/v3/committee/house/n2007069138?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2007069138?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 316: Elections Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Elections Committee',
    'House',
    'n88001560',
    'https://api.congress.gov/v3/committee/house/n88001560?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n88001560?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 317: Election of President, Vice President, and Representatives in Congress Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Election of President, Vice President, and Representatives in Congress Committee',
    'House',
    'n2006005529',
    'https://api.congress.gov/v3/committee/house/n2006005529?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2006005529?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 318: Coinage, Weights, and Measures Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Coinage, Weights, and Measures Committee',
    'House',
    'n81025902',
    'https://api.congress.gov/v3/committee/house/n81025902?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n81025902?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 319: Claims Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Claims Committee',
    'House',
    'n50078971',
    'https://api.congress.gov/v3/committee/house/n50078971?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n50078971?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 320: Civil Service Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Service Committee',
    'House',
    'no2003009976',
    'https://api.congress.gov/v3/committee/house/no2003009976?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no2003009976?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 321: Census Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Census Committee',
    'House',
    'no98108649',
    'https://api.congress.gov/v3/committee/house/no98108649?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no98108649?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 322: Accounts Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Accounts Committee',
    'House',
    'nr95008630',
    'https://api.congress.gov/v3/committee/house/nr95008630?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/nr95008630?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 323: Congressional Oversight Commission
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Congressional Oversight Commission',
    'Joint',
    'jcov00',
    'https://api.congress.gov/v3/committee/joint/jcov00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/joint/jcov00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 324: Oversight and Government Reform Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Government Reform Committee',
    'House',
    'hsgo00',
    'https://api.congress.gov/v3/committee/house/hsgo00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hsgo00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 325: Judiciary Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Judiciary Committee',
    'House',
    'hsju00',
    'https://api.congress.gov/v3/committee/house/hsju00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hsju00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 326: Roads and Canals Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Roads and Canals Committee',
    'Senate',
    'nr92024277',
    'https://api.congress.gov/v3/committee/senate/nr92024277?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/nr92024277?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 327: Private Land Claims Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Private Land Claims Committee',
    'Senate',
    'n87901340',
    'https://api.congress.gov/v3/committee/senate/n87901340?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/senate/n87901340?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 328: Expenditures in Interior Department Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expenditures in Interior Department Committee',
    'House',
    'no90011669',
    'https://api.congress.gov/v3/committee/house/no90011669?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/no90011669?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 329: Alcoholic Liquor Traffic Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Alcoholic Liquor Traffic Committee',
    'House',
    'n2006001899',
    'https://api.congress.gov/v3/committee/house/n2006001899?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/n2006001899?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 330: Select Committee on the Strategic Competition Between the United States and the Chinese Communist Party
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on the Strategic Competition Between the United States and the Chinese Communist Party',
    'House',
    'hlzs00',
    'https://api.congress.gov/v3/committee/house/hlzs00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hlzs00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 331: Education and Workforce Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Education and Workforce Committee',
    'House',
    'hsed00',
    'https://api.congress.gov/v3/committee/house/hsed00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hsed00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 332: Select Committee on the Climate Crisis
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on the Climate Crisis',
    'House',
    'hlcn00',
    'https://api.congress.gov/v3/committee/house/hlcn00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hlcn00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 333: Select Committee on Economic Disparity and Fairness in Growth
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on Economic Disparity and Fairness in Growth',
    'House',
    'hlef00',
    'https://api.congress.gov/v3/committee/house/hlef00?format=json',
    true,
    false,
    'https://api.congress.gov/v3/committee/house/hlef00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 334: Select Committee on Secret Military Assistance to Iran and the Nicaraguan Opposition
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on Secret Military Assistance to Iran and the Nicaraguan Opposition',
    'Senate',
    'slso00',
    'https://api.congress.gov/v3/committee/senate/slso00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/slso00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 335: U.S.-China Economic and Security Review Commission
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'U.S.-China Economic and Security Review Commission',
    'Joint',
    'jcuc00',
    'https://api.congress.gov/v3/committee/joint/jcuc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jcuc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 336: Joint Select Committee on Solvency of Multiemployer Pension Plans
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Select Committee on Solvency of Multiemployer Pension Plans',
    'Joint',
    'jspp00',
    'https://api.congress.gov/v3/committee/joint/jspp00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jspp00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 337: Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigations Subcommittee',
    'Senate',
    'slia01',
    'https://api.congress.gov/v3/committee/senate/slia01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/slia01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 338: Economic Goals and Intergovernmental Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Goals and Intergovernmental Policy Subcommittee',
    'Senate',
    'jsec03',
    'https://api.congress.gov/v3/committee/senate/jsec03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/jsec03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 339: Congressional Oversight Panel
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Congressional Oversight Panel',
    'Joint',
    'jocp00',
    'https://api.congress.gov/v3/committee/joint/jocp00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jocp00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 340: Response to Hurricane Katrina Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Response to Hurricane Katrina Committee',
    'House',
    'hlhk00',
    'https://api.congress.gov/v3/committee/house/hlhk00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlhk00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 341: U.S. National and Military/Commercial Concerns with China (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'U.S. National and Military/Commercial Concerns with China (Select) Committee',
    'House',
    'hlrk00',
    'https://api.congress.gov/v3/committee/house/hlrk00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlrk00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 342: Senate National Security Working Group
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Senate National Security Working Group',
    'Senate',
    'sowg00',
    'https://api.congress.gov/v3/committee/senate/sowg00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/sowg00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 343: Joint Atomic Energy Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Atomic Energy Committee',
    'Senate',
    'jsat00',
    'https://api.congress.gov/v3/committee/senate/jsat00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/jsat00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 344: Tom Lantos Human Rights Commission
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tom Lantos Human Rights Commission',
    'House',
    'hotl00',
    'https://api.congress.gov/v3/committee/house/hotl00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hotl00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 345: Joint Atomic Energy Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Atomic Energy Committee',
    'House',
    'hsat00',
    'https://api.congress.gov/v3/committee/house/hsat00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsat00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 346: Select Committee on Ethics (105th)
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on Ethics (105th)',
    'House',
    'hleb00',
    'https://api.congress.gov/v3/committee/house/hleb00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hleb00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 347: POW/MIA Affairs (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'POW/MIA Affairs (Select) Committee',
    'Senate',
    'slpo00',
    'https://api.congress.gov/v3/committee/senate/slpo00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/slpo00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 348: Children, Youth, and Families (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Children, Youth, and Families (Select) Committee',
    'House',
    'hlcf00',
    'https://api.congress.gov/v3/committee/house/hlcf00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlcf00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 349: Aging (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aging (Select) Committee',
    'House',
    'hlse00',
    'https://api.congress.gov/v3/committee/house/hlse00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlse00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 350: Energy Independence and Global Warming (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Independence and Global Warming (Select) Committee',
    'House',
    'hlgw00',
    'https://api.congress.gov/v3/committee/house/hlgw00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlgw00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 351: Transportation and Infrastructure Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation and Infrastructure Committee',
    'House',
    'hspw00',
    'https://api.congress.gov/v3/committee/house/hspw00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hspw00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 352: Whole House on State of Union Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Whole House on State of Union Committee',
    'House',
    'hshf00',
    'https://api.congress.gov/v3/committee/house/hshf00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hshf00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 353: Financial Services Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Services Committee',
    'House',
    'hsba00',
    'https://api.congress.gov/v3/committee/house/hsba00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsba00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 354: Impeachment Trial Committee on the Articles Against Judge G. Thomas Porteous, Jr.
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Impeachment Trial Committee on the Articles Against Judge G. Thomas Porteous, Jr.',
    'Senate',
    'spia00',
    'https://api.congress.gov/v3/committee/senate/spia00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spia00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 355: Agriculture Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Agriculture Committee',
    'House',
    'hsag00',
    'https://api.congress.gov/v3/committee/house/hsag00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsag00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 356: Ethics Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ethics Committee',
    'House',
    'hsso00',
    'https://api.congress.gov/v3/committee/house/hsso00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsso00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 357: Strategic Technologies and Advanced Research Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Strategic Technologies and Advanced Research Subcommittee',
    'House',
    'hlig10',
    'https://api.congress.gov/v3/committee/house/hlig10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlig10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 358: Terrorism and Illicit Finance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Terrorism and Illicit Finance Subcommittee',
    'House',
    'hsba01',
    'https://api.congress.gov/v3/committee/house/hsba01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 359: Small Business Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Small Business Committee',
    'House',
    'hssm00',
    'https://api.congress.gov/v3/committee/house/hssm00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hssm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 360: Manufacturing, Trade, and Consumer Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Manufacturing, Trade, and Consumer Protection Subcommittee',
    'Senate',
    'sscm29',
    'https://api.congress.gov/v3/committee/senate/sscm29?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm29?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 361: Transportation and Safety Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation and Safety Subcommittee',
    'Senate',
    'sscm32',
    'https://api.congress.gov/v3/committee/senate/sscm32?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm32?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 362: Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Security Subcommittee',
    'Senate',
    'sscm31',
    'https://api.congress.gov/v3/committee/senate/sscm31?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm31?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 363: Aviation and Space Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aviation and Space Subcommittee',
    'Senate',
    'sscm28',
    'https://api.congress.gov/v3/committee/senate/sscm28?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm28?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 364: Appropriations Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Appropriations Committee',
    'House',
    'hsap00',
    'https://api.congress.gov/v3/committee/house/hsap00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsap00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 365: Foreign Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Foreign Affairs Committee',
    'House',
    'hsfa00',
    'https://api.congress.gov/v3/committee/house/hsfa00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsfa00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 366: Expedited Procedures
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Expedited Procedures',
    'House',
    'hsru05',
    'https://api.congress.gov/v3/committee/house/hsru05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsru05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 367: Investigate Whitewater Development Corporation and Related Matters (Special) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigate Whitewater Development Corporation and Related Matters (Special) Committee',
    'Senate',
    'spww00',
    'https://api.congress.gov/v3/committee/senate/spww00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spww00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 368: Armed Services Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Armed Services Committee',
    'House',
    'hsas00',
    'https://api.congress.gov/v3/committee/house/hsas00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsas00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 369: Natural Resources Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Natural Resources Committee',
    'House',
    'hsii00',
    'https://api.congress.gov/v3/committee/house/hsii00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsii00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 370: Intelligence (Permanent Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intelligence (Permanent Select) Committee',
    'House',
    'hlig00',
    'https://api.congress.gov/v3/committee/house/hlig00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlig00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 371: Ways and Means Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ways and Means Committee',
    'House',
    'hswm00',
    'https://api.congress.gov/v3/committee/house/hswm00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hswm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 372: Regulatory Affairs and Federal Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regulatory Affairs and Federal Management Subcommittee',
    'Senate',
    'ssga19',
    'https://api.congress.gov/v3/committee/senate/ssga19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 373: Select Committee on the Events Surrounding the 2012 Terrorist Attack in Benghazi Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on the Events Surrounding the 2012 Terrorist Attack in Benghazi Committee',
    'House',
    'hlzi00',
    'https://api.congress.gov/v3/committee/house/hlzi00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlzi00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 374: Ethics (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ethics (Select) Committee',
    'House',
    'hlet00',
    'https://api.congress.gov/v3/committee/house/hlet00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlet00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 375: Science, Space, and Technology Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Science, Space, and Technology Committee',
    'House',
    'hssy00',
    'https://api.congress.gov/v3/committee/house/hssy00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hssy00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 376: Veterans'' Affairs Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Veterans'' Affairs Committee',
    'House',
    'hsvr00',
    'https://api.congress.gov/v3/committee/house/hsvr00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsvr00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 377: Committee on House Administration
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Committee on House Administration',
    'House',
    'hsha00',
    'https://api.congress.gov/v3/committee/house/hsha00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsha00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 378: Homeland Security Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Homeland Security Committee',
    'House',
    'hshm00',
    'https://api.congress.gov/v3/committee/house/hshm00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hshm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 379: Energy and Commerce Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Commerce Committee',
    'House',
    'hsif00',
    'https://api.congress.gov/v3/committee/house/hsif00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsif00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 380: Rules Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rules Committee',
    'House',
    'hsru00',
    'https://api.congress.gov/v3/committee/house/hsru00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsru00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 381: Select Committee on Committees Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee on Committees Committee',
    'House',
    'hlcq00',
    'https://api.congress.gov/v3/committee/house/hlcq00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlcq00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 382: Inaugural Ceremonies - 2004 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 2004 Committee',
    'Joint',
    'jsie00',
    'https://api.congress.gov/v3/committee/joint/jsie00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsie00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 383: Inaugural Ceremonies - 1996 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 1996 Committee',
    'Joint',
    'jsic00',
    'https://api.congress.gov/v3/committee/joint/jsic00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsic00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 384: Inaugural Ceremonies - 1988 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 1988 Committee',
    'Joint',
    'jsia00',
    'https://api.congress.gov/v3/committee/joint/jsia00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsia00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 385: IRS Restructuring Commission Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'IRS Restructuring Commission Committee',
    'Joint',
    'jcir00',
    'https://api.congress.gov/v3/committee/joint/jcir00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jcir00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 386: Medicare Commission Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Medicare Commission Committee',
    'Joint',
    'jcfm00',
    'https://api.congress.gov/v3/committee/joint/jcfm00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jcfm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 387: Hostages Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Hostages Committee',
    'House',
    'htht00',
    'https://api.congress.gov/v3/committee/house/htht00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/htht00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 388: Joint Deficit Reduction Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Joint Deficit Reduction Committee',
    'House',
    'htde00',
    'https://api.congress.gov/v3/committee/house/htde00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/htde00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 389: Internal Security Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Internal Security Committee',
    'House',
    'hsua00',
    'https://api.congress.gov/v3/committee/house/hsua00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsua00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 390: Post Office and Civil Service Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Post Office and Civil Service Committee',
    'House',
    'hspo00',
    'https://api.congress.gov/v3/committee/house/hspo00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hspo00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 391: Merchant Marine and Fisheries Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Merchant Marine and Fisheries Committee',
    'House',
    'hsmm00',
    'https://api.congress.gov/v3/committee/house/hsmm00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsmm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 392: District of Columbia Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'District of Columbia Committee',
    'House',
    'hsdt00',
    'https://api.congress.gov/v3/committee/house/hsdt00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsdt00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 393: Budget Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Budget Committee',
    'House',
    'hsbu00',
    'https://api.congress.gov/v3/committee/house/hsbu00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsbu00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 394: Assassinations Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Assassinations Committee',
    'House',
    'hlzc00',
    'https://api.congress.gov/v3/committee/house/hlzc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlzc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 395: Secret and Confidential Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Secret and Confidential Committee',
    'Senate',
    'spzm00',
    'https://api.congress.gov/v3/committee/senate/spzm00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spzm00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 396: National Emergencies Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Emergencies Committee',
    'Senate',
    'spzk00',
    'https://api.congress.gov/v3/committee/senate/spzk00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spzk00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 397: Impeachment Trial Committee on the Articles Against Judge Walter L. Nixon, Jr.
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Impeachment Trial Committee on the Articles Against Judge Walter L. Nixon, Jr.',
    'Senate',
    'sptr00',
    'https://api.congress.gov/v3/committee/senate/sptr00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/sptr00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 398: District of Columbia Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'District of Columbia Committee',
    'Senate',
    'ssdt00',
    'https://api.congress.gov/v3/committee/senate/ssdt00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/ssdt00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 399: Post Office and Civil Service Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Post Office and Civil Service Committee',
    'Senate',
    'sspo00',
    'https://api.congress.gov/v3/committee/senate/sspo00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/sspo00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 400: Inaugural Ceremonies - 2012 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 2012 Committee',
    'Joint',
    'jsig00',
    'https://api.congress.gov/v3/committee/joint/jsig00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsig00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 400/815 committees processed

-- Committee 401: Official Conduct (Special) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Official Conduct (Special) Committee',
    'Senate',
    'spoc00',
    'https://api.congress.gov/v3/committee/senate/spoc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spoc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 402: Impeachment Trial Committee on the Articles Against Judge Alcee L. Hastings
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Impeachment Trial Committee on the Articles Against Judge Alcee L. Hastings',
    'Senate',
    'spim00',
    'https://api.congress.gov/v3/committee/senate/spim00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spim00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 403: Special Committee on the Impeachment Trial of Judge Harry E. Claiborne
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Special Committee on the Impeachment Trial of Judge Harry E. Claiborne',
    'Senate',
    'spie00',
    'https://api.congress.gov/v3/committee/senate/spie00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/spie00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 404: Watergate Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Watergate Committee',
    'Senate',
    'slzp00',
    'https://api.congress.gov/v3/committee/senate/slzp00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/slzp00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 405: Study Intelligence Activities Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Study Intelligence Activities Committee',
    'Senate',
    'slzj00',
    'https://api.congress.gov/v3/committee/senate/slzj00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/slzj00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 406: Undercover Activities Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Undercover Activities Committee',
    'Senate',
    'sluc00',
    'https://api.congress.gov/v3/committee/senate/sluc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/sluc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 407: Study Committee System Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Study Committee System Committee',
    'Senate',
    'sltc00',
    'https://api.congress.gov/v3/committee/senate/sltc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/sltc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 408: Narcotics Abuse and Control Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Narcotics Abuse and Control Committee',
    'House',
    'hlna00',
    'https://api.congress.gov/v3/committee/house/hlna00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlna00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 409: Population Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Population Committee',
    'House',
    'hlze00',
    'https://api.congress.gov/v3/committee/house/hlze00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlze00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 410: Ethics Study Commission Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ethics Study Commission Committee',
    'Senate',
    'scet00',
    'https://api.congress.gov/v3/committee/senate/scet00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/scet00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 411: Organization of Congress Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Organization of Congress Committee',
    'Joint',
    'jsoc00',
    'https://api.congress.gov/v3/committee/joint/jsoc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsoc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 412: Defense Production Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Production Committee',
    'Joint',
    'jsjx00',
    'https://api.congress.gov/v3/committee/joint/jsjx00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsjx00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 413: Inaugural Ceremonies - 2008 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 2008 Committee',
    'Joint',
    'jsif00',
    'https://api.congress.gov/v3/committee/joint/jsif00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsif00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 414: Investigate Campaign Expenditures Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigate Campaign Expenditures Committee',
    'House',
    'hpzh00',
    'https://api.congress.gov/v3/committee/house/hpzh00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hpzh00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 415: The Pepper Commission Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'The Pepper Commission Committee',
    'Joint',
    'jchc00',
    'https://api.congress.gov/v3/committee/joint/jchc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jchc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 416: Inaugural Ceremonies - 1992 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 1992 Committee',
    'Joint',
    'jsib00',
    'https://api.congress.gov/v3/committee/joint/jsib00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsib00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 417: Inaugural Ceremonies - 2016 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 2016 Committee',
    'Joint',
    'jsih00',
    'https://api.congress.gov/v3/committee/joint/jsih00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsih00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 418: Select Panel Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Panel Committee',
    'House',
    'hlie00',
    'https://api.congress.gov/v3/committee/house/hlie00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlie00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 419: Budget Control Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Budget Control Committee',
    'Joint',
    'jsjz00',
    'https://api.congress.gov/v3/committee/joint/jsjz00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsjz00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 420: Inaugural Ceremonies - 2000 Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Inaugural Ceremonies - 2000 Committee',
    'Joint',
    'jsid00',
    'https://api.congress.gov/v3/committee/joint/jsid00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsid00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 421: Professional Sports Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Professional Sports Committee',
    'House',
    'hlzg00',
    'https://api.congress.gov/v3/committee/house/hlzg00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlzg00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 422: Missing Persons Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Missing Persons Committee',
    'House',
    'hlzf00',
    'https://api.congress.gov/v3/committee/house/hlzf00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlzf00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 423: Congressional Operations Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Congressional Operations Committee',
    'House',
    'hlzd00',
    'https://api.congress.gov/v3/committee/house/hlzd00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlzd00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 424: Aeronautical and Space Sciences Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aeronautical and Space Sciences Committee',
    'Senate',
    'ssae00',
    'https://api.congress.gov/v3/committee/senate/ssae00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/senate/ssae00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 425: Outer Continental Shelf (Select) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Outer Continental Shelf (Select) Committee',
    'House',
    'hloc00',
    'https://api.congress.gov/v3/committee/house/hloc00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hloc00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 426: Covert Arms Deals with Iran Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Covert Arms Deals with Iran Committee',
    'House',
    'hlir00',
    'https://api.congress.gov/v3/committee/house/hlir00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlir00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 427: Hunger Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Hunger Committee',
    'House',
    'hlhn00',
    'https://api.congress.gov/v3/committee/house/hlhn00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlhn00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 428: U.S. Role in Iranian Arms Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'U.S. Role in Iranian Arms Committee',
    'House',
    'hlbz00',
    'https://api.congress.gov/v3/committee/house/hlbz00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hlbz00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 429: Energy (Ad Hoc) Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy (Ad Hoc) Committee',
    'House',
    'hhah00',
    'https://api.congress.gov/v3/committee/house/hhah00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hhah00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 430: Bicentenary Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Bicentenary Committee',
    'House',
    'hcza00',
    'https://api.congress.gov/v3/committee/house/hcza00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hcza00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 431: Congressional Operations Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Congressional Operations Committee',
    'Joint',
    'jsjy00',
    'https://api.congress.gov/v3/committee/joint/jsjy00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/joint/jsjy00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 432: Select Committee to Investigate the Voting Irregularities of August 2, 2007
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Select Committee to Investigate the Voting Irregularities of August 2, 2007',
    'House',
    'hsro00',
    'https://api.congress.gov/v3/committee/house/hsro00?format=json',
    false,
    false,
    'https://api.congress.gov/v3/committee/house/hsro00?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 433: Urban and Minority-Owned Business Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Urban and Minority-Owned Business Development Subcommittee',
    'Senate',
    'sssb06',
    'https://api.congress.gov/v3/committee/senate/sssb06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 434: Innovation, Manufacturing, and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Innovation, Manufacturing, and Technology Subcommittee',
    'Senate',
    'sssb04',
    'https://api.congress.gov/v3/committee/senate/sssb04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 435: Advocacy and The Future of Small Business Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Advocacy and The Future of Small Business Subcommittee',
    'Senate',
    'sssb08',
    'https://api.congress.gov/v3/committee/senate/sssb08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 436: Competitiveness, Capital Formation and Economic Opportunity Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Competitiveness, Capital Formation and Economic Opportunity Subcommittee',
    'Senate',
    'sssb07',
    'https://api.congress.gov/v3/committee/senate/sssb07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 437: Government Contracting and Paperwork Reduction Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Government Contracting and Paperwork Reduction Subcommittee',
    'Senate',
    'sssb02',
    'https://api.congress.gov/v3/committee/senate/sssb02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 438: Competition and Antitrust Enforcement Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Competition and Antitrust Enforcement Subcommittee',
    'Senate',
    'sssb05',
    'https://api.congress.gov/v3/committee/senate/sssb05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 439: Entrepreneurship and Special Problems Facing Small Business Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Entrepreneurship and Special Problems Facing Small Business Subcommittee',
    'Senate',
    'sssb12',
    'https://api.congress.gov/v3/committee/senate/sssb12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 440: Small Business: Family Farm Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Small Business: Family Farm Subcommittee',
    'Senate',
    'sssb11',
    'https://api.congress.gov/v3/committee/senate/sssb11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 441: Rural Economy and Family Farming Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rural Economy and Family Farming Subcommittee',
    'Senate',
    'sssb03',
    'https://api.congress.gov/v3/committee/senate/sssb03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 442: Crime and Drugs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Crime and Drugs Subcommittee',
    'Senate',
    'ssju15',
    'https://api.congress.gov/v3/committee/senate/ssju15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 443: Bankruptcy and the Courts Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Bankruptcy and the Courts Subcommittee',
    'Senate',
    'ssju24',
    'https://api.congress.gov/v3/committee/senate/ssju24?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 444: Constitution Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Constitution Subcommittee',
    'Senate',
    'ssju18',
    'https://api.congress.gov/v3/committee/senate/ssju18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 445: Corrections and Rehabilitation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Corrections and Rehabilitation Subcommittee',
    'Senate',
    'ssju14',
    'https://api.congress.gov/v3/committee/senate/ssju14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 446: Privacy, Technology and the Law Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Privacy, Technology and the Law Subcommittee',
    'Senate',
    'ssju23',
    'https://api.congress.gov/v3/committee/senate/ssju23?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 447: Human Rights and the Law Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Human Rights and the Law Subcommittee',
    'Senate',
    'ssju20',
    'https://api.congress.gov/v3/committee/senate/ssju20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 448: Export Expansion and Agricultural Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Export Expansion and Agricultural Development Subcommittee',
    'Senate',
    'sssb01',
    'https://api.congress.gov/v3/committee/senate/sssb01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sssb01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 449: Human Rights and the Law Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Human Rights and the Law Subcommittee',
    'Senate',
    'ssju19',
    'https://api.congress.gov/v3/committee/senate/ssju19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 450: Intellectual Property Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intellectual Property Subcommittee',
    'Senate',
    'ssju17',
    'https://api.congress.gov/v3/committee/senate/ssju17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 451: Youth Violence Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Youth Violence Subcommittee',
    'Senate',
    'ssju07',
    'https://api.congress.gov/v3/committee/senate/ssju07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 452: Crime, Corrections and Victims'' Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Crime, Corrections and Victims'' Rights Subcommittee',
    'Senate',
    'ssju12',
    'https://api.congress.gov/v3/committee/senate/ssju12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 453: Criminal Justice Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Criminal Justice Oversight Subcommittee',
    'Senate',
    'ssju11',
    'https://api.congress.gov/v3/committee/senate/ssju11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 454: Patents, Copyrights and Trademarks Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Patents, Copyrights and Trademarks Subcommittee',
    'Senate',
    'ssju06',
    'https://api.congress.gov/v3/committee/senate/ssju06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 455: Terrorism, Technology, and Government Information Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Terrorism, Technology, and Government Information Subcommittee',
    'Senate',
    'ssju05',
    'https://api.congress.gov/v3/committee/senate/ssju05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 456: Terrorism and Homeland Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Terrorism and Homeland Security Subcommittee',
    'Senate',
    'ssju09',
    'https://api.congress.gov/v3/committee/senate/ssju09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 457: Administrative Oversight and the Courts Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Administrative Oversight and the Courts Subcommittee',
    'Senate',
    'ssju02',
    'https://api.congress.gov/v3/committee/senate/ssju02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 458: Constitution, Civil Rights and Property Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Constitution, Civil Rights and Property Rights Subcommittee',
    'Senate',
    'ssju03',
    'https://api.congress.gov/v3/committee/senate/ssju03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssju03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 459: Substance Abuse and Mental Health Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Substance Abuse and Mental Health Services Subcommittee',
    'Senate',
    'sshr07',
    'https://api.congress.gov/v3/committee/senate/sshr07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 460: Employment, Safety, and Training Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Employment, Safety, and Training Subcommittee',
    'Senate',
    'sshr08',
    'https://api.congress.gov/v3/committee/senate/sshr08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 461: Employment and Productivity Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Employment and Productivity Subcommittee',
    'Senate',
    'sshr04',
    'https://api.congress.gov/v3/committee/senate/sshr04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 462: Disability Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Disability Policy Subcommittee',
    'Senate',
    'sshr02',
    'https://api.congress.gov/v3/committee/senate/sshr02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 463: Aging Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aging Subcommittee',
    'Senate',
    'sshr05',
    'https://api.congress.gov/v3/committee/senate/sshr05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 464: Education, Arts and Humanities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Education, Arts and Humanities Subcommittee',
    'Senate',
    'sshr01',
    'https://api.congress.gov/v3/committee/senate/sshr01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 465: Labor Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Labor Subcommittee',
    'Senate',
    'sshr03',
    'https://api.congress.gov/v3/committee/senate/sshr03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 466: Children and Families Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Children and Families Subcommittee',
    'Senate',
    'sshr06',
    'https://api.congress.gov/v3/committee/senate/sshr06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 467: Bioterrorism and Public Health Preparedness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Bioterrorism and Public Health Preparedness Subcommittee',
    'Senate',
    'sshr10',
    'https://api.congress.gov/v3/committee/senate/sshr10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sshr10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 468: International Security, Proliferation and Federal Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Security, Proliferation and Federal Services Subcommittee',
    'Senate',
    'ssga07',
    'https://api.congress.gov/v3/committee/senate/ssga07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 469: Federal Financial Management, Government Information, Federal Services, and International Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Federal Financial Management, Government Information, Federal Services, and International Security Subcommittee',
    'Senate',
    'ssga09',
    'https://api.congress.gov/v3/committee/senate/ssga09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 470: Disaster Recovery (Ad Hoc) Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Disaster Recovery (Ad Hoc) Subcommittee',
    'Senate',
    'ssga11',
    'https://api.congress.gov/v3/committee/senate/ssga11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 471: Disaster Recovery and Intergovernmental Affairs (Ad Hoc) Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Disaster Recovery and Intergovernmental Affairs (Ad Hoc) Subcommittee',
    'Senate',
    'ssga14',
    'https://api.congress.gov/v3/committee/senate/ssga14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 472: Emergency Management, Intergovernmental Relations, and the District of Columbia Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Emergency Management, Intergovernmental Relations, and the District of Columbia Subcommittee',
    'Senate',
    'ssga17',
    'https://api.congress.gov/v3/committee/senate/ssga17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 473: General Services, Federalism, and the District of Columbia Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'General Services, Federalism, and the District of Columbia Subcommittee',
    'Senate',
    'ssga04',
    'https://api.congress.gov/v3/committee/senate/ssga04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 474: State, Local, and Private Sector Preparedness and Integration (Ad Hoc) Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'State, Local, and Private Sector Preparedness and Integration (Ad Hoc) Subcommittee',
    'Senate',
    'ssga10',
    'https://api.congress.gov/v3/committee/senate/ssga10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 475: Financial and Contracting Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial and Contracting Oversight Subcommittee',
    'Senate',
    'ssga15',
    'https://api.congress.gov/v3/committee/senate/ssga15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 476: Efficiency and Effectiveness of Federal Programs and the Federal Workforce Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Efficiency and Effectiveness of Federal Programs and the Federal Workforce Subcommittee',
    'Senate',
    'ssga16',
    'https://api.congress.gov/v3/committee/senate/ssga16?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 477: Oversight of Government Management, the Federal Workforce, and the District of Columbia Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight of Government Management, the Federal Workforce, and the District of Columbia Subcommittee',
    'Senate',
    'ssga03',
    'https://api.congress.gov/v3/committee/senate/ssga03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 478: Oversight of Government Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight of Government Management Subcommittee',
    'Senate',
    'ssga08',
    'https://api.congress.gov/v3/committee/senate/ssga08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 479: Contracting Oversight (Ad Hoc) Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Contracting Oversight (Ad Hoc) Subcommittee',
    'Senate',
    'ssga13',
    'https://api.congress.gov/v3/committee/senate/ssga13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 480: Federal Spending Oversight and Emergency Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Federal Spending Oversight and Emergency Management Subcommittee',
    'Senate',
    'ssga18',
    'https://api.congress.gov/v3/committee/senate/ssga18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 481: Regulation and Government Information Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regulation and Government Information Subcommittee',
    'Senate',
    'ssga02',
    'https://api.congress.gov/v3/committee/senate/ssga02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 482: Post Office and Civil Service Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Post Office and Civil Service Subcommittee',
    'Senate',
    'ssga05',
    'https://api.congress.gov/v3/committee/senate/ssga05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 483: Financial Management and Accountability Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Management and Accountability Subcommittee',
    'Senate',
    'ssga06',
    'https://api.congress.gov/v3/committee/senate/ssga06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssga06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 484: International Economic Policy, Export and Trade Promotion Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Economic Policy, Export and Trade Promotion Subcommittee',
    'Senate',
    'ssfr03',
    'https://api.congress.gov/v3/committee/senate/ssfr03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 485: Central Asia and South Caucasus Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Central Asia and South Caucasus Subcommittee',
    'Senate',
    'ssfr11',
    'https://api.congress.gov/v3/committee/senate/ssfr11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 486: International Development and Foreign Assistance, Economic Affairs, International Environmental Protection, and Peace Corps Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Development and Foreign Assistance, Economic Affairs, International Environmental Protection, and Peace Corps Subcommittee',
    'Senate',
    'ssfr12',
    'https://api.congress.gov/v3/committee/senate/ssfr12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 487: International Operations and Organizations, Human Rights, Democracy, and Global Women''s Issues Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Operations and Organizations, Human Rights, Democracy, and Global Women''s Issues Subcommittee',
    'Senate',
    'ssfr13',
    'https://api.congress.gov/v3/committee/senate/ssfr13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 488: International Operations and Terrorism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Operations and Terrorism Subcommittee',
    'Senate',
    'ssfr04',
    'https://api.congress.gov/v3/committee/senate/ssfr04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 489: Special Subcommittee on War Powers Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Special Subcommittee on War Powers Subcommittee',
    'Senate',
    'ssfr10',
    'https://api.congress.gov/v3/committee/senate/ssfr10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfr10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 490: Energy and Agricultural Taxation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Agricultural Taxation Subcommittee',
    'Senate',
    'ssfi07',
    'https://api.congress.gov/v3/committee/senate/ssfi07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 491: Taxation and IRS Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Taxation and IRS Oversight Subcommittee',
    'Senate',
    'ssfi06',
    'https://api.congress.gov/v3/committee/senate/ssfi06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 492: Private Retirement Plans and Oversight of the Internal Revenue Service Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Private Retirement Plans and Oversight of the Internal Revenue Service Subcommittee',
    'Senate',
    'ssfi05',
    'https://api.congress.gov/v3/committee/senate/ssfi05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 493: Long-Term Growth and Debt Reduction Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Long-Term Growth and Debt Reduction Subcommittee',
    'Senate',
    'ssfi09',
    'https://api.congress.gov/v3/committee/senate/ssfi09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 494: Oversight of the Internal Revenue Service Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight of the Internal Revenue Service Subcommittee',
    'Senate',
    'ssfi16',
    'https://api.congress.gov/v3/committee/senate/ssfi16?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 495: Economic Growth, Employment and Revenue Sharing Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Growth, Employment and Revenue Sharing Subcommittee',
    'Senate',
    'ssfi20',
    'https://api.congress.gov/v3/committee/senate/ssfi20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 496: Estate and Gift Taxation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Estate and Gift Taxation Subcommittee',
    'Senate',
    'ssfi21',
    'https://api.congress.gov/v3/committee/senate/ssfi21?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 497: Medicare, Long-Term Care and Health Insurance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Medicare, Long-Term Care and Health Insurance Subcommittee',
    'Senate',
    'ssfi08',
    'https://api.congress.gov/v3/committee/senate/ssfi08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 498: Savings, Pensions and Investment Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Savings, Pensions and Investment Policy Subcommittee',
    'Senate',
    'ssfi19',
    'https://api.congress.gov/v3/committee/senate/ssfi19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 499: Long-Term Growth, Debt and Deficit Reduction Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Long-Term Growth, Debt and Deficit Reduction Subcommittee',
    'Senate',
    'ssfi04',
    'https://api.congress.gov/v3/committee/senate/ssfi04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 500: International Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Trade Subcommittee',
    'Senate',
    'ssfi03',
    'https://api.congress.gov/v3/committee/senate/ssfi03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 500/815 committees processed

-- Committee 501: Medicaid and Health Care for Low-Income Families Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Medicaid and Health Care for Low-Income Families Subcommittee',
    'Senate',
    'ssfi01',
    'https://api.congress.gov/v3/committee/senate/ssfi01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssfi01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 502: Fisheries, Wildlife, and Water Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fisheries, Wildlife, and Water Subcommittee',
    'Senate',
    'ssev11',
    'https://api.congress.gov/v3/committee/senate/ssev11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 503: Green Jobs and the New Economy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Green Jobs and the New Economy Subcommittee',
    'Senate',
    'ssev16',
    'https://api.congress.gov/v3/committee/senate/ssev16?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 504: Public Sector Solutions to Global Warming, Oversight, and Children''s Health Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Sector Solutions to Global Warming, Oversight, and Children''s Health Protection Subcommittee',
    'Senate',
    'ssev12',
    'https://api.congress.gov/v3/committee/senate/ssev12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 505: Clean Air and Nuclear Regulation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Clean Air and Nuclear Regulation Subcommittee',
    'Senate',
    'ssev07',
    'https://api.congress.gov/v3/committee/senate/ssev07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 506: Nuclear Regulation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Nuclear Regulation Subcommittee',
    'Senate',
    'ssev05',
    'https://api.congress.gov/v3/committee/senate/ssev05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 507: Clean Water, Fisheries and Wildlife Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Clean Water, Fisheries and Wildlife Subcommittee',
    'Senate',
    'ssev06',
    'https://api.congress.gov/v3/committee/senate/ssev06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 508: Transportation Safety, Infrastructure Security, and Water Quality Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation Safety, Infrastructure Security, and Water Quality Subcommittee',
    'Senate',
    'ssev14',
    'https://api.congress.gov/v3/committee/senate/ssev14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 509: Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight Subcommittee',
    'Senate',
    'ssev18',
    'https://api.congress.gov/v3/committee/senate/ssev18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 510: Children''s Health and Environmental Responsibility Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Children''s Health and Environmental Responsibility Subcommittee',
    'Senate',
    'ssev17',
    'https://api.congress.gov/v3/committee/senate/ssev17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 511: Private Sector and Consumer Solutions to Global Warming and Wildlife Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Private Sector and Consumer Solutions to Global Warming and Wildlife Protection Subcommittee',
    'Senate',
    'ssev13',
    'https://api.congress.gov/v3/committee/senate/ssev13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 512: Superfund, Recycling, and Solid Waste Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Superfund, Recycling, and Solid Waste Management Subcommittee',
    'Senate',
    'ssev04',
    'https://api.congress.gov/v3/committee/senate/ssev04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 513: Environmental Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environmental Protection Subcommittee',
    'Senate',
    'ssev02',
    'https://api.congress.gov/v3/committee/senate/ssev02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 514: Toxic Substances, Research and Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Toxic Substances, Research and Development Subcommittee',
    'Senate',
    'ssev03',
    'https://api.congress.gov/v3/committee/senate/ssev03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 515: Natural Resources Development and Production Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Natural Resources Development and Production Subcommittee',
    'Senate',
    'sseg10',
    'https://api.congress.gov/v3/committee/senate/sseg10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 516: Water Resources, Transportation, Public Buildings, and Economic Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Water Resources, Transportation, Public Buildings, and Economic Development Subcommittee',
    'Senate',
    'ssev01',
    'https://api.congress.gov/v3/committee/senate/ssev01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssev01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 517: Energy Production and Regulation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Production and Regulation Subcommittee',
    'Senate',
    'sseg05',
    'https://api.congress.gov/v3/committee/senate/sseg05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 518: Water and Power Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Water and Power Subcommittee',
    'Senate',
    'sseg08',
    'https://api.congress.gov/v3/committee/senate/sseg08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 519: Public Lands, Reserved Water and Resource Conservation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Lands, Reserved Water and Resource Conservation Subcommittee',
    'Senate',
    'sseg09',
    'https://api.congress.gov/v3/committee/senate/sseg09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 520: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'Senate',
    'sseg06',
    'https://api.congress.gov/v3/committee/senate/sseg06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 521: Renewable Energy, Energy Efficiency, and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Renewable Energy, Energy Efficiency, and Competitiveness Subcommittee',
    'Senate',
    'sseg02',
    'https://api.congress.gov/v3/committee/senate/sseg02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sseg02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 522: Oceans, Atmosphere, Fisheries, and Coast Guard Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oceans, Atmosphere, Fisheries, and Coast Guard Subcommittee',
    'Senate',
    'sscm22',
    'https://api.congress.gov/v3/committee/senate/sscm22?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 523: Consumer Protection, Product Safety, Insurance, and Data Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer Protection, Product Safety, Insurance, and Data Security Subcommittee',
    'Senate',
    'sscm20',
    'https://api.congress.gov/v3/committee/senate/sscm20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 524: Fisheries and Coast Guard Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fisheries and Coast Guard Subcommittee',
    'Senate',
    'sscm15',
    'https://api.congress.gov/v3/committee/senate/sscm15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 525: Surface Transportation and Merchant Marine Infrastructure, Safety and Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Surface Transportation and Merchant Marine Infrastructure, Safety and Security Subcommittee',
    'Senate',
    'sscm25',
    'https://api.congress.gov/v3/committee/senate/sscm25?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm25?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 526: Interstate Commerce, Trade, and Tourism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Interstate Commerce, Trade, and Tourism Subcommittee',
    'Senate',
    'sscm21',
    'https://api.congress.gov/v3/committee/senate/sscm21?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 527: Global Climate Change and Impacts Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Global Climate Change and Impacts Subcommittee',
    'Senate',
    'sscm14',
    'https://api.congress.gov/v3/committee/senate/sscm14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 528: Technology, Innovation, and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology, Innovation, and Competitiveness Subcommittee',
    'Senate',
    'sscm18',
    'https://api.congress.gov/v3/committee/senate/sscm18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 529: Oceans, Fisheries and Coast Guard Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oceans, Fisheries and Coast Guard Subcommittee',
    'Senate',
    'sscm09',
    'https://api.congress.gov/v3/committee/senate/sscm09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 530: Disaster Prevention and Prediction Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Disaster Prevention and Prediction Subcommittee',
    'Senate',
    'sscm13',
    'https://api.congress.gov/v3/committee/senate/sscm13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 531: Consumer Affairs, Product Safety, and Insurance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer Affairs, Product Safety, and Insurance Subcommittee',
    'Senate',
    'sscm12',
    'https://api.congress.gov/v3/committee/senate/sscm12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 532: Manufacturing and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Manufacturing and Competitiveness Subcommittee',
    'Senate',
    'sscm10',
    'https://api.congress.gov/v3/committee/senate/sscm10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 533: Trade, Tourism, and Economic Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Trade, Tourism, and Economic Development Subcommittee',
    'Senate',
    'sscm19',
    'https://api.congress.gov/v3/committee/senate/sscm19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 534: Science and Space Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Science and Space Subcommittee',
    'Senate',
    'sscm17',
    'https://api.congress.gov/v3/committee/senate/sscm17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 535: National Ocean Policy Study Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Ocean Policy Study Subcommittee',
    'Senate',
    'sscm16',
    'https://api.congress.gov/v3/committee/senate/sscm16?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 536: Competition, Foreign Commerce, and Infrastructure Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Competition, Foreign Commerce, and Infrastructure Subcommittee',
    'Senate',
    'sscm11',
    'https://api.congress.gov/v3/committee/senate/sscm11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 537: Tourism, Competitiveness, and Innovation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tourism, Competitiveness, and Innovation Subcommittee',
    'Senate',
    'sscm27',
    'https://api.congress.gov/v3/committee/senate/sscm27?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 538: Science, Oceans, Fisheries, and Weather Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Science, Oceans, Fisheries, and Weather Subcommittee',
    'Senate',
    'sscm30',
    'https://api.congress.gov/v3/committee/senate/sscm30?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm30?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 539: Communications, Technology, Innovation, and the Internet Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Communications, Technology, Innovation, and the Internet Subcommittee',
    'Senate',
    'sscm26',
    'https://api.congress.gov/v3/committee/senate/sscm26?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm26?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 540: Space, Science, and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Space, Science, and Competitiveness Subcommittee',
    'Senate',
    'sscm24',
    'https://api.congress.gov/v3/committee/senate/sscm24?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 541: Science, Technology, and Innovation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Science, Technology, and Innovation Subcommittee',
    'Senate',
    'sscm23',
    'https://api.congress.gov/v3/committee/senate/sscm23?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 542: Surface Transportation and Merchant Marine Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Surface Transportation and Merchant Marine Subcommittee',
    'Senate',
    'sscm08',
    'https://api.congress.gov/v3/committee/senate/sscm08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 543: Aviation Operations, Safety, and Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Aviation Operations, Safety, and Security Subcommittee',
    'Senate',
    'sscm01',
    'https://api.congress.gov/v3/committee/senate/sscm01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 544: Communications Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Communications Subcommittee',
    'Senate',
    'sscm02',
    'https://api.congress.gov/v3/committee/senate/sscm02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 545: Consumer Affairs and Product Safety Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer Affairs and Product Safety Subcommittee',
    'Senate',
    'sscm03',
    'https://api.congress.gov/v3/committee/senate/sscm03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 546: Science, Technology, and Space Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Science, Technology, and Space Subcommittee',
    'Senate',
    'sscm05',
    'https://api.congress.gov/v3/committee/senate/sscm05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 547: Merchant Marine Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Merchant Marine Subcommittee',
    'Senate',
    'sscm06',
    'https://api.congress.gov/v3/committee/senate/sscm06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 548: Foreign Commerce and Tourism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Foreign Commerce and Tourism Subcommittee',
    'Senate',
    'sscm04',
    'https://api.congress.gov/v3/committee/senate/sscm04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 549: National Ocean Policy Study Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Ocean Policy Study Subcommittee',
    'Senate',
    'sscm07',
    'https://api.congress.gov/v3/committee/senate/sscm07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/sscm07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 550: HUD/Moderate Rehabilitation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'HUD/Moderate Rehabilitation Subcommittee',
    'Senate',
    'ssbk06',
    'https://api.congress.gov/v3/committee/senate/ssbk06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 551: Consumer and Regulatory Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer and Regulatory Affairs Subcommittee',
    'Senate',
    'ssbk03',
    'https://api.congress.gov/v3/committee/senate/ssbk03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 552: Acquisition and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Acquisition and Technology Subcommittee',
    'Senate',
    'ssas18',
    'https://api.congress.gov/v3/committee/senate/ssas18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 553: HUD Oversight and Structure Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'HUD Oversight and Structure Subcommittee',
    'Senate',
    'ssbk10',
    'https://api.congress.gov/v3/committee/senate/ssbk10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 554: Financial Services and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Services and Technology Subcommittee',
    'Senate',
    'ssbk11',
    'https://api.congress.gov/v3/committee/senate/ssbk11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 555: Economic Stabilization and Rural Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Stabilization and Rural Development Subcommittee',
    'Senate',
    'ssbk07',
    'https://api.congress.gov/v3/committee/senate/ssbk07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 556: Sea Power and Force Projection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Sea Power and Force Projection Subcommittee',
    'Senate',
    'ssas19',
    'https://api.congress.gov/v3/committee/senate/ssas19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 557: Housing and Urban Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Housing and Urban Affairs Subcommittee',
    'Senate',
    'ssbk02',
    'https://api.congress.gov/v3/committee/senate/ssbk02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssbk02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 558: Readiness, Sustainability and Support Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Readiness, Sustainability and Support Subcommittee',
    'Senate',
    'ssas04',
    'https://api.congress.gov/v3/committee/senate/ssas04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 559: Conventional Forces and Alliance Defense Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Conventional Forces and Alliance Defense Subcommittee',
    'Senate',
    'ssas02',
    'https://api.congress.gov/v3/committee/senate/ssas02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 560: Strategic Forces and Nuclear Deterrence Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Strategic Forces and Nuclear Deterrence Subcommittee',
    'Senate',
    'ssas01',
    'https://api.congress.gov/v3/committee/senate/ssas01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 561: Defense Technology, Acquisition, and Industrial Base Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Technology, Acquisition, and Industrial Base Subcommittee',
    'Senate',
    'ssas07',
    'https://api.congress.gov/v3/committee/senate/ssas07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 562: Projection Forces and Regional Defense Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Projection Forces and Regional Defense Subcommittee',
    'Senate',
    'ssas03',
    'https://api.congress.gov/v3/committee/senate/ssas03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 563: Nuclear Deterrence, Arms Control, and Defense Intelligence Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Nuclear Deterrence, Arms Control, and Defense Intelligence Subcommittee',
    'Senate',
    'ssas10',
    'https://api.congress.gov/v3/committee/senate/ssas10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 564: Regional Defense and Contingency Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regional Defense and Contingency Forces Subcommittee',
    'Senate',
    'ssas12',
    'https://api.congress.gov/v3/committee/senate/ssas12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 565: Coalition Defense and Reinforcing Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Coalition Defense and Reinforcing Forces Subcommittee',
    'Senate',
    'ssas11',
    'https://api.congress.gov/v3/committee/senate/ssas11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 566: Force Requirements and Personnel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Force Requirements and Personnel Subcommittee',
    'Senate',
    'ssas09',
    'https://api.congress.gov/v3/committee/senate/ssas09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 567: Military Readiness and Defense Infrastructure Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Readiness and Defense Infrastructure Subcommittee',
    'Senate',
    'ssas08',
    'https://api.congress.gov/v3/committee/senate/ssas08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 568: Defense Industry and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Industry and Technology Subcommittee',
    'Senate',
    'ssas06',
    'https://api.congress.gov/v3/committee/senate/ssas06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 569: Manpower and Personnel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Manpower and Personnel Subcommittee',
    'Senate',
    'ssas05',
    'https://api.congress.gov/v3/committee/senate/ssas05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssas05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 570: Energy and Water Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Water Development Subcommittee',
    'Senate',
    'ssap10',
    'https://api.congress.gov/v3/committee/senate/ssap10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 571: Transportation, Treasury and General Government Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation, Treasury and General Government Subcommittee',
    'Senate',
    'ssap15',
    'https://api.congress.gov/v3/committee/senate/ssap15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 572: Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation Subcommittee',
    'Senate',
    'ssap12',
    'https://api.congress.gov/v3/committee/senate/ssap12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 573: Commerce, Justice, State, and the Judiciary Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Justice, State, and the Judiciary Subcommittee',
    'Senate',
    'ssap11',
    'https://api.congress.gov/v3/committee/senate/ssap11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 574: Military Construction Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Construction Subcommittee',
    'Senate',
    'ssap09',
    'https://api.congress.gov/v3/committee/senate/ssap09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 575: VA, HUD, and Independent Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'VA, HUD, and Independent Agencies Subcommittee',
    'Senate',
    'ssap05',
    'https://api.congress.gov/v3/committee/senate/ssap05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 576: Foreign Operations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Foreign Operations Subcommittee',
    'Senate',
    'ssap04',
    'https://api.congress.gov/v3/committee/senate/ssap04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 577: Nutrition and Food Assistance, Sustainable and Organic Agriculture, and General Legislation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Nutrition and Food Assistance, Sustainable and Organic Agriculture, and General Legislation Subcommittee',
    'Senate',
    'ssaf10',
    'https://api.congress.gov/v3/committee/senate/ssaf10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 578: Rural Revitalization, Conservation, Forestry, and Credit Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rural Revitalization, Conservation, Forestry, and Credit Subcommittee',
    'Senate',
    'ssaf12',
    'https://api.congress.gov/v3/committee/senate/ssaf12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 579: Production, Income Protection and Price Support Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Production, Income Protection and Price Support Subcommittee',
    'Senate',
    'ssaf11',
    'https://api.congress.gov/v3/committee/senate/ssaf11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 580: District of Columbia Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'District of Columbia Subcommittee',
    'Senate',
    'ssap03',
    'https://api.congress.gov/v3/committee/senate/ssap03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 581: Interior Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Interior Subcommittee',
    'Senate',
    'ssap06',
    'https://api.congress.gov/v3/committee/senate/ssap06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 582: Transportation, Treasury, the Judiciary, and Housing and Urban Development, and Related Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation, Treasury, the Judiciary, and Housing and Urban Development, and Related Agencies Subcommittee',
    'Senate',
    'ssap21',
    'https://api.congress.gov/v3/committee/senate/ssap21?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 583: Treasury and General Government Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Treasury and General Government Subcommittee',
    'Senate',
    'ssap13',
    'https://api.congress.gov/v3/committee/senate/ssap13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssap13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 584: Agricultural Credit Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Agricultural Credit Subcommittee',
    'Senate',
    'ssaf03',
    'https://api.congress.gov/v3/committee/senate/ssaf03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 585: Forestry, Conservation, and Rural Revitalization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Forestry, Conservation, and Rural Revitalization Subcommittee',
    'Senate',
    'ssaf05',
    'https://api.congress.gov/v3/committee/senate/ssaf05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 586: Research, Nutrition, and General Legislation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Research, Nutrition, and General Legislation Subcommittee',
    'Senate',
    'ssaf06',
    'https://api.congress.gov/v3/committee/senate/ssaf06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 587: Domestic and Foreign Marketing, Inspection, and Plant and Animal Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic and Foreign Marketing, Inspection, and Plant and Animal Health Subcommittee',
    'Senate',
    'ssaf08',
    'https://api.congress.gov/v3/committee/senate/ssaf08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 588: Energy, Science and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy, Science and Technology Subcommittee',
    'Senate',
    'ssaf09',
    'https://api.congress.gov/v3/committee/senate/ssaf09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 589: Agricultural Research, Conservation, Forestry and General Legislation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Agricultural Research, Conservation, Forestry and General Legislation Subcommittee',
    'Senate',
    'ssaf04',
    'https://api.congress.gov/v3/committee/senate/ssaf04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 590: Conservation and Forestry Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Conservation and Forestry Subcommittee',
    'Senate',
    'ssaf07',
    'https://api.congress.gov/v3/committee/senate/ssaf07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 591: Production and Price Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Production and Price Competitiveness Subcommittee',
    'Senate',
    'ssaf01',
    'https://api.congress.gov/v3/committee/senate/ssaf01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 592: Marketing, Inspection, and Product Promotion Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Marketing, Inspection, and Product Promotion Subcommittee',
    'Senate',
    'ssaf02',
    'https://api.congress.gov/v3/committee/senate/ssaf02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/ssaf02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 593: Analysis and Production Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Analysis and Production Subcommittee',
    'Senate',
    'slin03',
    'https://api.congress.gov/v3/committee/senate/slin03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/slin03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 594: Budget Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Budget Subcommittee',
    'Senate',
    'slin02',
    'https://api.congress.gov/v3/committee/senate/slin02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/slin02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 595: Oversight of the Terrorist Surveillance Program Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight of the Terrorist Surveillance Program Subcommittee',
    'Senate',
    'slin01',
    'https://api.congress.gov/v3/committee/senate/slin01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/slin01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 596: Collection and Foreign Operations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Collection and Foreign Operations Subcommittee',
    'Senate',
    'slin06',
    'https://api.congress.gov/v3/committee/senate/slin06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/senate/slin06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 597: International Economic Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Economic Policy Subcommittee',
    'Joint',
    'jsec01',
    'https://api.congress.gov/v3/committee/joint/jsec01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 598: Education and Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Education and Health Subcommittee',
    'Joint',
    'jsec08',
    'https://api.congress.gov/v3/committee/joint/jsec08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 599: Economic Growth, Trade, and Taxes Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Growth, Trade, and Taxes Subcommittee',
    'Joint',
    'jsec05',
    'https://api.congress.gov/v3/committee/joint/jsec05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 600: Fiscal and Monetary Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fiscal and Monetary Policy Subcommittee',
    'Joint',
    'jsec06',
    'https://api.congress.gov/v3/committee/joint/jsec06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 600/815 committees processed

-- Committee 601: Economic Resources and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Resources and Competitiveness Subcommittee',
    'Joint',
    'jsec07',
    'https://api.congress.gov/v3/committee/joint/jsec07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 602: Technology and National Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology and National Security Subcommittee',
    'Joint',
    'jsec04',
    'https://api.congress.gov/v3/committee/joint/jsec04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 603: Investment, Jobs, and Prices Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investment, Jobs, and Prices Subcommittee',
    'Joint',
    'jsec02',
    'https://api.congress.gov/v3/committee/joint/jsec02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/joint/jsec02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 604: Compensation, Pension and Insurance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Compensation, Pension and Insurance Subcommittee',
    'House',
    'hsvr01',
    'https://api.congress.gov/v3/committee/house/hsvr01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 605: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsvr05',
    'https://api.congress.gov/v3/committee/house/hsvr05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 606: Housing and Memorial Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Housing and Memorial Affairs Subcommittee',
    'House',
    'hsvr04',
    'https://api.congress.gov/v3/committee/house/hsvr04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 607: Education, Training, Employment and Housing Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Education, Training, Employment and Housing Subcommittee',
    'House',
    'hsvr07',
    'https://api.congress.gov/v3/committee/house/hsvr07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 608: Education, Training and Employment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Education, Training and Employment Subcommittee',
    'House',
    'hsvr02',
    'https://api.congress.gov/v3/committee/house/hsvr02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 609: Benefits Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Benefits Subcommittee',
    'House',
    'hsvr06',
    'https://api.congress.gov/v3/committee/house/hsvr06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsvr06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 610: Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology Subcommittee',
    'House',
    'hssy17',
    'https://api.congress.gov/v3/committee/house/hssy17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 611: Research Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Research Subcommittee',
    'House',
    'hssy14',
    'https://api.congress.gov/v3/committee/house/hssy14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 612: Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology Subcommittee',
    'House',
    'hssy19',
    'https://api.congress.gov/v3/committee/house/hssy19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 613: Transportation, Aviation and Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation, Aviation and Materials Subcommittee',
    'House',
    'hssy07',
    'https://api.congress.gov/v3/committee/house/hssy07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 614: Technology and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology and Competitiveness Subcommittee',
    'House',
    'hssy13',
    'https://api.congress.gov/v3/committee/house/hssy13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 615: International Scientific Cooperation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Scientific Cooperation Subcommittee',
    'House',
    'hssy11',
    'https://api.congress.gov/v3/committee/house/hssy11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 616: Task Force on Science Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Task Force on Science Policy Subcommittee',
    'House',
    'hssy08',
    'https://api.congress.gov/v3/committee/house/hssy08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 617: Energy Research and Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Research and Development Subcommittee',
    'House',
    'hssy06',
    'https://api.congress.gov/v3/committee/house/hssy06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 618: Energy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Subcommittee',
    'House',
    'hssy10',
    'https://api.congress.gov/v3/committee/house/hssy10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 619: Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment Subcommittee',
    'House',
    'hssy04',
    'https://api.congress.gov/v3/committee/house/hssy04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 620: International Scientific Cooperation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Scientific Cooperation Subcommittee',
    'House',
    'hssy01',
    'https://api.congress.gov/v3/committee/house/hssy01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 621: Space Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Space Subcommittee',
    'House',
    'hssy02',
    'https://api.congress.gov/v3/committee/house/hssy02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 622: Science, Research and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Science, Research and Technology Subcommittee',
    'House',
    'hssy03',
    'https://api.congress.gov/v3/committee/house/hssy03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 623: Investigations and Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigations and Oversight Subcommittee',
    'House',
    'hssy05',
    'https://api.congress.gov/v3/committee/house/hssy05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssy05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 624: Underserved, Agricultural, and Rural Business Development
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Underserved, Agricultural, and Rural Business Development',
    'House',
    'hssm25',
    'https://api.congress.gov/v3/committee/house/hssm25?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm25?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 625: Empowerment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Empowerment Subcommittee',
    'House',
    'hssm20',
    'https://api.congress.gov/v3/committee/house/hssm20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 626: Finance and Tax
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Finance and Tax',
    'House',
    'hssm19',
    'https://api.congress.gov/v3/committee/house/hssm19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 627: Tax and Finance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tax and Finance Subcommittee',
    'House',
    'hssm18',
    'https://api.congress.gov/v3/committee/house/hssm18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 628: Procurement, Exports and Business Opportunities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Procurement, Exports and Business Opportunities Subcommittee',
    'House',
    'hssm16',
    'https://api.congress.gov/v3/committee/house/hssm16?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm16?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 629: Minority Enterprise, Finance and Urban Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Minority Enterprise, Finance and Urban Development Subcommittee',
    'House',
    'hssm13',
    'https://api.congress.gov/v3/committee/house/hssm13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 630: Regulations and Healthcare Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regulations and Healthcare Subcommittee',
    'House',
    'hssm17',
    'https://api.congress.gov/v3/committee/house/hssm17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 631: Innovation, Entrepreneurship, and Workforce Development
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Innovation, Entrepreneurship, and Workforce Development',
    'House',
    'hssm26',
    'https://api.congress.gov/v3/committee/house/hssm26?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm26?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 632: Government Programs and Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Government Programs and Oversight Subcommittee',
    'House',
    'hssm15',
    'https://api.congress.gov/v3/committee/house/hssm15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 633: Rural Enterprises, Exports and Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rural Enterprises, Exports and Environment Subcommittee',
    'House',
    'hssm14',
    'https://api.congress.gov/v3/committee/house/hssm14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 634: Exports, Tourism and Special Problems Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Exports, Tourism and Special Problems Subcommittee',
    'House',
    'hssm06',
    'https://api.congress.gov/v3/committee/house/hssm06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 635: Energy and Agriculture Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Agriculture Subcommittee',
    'House',
    'hssm04',
    'https://api.congress.gov/v3/committee/house/hssm04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 636: Regulation and Business Opportunities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regulation and Business Opportunities Subcommittee',
    'House',
    'hssm03',
    'https://api.congress.gov/v3/committee/house/hssm03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 637: SBA, and the General Economy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'SBA, and the General Economy Subcommittee',
    'House',
    'hssm02',
    'https://api.congress.gov/v3/committee/house/hssm02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 638: Technology and the House Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology and the House Subcommittee',
    'House',
    'hsru01',
    'https://api.congress.gov/v3/committee/house/hsru01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsru01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 639: Procurement, Innovation and Minority Enterprise Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Procurement, Innovation and Minority Enterprise Development Subcommittee',
    'House',
    'hssm01',
    'https://api.congress.gov/v3/committee/house/hssm01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 640: Tax, Access to Equity Capital and Business Opportunities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Tax, Access to Equity Capital and Business Opportunities Subcommittee',
    'House',
    'hssm05',
    'https://api.congress.gov/v3/committee/house/hssm05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 641: Procurement, Taxation and Tourism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Procurement, Taxation and Tourism Subcommittee',
    'House',
    'hssm09',
    'https://api.congress.gov/v3/committee/house/hssm09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 642: Antitrust, Impact of Deregulation and Ecology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Antitrust, Impact of Deregulation and Ecology Subcommittee',
    'House',
    'hssm12',
    'https://api.congress.gov/v3/committee/house/hssm12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 643: Regulation, Business Opportunities, and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regulation, Business Opportunities, and Technology Subcommittee',
    'House',
    'hssm11',
    'https://api.congress.gov/v3/committee/house/hssm11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 644: Environment and Employment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment and Employment Subcommittee',
    'House',
    'hssm10',
    'https://api.congress.gov/v3/committee/house/hssm10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 645: Exports, Tax Policy, and Special Problems Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Exports, Tax Policy, and Special Problems Subcommittee',
    'House',
    'hssm08',
    'https://api.congress.gov/v3/committee/house/hssm08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 646: SBA Legislation and the General Economy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'SBA Legislation and the General Economy Subcommittee',
    'House',
    'hssm07',
    'https://api.congress.gov/v3/committee/house/hssm07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hssm07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 647: Public-Private Partnerships Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public-Private Partnerships Subcommittee',
    'House',
    'hspw33',
    'https://api.congress.gov/v3/committee/house/hspw33?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw33?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 648: Public Buildings and Grounds Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Public Buildings and Grounds Subcommittee',
    'House',
    'hspw04',
    'https://api.congress.gov/v3/committee/house/hspw04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 649: Surface Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Surface Transportation Subcommittee',
    'House',
    'hspw03',
    'https://api.congress.gov/v3/committee/house/hspw03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 650: Economic Development, Public Buildings, Hazardous Materials and Pipeline Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Development, Public Buildings, Hazardous Materials and Pipeline Transportation Subcommittee',
    'House',
    'hspw08',
    'https://api.congress.gov/v3/committee/house/hspw08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 651: Railroads Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Railroads Subcommittee',
    'House',
    'hspw09',
    'https://api.congress.gov/v3/committee/house/hspw09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 652: Economic Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Development Subcommittee',
    'House',
    'hspw06',
    'https://api.congress.gov/v3/committee/house/hspw06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 653: Ground Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Ground Transportation Subcommittee',
    'House',
    'hspw10',
    'https://api.congress.gov/v3/committee/house/hspw10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 654: Oversight, Investigations and Emergency Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight, Investigations and Emergency Management Subcommittee',
    'House',
    'hspw11',
    'https://api.congress.gov/v3/committee/house/hspw11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 655: Investigations and Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigations and Oversight Subcommittee',
    'House',
    'hspw01',
    'https://api.congress.gov/v3/committee/house/hspw01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspw01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 656: Census, Statistics and Postal Personnel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Census, Statistics and Postal Personnel Subcommittee',
    'House',
    'hspo09',
    'https://api.congress.gov/v3/committee/house/hspo09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 657: Postal Personnel and Modernization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Postal Personnel and Modernization Subcommittee',
    'House',
    'hspo05',
    'https://api.congress.gov/v3/committee/house/hspo05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 658: Postal Operations and Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Postal Operations and Services Subcommittee',
    'House',
    'hspo06',
    'https://api.congress.gov/v3/committee/house/hspo06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 659: Census and Population Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Census and Population Subcommittee',
    'House',
    'hspo01',
    'https://api.congress.gov/v3/committee/house/hspo01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 660: Compensation and Employee Benefits Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Compensation and Employee Benefits Subcommittee',
    'House',
    'hspo02',
    'https://api.congress.gov/v3/committee/house/hspo02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 661: Civil Service Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Service Subcommittee',
    'House',
    'hspo03',
    'https://api.congress.gov/v3/committee/house/hspo03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 662: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hspo07',
    'https://api.congress.gov/v3/committee/house/hspo07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 663: Human Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Human Resources Subcommittee',
    'House',
    'hspo04',
    'https://api.congress.gov/v3/committee/house/hspo04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hspo04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 664: Merchant Marine Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Merchant Marine Subcommittee',
    'House',
    'hsmm06',
    'https://api.congress.gov/v3/committee/house/hsmm06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 665: Panama Canal and Outer Continental Shelf Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Panama Canal and Outer Continental Shelf Subcommittee',
    'House',
    'hsmm05',
    'https://api.congress.gov/v3/committee/house/hsmm05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 666: Oceanography Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oceanography Subcommittee',
    'House',
    'hsmm04',
    'https://api.congress.gov/v3/committee/house/hsmm04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 667: Coast Guard and Navigation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Coast Guard and Navigation Subcommittee',
    'House',
    'hsmm01',
    'https://api.congress.gov/v3/committee/house/hsmm01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 668: Fisheries and Wildlife Conservation and the Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fisheries and Wildlife Conservation and the Environment Subcommittee',
    'House',
    'hsmm02',
    'https://api.congress.gov/v3/committee/house/hsmm02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 669: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsmm07',
    'https://api.congress.gov/v3/committee/house/hsmm07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 670: Fisheries Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fisheries Management Subcommittee',
    'House',
    'hsmm23',
    'https://api.congress.gov/v3/committee/house/hsmm23?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 671: Environment and Natural Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment and Natural Resources Subcommittee',
    'House',
    'hsmm22',
    'https://api.congress.gov/v3/committee/house/hsmm22?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 672: Oceanography, Gulf of Mexico and the Outer Continental Shelf Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oceanography, Gulf of Mexico and the Outer Continental Shelf Subcommittee',
    'House',
    'hsmm08',
    'https://api.congress.gov/v3/committee/house/hsmm08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsmm08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 673: Commercial and Administrative Law Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commercial and Administrative Law Subcommittee',
    'House',
    'hsju09',
    'https://api.congress.gov/v3/committee/house/hsju09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsju09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 674: Over-Criminalization Task Force Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Over-Criminalization Task Force Subcommittee',
    'House',
    'hsju12',
    'https://api.congress.gov/v3/committee/house/hsju12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsju12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 675: Crime Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Crime Subcommittee',
    'House',
    'hsju06',
    'https://api.congress.gov/v3/committee/house/hsju06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsju06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 676: Criminal Justice Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Criminal Justice Subcommittee',
    'House',
    'hsju07',
    'https://api.congress.gov/v3/committee/house/hsju07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsju07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 677: Civil and Constitutional Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil and Constitutional Rights Subcommittee',
    'House',
    'hsju04',
    'https://api.congress.gov/v3/committee/house/hsju04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsju04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 678: Administrative Law and Governmental Relations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Administrative Law and Governmental Relations Subcommittee',
    'House',
    'hsju02',
    'https://api.congress.gov/v3/committee/house/hsju02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsju02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 679: Forests and Forest Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Forests and Forest Health Subcommittee',
    'House',
    'hsii20',
    'https://api.congress.gov/v3/committee/house/hsii20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 680: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsii11',
    'https://api.congress.gov/v3/committee/house/hsii11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 681: Native American and Insular Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Native American and Insular Affairs Subcommittee',
    'House',
    'hsii14',
    'https://api.congress.gov/v3/committee/house/hsii14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 682: Fisheries, Wildlife, Oceans, and Insular Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fisheries, Wildlife, Oceans, and Insular Affairs Subcommittee',
    'House',
    'hsii22',
    'https://api.congress.gov/v3/committee/house/hsii22?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 683: Insular and International Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Insular and International Affairs Subcommittee',
    'House',
    'hsii09',
    'https://api.congress.gov/v3/committee/house/hsii09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 684: Water, Power and Offshore Energy Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Water, Power and Offshore Energy Resources Subcommittee',
    'House',
    'hsii05',
    'https://api.congress.gov/v3/committee/house/hsii05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 685: General Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'General Oversight and Investigations Subcommittee',
    'House',
    'hsii03',
    'https://api.congress.gov/v3/committee/house/hsii03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 686: Mining and Natural Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Mining and Natural Resources Subcommittee',
    'House',
    'hsii02',
    'https://api.congress.gov/v3/committee/house/hsii02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 687: National Parks and Public Lands Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Parks and Public Lands Subcommittee',
    'House',
    'hsii01',
    'https://api.congress.gov/v3/committee/house/hsii01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 688: National Parks and Recreation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'National Parks and Recreation Subcommittee',
    'House',
    'hsii08',
    'https://api.congress.gov/v3/committee/house/hsii08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 689: Native American Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Native American Affairs Subcommittee',
    'House',
    'hsii04',
    'https://api.congress.gov/v3/committee/house/hsii04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 690: Insular and International Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Insular and International Affairs Subcommittee',
    'House',
    'hsii07',
    'https://api.congress.gov/v3/committee/house/hsii07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsii07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 691: Telecommunications, Trade, and Consumer Protection Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Telecommunications, Trade, and Consumer Protection Subcommittee',
    'House',
    'hsif12',
    'https://api.congress.gov/v3/committee/house/hsif12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 692: Commerce, Trade, and Hazardous Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Trade, and Hazardous Materials Subcommittee',
    'House',
    'hsif11',
    'https://api.congress.gov/v3/committee/house/hsif11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 693: Finance and Hazardous Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Finance and Hazardous Materials Subcommittee',
    'House',
    'hsif13',
    'https://api.congress.gov/v3/committee/house/hsif13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 694: Environment and Hazardous Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment and Hazardous Materials Subcommittee',
    'House',
    'hsif15',
    'https://api.congress.gov/v3/committee/house/hsif15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 695: Transportation and Hazardous Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation and Hazardous Materials Subcommittee',
    'House',
    'hsif10',
    'https://api.congress.gov/v3/committee/house/hsif10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 696: Commerce, Consumer Protection, and Competitiveness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Consumer Protection, and Competitiveness Subcommittee',
    'House',
    'hsif06',
    'https://api.congress.gov/v3/committee/house/hsif06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 697: Health and Environment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health and Environment Subcommittee',
    'House',
    'hsif04',
    'https://api.congress.gov/v3/committee/house/hsif04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 698: Transportation, Tourism, and Hazardous Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation, Tourism, and Hazardous Materials Subcommittee',
    'House',
    'hsif07',
    'https://api.congress.gov/v3/committee/house/hsif07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 699: Telecommunications and Finance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Telecommunications and Finance Subcommittee',
    'House',
    'hsif01',
    'https://api.congress.gov/v3/committee/house/hsif01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsif01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 700: Rules Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Rules Subcommittee',
    'House',
    'hshm02',
    'https://api.congress.gov/v3/committee/house/hshm02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hshm02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 700/815 committees processed

-- Committee 701: Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Investigations Subcommittee',
    'House',
    'hshm10',
    'https://api.congress.gov/v3/committee/house/hshm10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hshm10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 702: Prevention of Nuclear and Biological Attack Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Prevention of Nuclear and Biological Attack Subcommittee',
    'House',
    'hshm06',
    'https://api.congress.gov/v3/committee/house/hshm06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hshm06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 703: Cybersecurity, Science, and Research and Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cybersecurity, Science, and Research and Development Subcommittee',
    'House',
    'hshm04',
    'https://api.congress.gov/v3/committee/house/hshm04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hshm04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 704: Emergency Preparedness and Response Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Emergency Preparedness and Response Subcommittee',
    'House',
    'hshm03',
    'https://api.congress.gov/v3/committee/house/hshm03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hshm03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 705: Infrastructure and Border Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Infrastructure and Border Security Subcommittee',
    'House',
    'hshm01',
    'https://api.congress.gov/v3/committee/house/hshm01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hshm01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 706: Administrative Oversight Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Administrative Oversight Subcommittee',
    'House',
    'hsha22',
    'https://api.congress.gov/v3/committee/house/hsha22?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 707: Libraries and Memorials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Libraries and Memorials Subcommittee',
    'House',
    'hsha09',
    'https://api.congress.gov/v3/committee/house/hsha09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 708: Office Systems Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Office Systems Subcommittee',
    'House',
    'hsha07',
    'https://api.congress.gov/v3/committee/house/hsha07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 709: Personnel and Police Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Personnel and Police Subcommittee',
    'House',
    'hsha05',
    'https://api.congress.gov/v3/committee/house/hsha05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 710: Capitol Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Capitol Security Subcommittee',
    'House',
    'hsha04',
    'https://api.congress.gov/v3/committee/house/hsha04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 711: Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Services Subcommittee',
    'House',
    'hsha03',
    'https://api.congress.gov/v3/committee/house/hsha03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 712: Procurement and Printing Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Procurement and Printing Subcommittee',
    'House',
    'hsha02',
    'https://api.congress.gov/v3/committee/house/hsha02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 713: Technology, Information Policy, Intergovernmental Relations and the Census Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology, Information Policy, Intergovernmental Relations and the Census Subcommittee',
    'House',
    'hsgo20',
    'https://api.congress.gov/v3/committee/house/hsgo20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 714: Civil Service and Agency Organization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Service and Agency Organization Subcommittee',
    'House',
    'hsgo18',
    'https://api.congress.gov/v3/committee/house/hsgo18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 715: Government Efficiency and Financial Management Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Government Efficiency and Financial Management Subcommittee',
    'House',
    'hsgo19',
    'https://api.congress.gov/v3/committee/house/hsgo19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 716: Information Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Information Technology Subcommittee',
    'House',
    'hsgo25',
    'https://api.congress.gov/v3/committee/house/hsgo25?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo25?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 717: Accounts Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Accounts Subcommittee',
    'House',
    'hsha01',
    'https://api.congress.gov/v3/committee/house/hsha01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsha01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 718: Technology, Information Policy, Intergovernmental Relations and Procurement Reform Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology, Information Policy, Intergovernmental Relations and Procurement Reform Subcommittee',
    'House',
    'hsgo30',
    'https://api.congress.gov/v3/committee/house/hsgo30?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo30?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 719: Domestic Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic Policy Subcommittee',
    'House',
    'hsgo26',
    'https://api.congress.gov/v3/committee/house/hsgo26?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo26?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 720: Human Rights and Wellness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Human Rights and Wellness Subcommittee',
    'House',
    'hsgo21',
    'https://api.congress.gov/v3/committee/house/hsgo21?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 721: Transportation and Public Assets Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation and Public Assets Subcommittee',
    'House',
    'hsgo29',
    'https://api.congress.gov/v3/committee/house/hsgo29?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo29?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 722: Information Policy, Census, and National Archives Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Information Policy, Census, and National Archives Subcommittee',
    'House',
    'hsgo23',
    'https://api.congress.gov/v3/committee/house/hsgo23?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 723: Energy and Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy and Resources Subcommittee',
    'House',
    'hsgo22',
    'https://api.congress.gov/v3/committee/house/hsgo22?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 724: Civil Rights and Civil Liberties Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Rights and Civil Liberties Subcommittee',
    'House',
    'hsgo02',
    'https://api.congress.gov/v3/committee/house/hsgo02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 725: Energy Policy, Natural Resources and Regulatory Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Energy Policy, Natural Resources and Regulatory Affairs Subcommittee',
    'House',
    'hsgo01',
    'https://api.congress.gov/v3/committee/house/hsgo01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 726: Government Activities and Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Government Activities and Transportation Subcommittee',
    'House',
    'hsgo03',
    'https://api.congress.gov/v3/committee/house/hsgo03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 727: Intergovernmental Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intergovernmental Affairs Subcommittee',
    'House',
    'hsgo04',
    'https://api.congress.gov/v3/committee/house/hsgo04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 728: Regulatory Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Regulatory Affairs Subcommittee',
    'House',
    'hsgo08',
    'https://api.congress.gov/v3/committee/house/hsgo08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 729: Civil Service and Agency Organization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Service and Agency Organization Subcommittee',
    'House',
    'hsgo09',
    'https://api.congress.gov/v3/committee/house/hsgo09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 730: Postal Service Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Postal Service Subcommittee',
    'House',
    'hsgo11',
    'https://api.congress.gov/v3/committee/house/hsgo11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 731: Census Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Census Subcommittee',
    'House',
    'hsgo13',
    'https://api.congress.gov/v3/committee/house/hsgo13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 732: Criminal Justice, Drug Policy and Human Resources Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Criminal Justice, Drug Policy and Human Resources Subcommittee',
    'House',
    'hsgo14',
    'https://api.congress.gov/v3/committee/house/hsgo14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 733: Technology and Procurement Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Technology and Procurement Policy Subcommittee',
    'House',
    'hsgo15',
    'https://api.congress.gov/v3/committee/house/hsgo15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 734: District of Columbia Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'District of Columbia Subcommittee',
    'House',
    'hsgo10',
    'https://api.congress.gov/v3/committee/house/hsgo10?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo10?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 735: Employment, Housing, and Aviation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Employment, Housing, and Aviation Subcommittee',
    'House',
    'hsgo07',
    'https://api.congress.gov/v3/committee/house/hsgo07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsgo07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 736: International Terrorism, Nonproliferation and Human Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Terrorism, Nonproliferation and Human Rights Subcommittee',
    'House',
    'hsfa15',
    'https://api.congress.gov/v3/committee/house/hsfa15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 737: Terrorism,  Nonproliferation, and Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Terrorism,  Nonproliferation, and Trade Subcommittee',
    'House',
    'hsfa18',
    'https://api.congress.gov/v3/committee/house/hsfa18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 738: International Operations and Human Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Operations and Human Rights Subcommittee',
    'House',
    'hsfa12',
    'https://api.congress.gov/v3/committee/house/hsfa12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 739: International Security, International Organizations, and Human Rights Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Security, International Organizations, and Human Rights Subcommittee',
    'House',
    'hsfa11',
    'https://api.congress.gov/v3/committee/house/hsfa11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 740: Europe and the Middle East Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Europe and the Middle East Subcommittee',
    'House',
    'hsfa03',
    'https://api.congress.gov/v3/committee/house/hsfa03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 741: International Economic Policy and Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Economic Policy and Trade Subcommittee',
    'House',
    'hsfa04',
    'https://api.congress.gov/v3/committee/house/hsfa04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 742: Africa Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Africa Subcommittee',
    'House',
    'hsfa08',
    'https://api.congress.gov/v3/committee/house/hsfa08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 743: Arms Control, International Security and Science Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Arms Control, International Security and Science Subcommittee',
    'House',
    'hsfa01',
    'https://api.congress.gov/v3/committee/house/hsfa01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 744: International Operations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Operations Subcommittee',
    'House',
    'hsfa02',
    'https://api.congress.gov/v3/committee/house/hsfa02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsfa02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 745: Employment Opportunities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Employment Opportunities Subcommittee',
    'House',
    'hsed06',
    'https://api.congress.gov/v3/committee/house/hsed06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 746: Postsecondary Education, Training and Life-Long Learning Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Postsecondary Education, Training and Life-Long Learning Subcommittee',
    'House',
    'hsed08',
    'https://api.congress.gov/v3/committee/house/hsed08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 747: Health and Safety Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health and Safety Subcommittee',
    'House',
    'hsed05',
    'https://api.congress.gov/v3/committee/house/hsed05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 748: Civil Rights and Human Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Civil Rights and Human Services Subcommittee',
    'House',
    'hsed07',
    'https://api.congress.gov/v3/committee/house/hsed07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 749: Early Childhood, Youth and Families Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Early Childhood, Youth and Families Subcommittee',
    'House',
    'hsed11',
    'https://api.congress.gov/v3/committee/house/hsed11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 750: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsed12',
    'https://api.congress.gov/v3/committee/house/hsed12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 751: Labor Standards Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Labor Standards Subcommittee',
    'House',
    'hsed03',
    'https://api.congress.gov/v3/committee/house/hsed03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 752: Healthy Families and Communities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Healthy Families and Communities Subcommittee',
    'House',
    'hsed04',
    'https://api.congress.gov/v3/committee/house/hsed04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 753: Elementary, Secondary, and Vocational Education Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Elementary, Secondary, and Vocational Education Subcommittee',
    'House',
    'hsed01',
    'https://api.congress.gov/v3/committee/house/hsed01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsed01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 754: Fiscal Affairs and Health Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Fiscal Affairs and Health Subcommittee',
    'House',
    'hsdt01',
    'https://api.congress.gov/v3/committee/house/hsdt01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsdt01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 755: Domestic Monetary Policy, Technology, and Economic Growth Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic Monetary Policy, Technology, and Economic Growth Subcommittee',
    'House',
    'hsba18',
    'https://api.congress.gov/v3/committee/house/hsba18?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba18?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 756: Domestic Monetary Policy and Technology Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic Monetary Policy and Technology Subcommittee',
    'House',
    'hsba19',
    'https://api.congress.gov/v3/committee/house/hsba19?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba19?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 757: Government Operations and Metropolitan Affairs Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Government Operations and Metropolitan Affairs Subcommittee',
    'House',
    'hsdt02',
    'https://api.congress.gov/v3/committee/house/hsdt02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsdt02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 758: Judiciary and Education Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Judiciary and Education Subcommittee',
    'House',
    'hsdt03',
    'https://api.congress.gov/v3/committee/house/hsdt03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsdt03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 759: International Monetary Policy and Trade Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Monetary Policy and Trade Subcommittee',
    'House',
    'hsba17',
    'https://api.congress.gov/v3/committee/house/hsba17?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba17?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 760: Consumer Protection and Financial Institutions Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer Protection and Financial Institutions Subcommittee',
    'House',
    'hsba15',
    'https://api.congress.gov/v3/committee/house/hsba15?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba15?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 761: Domestic Monetary Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic Monetary Policy Subcommittee',
    'House',
    'hsba03',
    'https://api.congress.gov/v3/committee/house/hsba03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 762: Diversity and Inclusion Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Diversity and Inclusion Subcommittee',
    'House',
    'hsba13',
    'https://api.congress.gov/v3/committee/house/hsba13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 763: Domestic and International Monetary Policy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic and International Monetary Policy Subcommittee',
    'House',
    'hsba08',
    'https://api.congress.gov/v3/committee/house/hsba08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 764: Policy Research and Insurance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Policy Research and Insurance Subcommittee',
    'House',
    'hsba11',
    'https://api.congress.gov/v3/committee/house/hsba11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 765: Financial Institutions Supervision, Regulation and Deposit Insurance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Financial Institutions Supervision, Regulation and Deposit Insurance Subcommittee',
    'House',
    'hsba07',
    'https://api.congress.gov/v3/committee/house/hsba07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 766: International Development Institutions and Finance Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'International Development Institutions and Finance Subcommittee',
    'House',
    'hsba06',
    'https://api.congress.gov/v3/committee/house/hsba06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 767: Economic Growth and Credit Formation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Growth and Credit Formation Subcommittee',
    'House',
    'hsba14',
    'https://api.congress.gov/v3/committee/house/hsba14?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba14?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 768: Economic Stabilization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Economic Stabilization Subcommittee',
    'House',
    'hsba05',
    'https://api.congress.gov/v3/committee/house/hsba05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 769: Consumer Affairs and Coinage Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Consumer Affairs and Coinage Subcommittee',
    'House',
    'hsba02',
    'https://api.congress.gov/v3/committee/house/hsba02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsba02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 770: Panel on Business Challenges Within the Defense Industry Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Panel on Business Challenges Within the Defense Industry Subcommittee',
    'House',
    'hsas34',
    'https://api.congress.gov/v3/committee/house/hsas34?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas34?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 771: Defense Financial Management and Auditability Reform Panel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Financial Management and Auditability Reform Panel Subcommittee',
    'House',
    'hsas33',
    'https://api.congress.gov/v3/committee/house/hsas33?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas33?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 772: Projection Forces Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Projection Forces Subcommittee',
    'House',
    'hsas30',
    'https://api.congress.gov/v3/committee/house/hsas30?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas30?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 773: Special Oversight Panel on Department of Energy Reorganization Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Special Oversight Panel on Department of Energy Reorganization Subcommittee',
    'House',
    'hsas23',
    'https://api.congress.gov/v3/committee/house/hsas23?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 774: Seapower and Strategic and Critical Materials Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Seapower and Strategic and Critical Materials Subcommittee',
    'House',
    'hsas05',
    'https://api.congress.gov/v3/committee/house/hsas05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 775: Defense Policy Panel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Policy Panel Subcommittee',
    'House',
    'hsas08',
    'https://api.congress.gov/v3/committee/house/hsas08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 776: Special Oversight Panel on  Morale, Welfare, and Recreation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Special Oversight Panel on  Morale, Welfare, and Recreation Subcommittee',
    'House',
    'hsas12',
    'https://api.congress.gov/v3/committee/house/hsas12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 777: Military Procurement Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Procurement Subcommittee',
    'House',
    'hsas20',
    'https://api.congress.gov/v3/committee/house/hsas20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 778: Special Oversight Panel on Merchant Marine Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Special Oversight Panel on Merchant Marine Subcommittee',
    'House',
    'hsas22',
    'https://api.congress.gov/v3/committee/house/hsas22?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas22?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 779: Military Installations and Facilities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Installations and Facilities Subcommittee',
    'House',
    'hsas04',
    'https://api.congress.gov/v3/committee/house/hsas04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 780: Oversight and Investigations Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Oversight and Investigations Subcommittee',
    'House',
    'hsas06',
    'https://api.congress.gov/v3/committee/house/hsas06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 781: Special Oversight Panel on Terrorism Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Special Oversight Panel on Terrorism Subcommittee',
    'House',
    'hsas24',
    'https://api.congress.gov/v3/committee/house/hsas24?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 782: Total Force Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Total Force Subcommittee',
    'House',
    'hsas27',
    'https://api.congress.gov/v3/committee/house/hsas27?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 783: Procurement and Military Nuclear Systems Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Procurement and Military Nuclear Systems Subcommittee',
    'House',
    'hsas07',
    'https://api.congress.gov/v3/committee/house/hsas07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 784: Military Research and Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Research and Development Subcommittee',
    'House',
    'hsas01',
    'https://api.congress.gov/v3/committee/house/hsas01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 785: Defense Acquisition Reform Panel Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Defense Acquisition Reform Panel Subcommittee',
    'House',
    'hsas11',
    'https://api.congress.gov/v3/committee/house/hsas11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsas11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 786: Treasury, Postal Service, and General Government Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Treasury, Postal Service, and General Government Subcommittee',
    'House',
    'hsap13',
    'https://api.congress.gov/v3/committee/house/hsap13?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap13?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 787: Forestry, Resource Conservation and Research Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Forestry, Resource Conservation and Research Subcommittee',
    'House',
    'hsag27',
    'https://api.congress.gov/v3/committee/house/hsag27?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag27?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 788: General Farm Commodities, Resource Conservation and Credit Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'General Farm Commodities, Resource Conservation and Credit Subcommittee',
    'House',
    'hsag23',
    'https://api.congress.gov/v3/committee/house/hsag23?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag23?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 789: General Farm Commodities Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'General Farm Commodities Subcommittee',
    'House',
    'hsag25',
    'https://api.congress.gov/v3/committee/house/hsag25?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag25?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 790: Department Operations, Nutrition and Foreign Agriculture Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department Operations, Nutrition and Foreign Agriculture Subcommittee',
    'House',
    'hsag26',
    'https://api.congress.gov/v3/committee/house/hsag26?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag26?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 791: Risk Management, Research and Specialty Crops Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Risk Management, Research and Specialty Crops Subcommittee',
    'House',
    'hsag28',
    'https://api.congress.gov/v3/committee/house/hsag28?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag28?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 792: District of Columbia Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'District of Columbia Subcommittee',
    'House',
    'hsap03',
    'https://api.congress.gov/v3/committee/house/hsap03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 793: VA, HUD, and Independent Agencies Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'VA, HUD, and Independent Agencies Subcommittee',
    'House',
    'hsap05',
    'https://api.congress.gov/v3/committee/house/hsap05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 794: Legislative Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Legislative Subcommittee',
    'House',
    'hsap08',
    'https://api.congress.gov/v3/committee/house/hsap08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 795: Military Construction Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Military Construction Subcommittee',
    'House',
    'hsap09',
    'https://api.congress.gov/v3/committee/house/hsap09?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap09?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 796: Commerce, Justice, State, and the Judiciary Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Commerce, Justice, State, and the Judiciary Subcommittee',
    'House',
    'hsap11',
    'https://api.congress.gov/v3/committee/house/hsap11?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap11?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 797: Transportation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Transportation Subcommittee',
    'House',
    'hsap12',
    'https://api.congress.gov/v3/committee/house/hsap12?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsap12?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 798: Risk Management and Specialty Crops Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Risk Management and Specialty Crops Subcommittee',
    'House',
    'hsag24',
    'https://api.congress.gov/v3/committee/house/hsag24?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag24?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 799: Wheat, Soybeans, and Feed Grains Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Wheat, Soybeans, and Feed Grains Subcommittee',
    'House',
    'hsag08',
    'https://api.congress.gov/v3/committee/house/hsag08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 800: Department Operations and Nutrition Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department Operations and Nutrition Subcommittee',
    'House',
    'hsag20',
    'https://api.congress.gov/v3/committee/house/hsag20?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag20?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Progress: 800/815 committees processed

-- Committee 801: Foreign Agriculture and Hunger Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Foreign Agriculture and Hunger Subcommittee',
    'House',
    'hsag21',
    'https://api.congress.gov/v3/committee/house/hsag21?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag21?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 802: Peanuts and Tobacco Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Peanuts and Tobacco Subcommittee',
    'House',
    'hsag07',
    'https://api.congress.gov/v3/committee/house/hsag07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 803: Forests, Family Farms, and Energy Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Forests, Family Farms, and Energy Subcommittee',
    'House',
    'hsag06',
    'https://api.congress.gov/v3/committee/house/hsag06?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag06?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 804: Domestic Marketing, Consumer Relations, and Nutrition Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Domestic Marketing, Consumer Relations, and Nutrition Subcommittee',
    'House',
    'hsag05',
    'https://api.congress.gov/v3/committee/house/hsag05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 805: Department Operations, Research, and Foreign Agriculture Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Department Operations, Research, and Foreign Agriculture Subcommittee',
    'House',
    'hsag04',
    'https://api.congress.gov/v3/committee/house/hsag04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 806: Cotton, Rice, and Sugar Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Cotton, Rice, and Sugar Subcommittee',
    'House',
    'hsag02',
    'https://api.congress.gov/v3/committee/house/hsag02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 807: Environment, Credit and Rural Development Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Environment, Credit and Rural Development Subcommittee',
    'House',
    'hsag01',
    'https://api.congress.gov/v3/committee/house/hsag01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hsag01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 808: Retirement Income and Employment Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Retirement Income and Employment Subcommittee',
    'House',
    'hlse04',
    'https://api.congress.gov/v3/committee/house/hlse04?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlse04?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 809: Housing and Consumer Interests Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Housing and Consumer Interests Subcommittee',
    'House',
    'hlse03',
    'https://api.congress.gov/v3/committee/house/hlse03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlse03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 810: Health and Long-Term Care Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Health and Long-Term Care Subcommittee',
    'House',
    'hlse02',
    'https://api.congress.gov/v3/committee/house/hlse02?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlse02?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 811: Human Services Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Human Services Subcommittee',
    'House',
    'hlse01',
    'https://api.congress.gov/v3/committee/house/hlse01?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlse01?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 812: Terrorism and Homeland Security Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Terrorism and Homeland Security Subcommittee',
    'House',
    'hlig07',
    'https://api.congress.gov/v3/committee/house/hlig07?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlig07?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 813: Intelligence Modernization and Readiness Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Intelligence Modernization and Readiness Subcommittee',
    'House',
    'hlig08',
    'https://api.congress.gov/v3/committee/house/hlig08?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlig08?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 814: Emerging Threats Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Emerging Threats Subcommittee',
    'House',
    'hlig03',
    'https://api.congress.gov/v3/committee/house/hlig03?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlig03?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

-- Committee 815: Counterterrorism, Counterintelligence, and Counterproliferation Subcommittee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    'Counterterrorism, Counterintelligence, and Counterproliferation Subcommittee',
    'House',
    'hlig05',
    'https://api.congress.gov/v3/committee/house/hlig05?format=json',
    false,
    true,
    'https://api.congress.gov/v3/committee/house/hlig05?format=json',
    NOW()
) ON CONFLICT (name, chamber) DO NOTHING;

COMMIT;

-- Deployment complete!
-- Total committees processed: 815