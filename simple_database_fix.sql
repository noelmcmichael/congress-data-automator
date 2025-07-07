-- Clear existing committee and relationship data
DELETE FROM committee_memberships;
DELETE FROM committees;

-- Insert real congressional committees
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (1, 'Committee on Agriculture', 'House', 'Agriculture, nutrition, and related programs', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (2, 'Biotechnology, Horticulture, and Research Subcommittee', 'House', 'Subcommittee of Committee on Agriculture', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (3, 'Commodity Exchanges, Energy, and Credit Subcommittee', 'House', 'Subcommittee of Committee on Agriculture', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (4, 'Conservation and Forestry Subcommittee', 'House', 'Subcommittee of Committee on Agriculture', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (5, 'General Farm Commodities, Risk Management, and Credit Subcommittee', 'House', 'Subcommittee of Committee on Agriculture', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (6, 'Livestock and Foreign Agriculture Subcommittee', 'House', 'Subcommittee of Committee on Agriculture', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (7, 'Committee on Appropriations', 'House', 'Federal government spending and budget appropriations', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (8, 'Agriculture, Rural Development, Food and Drug Administration Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (9, 'Commerce, Justice, Science, and Related Agencies Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (10, 'Defense Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (11, 'Energy and Water Development Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (12, 'Financial Services and General Government Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (13, 'Homeland Security Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (14, 'Interior, Environment, and Related Agencies Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (15, 'Labor, Health and Human Services, Education Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (16, 'Legislative Branch Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (17, 'Military Construction, Veterans Affairs Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (18, 'State, Foreign Operations, and Related Programs Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (19, 'Transportation, Housing and Urban Development Subcommittee', 'House', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (20, 'Committee on Armed Services', 'House', 'National defense and military affairs', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (21, 'Cyber, Information Technologies, and Innovation Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (22, 'Intelligence and Special Operations Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (23, 'Military Personnel Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (24, 'Readiness Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (25, 'Seapower and Projection Forces Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (26, 'Strategic Forces Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (27, 'Tactical Air and Land Forces Subcommittee', 'House', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (28, 'Committee on the Budget', 'House', 'Federal budget process and fiscal policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (29, 'Committee on Education and the Workforce', 'House', 'Education and labor policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (30, 'Early Childhood, Elementary, and Secondary Education Subcommittee', 'House', 'Subcommittee of Committee on Education and the Workforce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (31, 'Health, Employment, Labor, and Pensions Subcommittee', 'House', 'Subcommittee of Committee on Education and the Workforce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (32, 'Higher Education and Workforce Development Subcommittee', 'House', 'Subcommittee of Committee on Education and the Workforce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (33, 'Workforce Protections Subcommittee', 'House', 'Subcommittee of Committee on Education and the Workforce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (34, 'Committee on Energy and Commerce', 'House', 'Energy, commerce, telecommunications, and consumer protection', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (35, 'Communications and Technology Subcommittee', 'House', 'Subcommittee of Committee on Energy and Commerce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (36, 'Energy, Climate, and Grid Security Subcommittee', 'House', 'Subcommittee of Committee on Energy and Commerce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (37, 'Environment, Manufacturing, and Critical Materials Subcommittee', 'House', 'Subcommittee of Committee on Energy and Commerce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (38, 'Health Subcommittee', 'House', 'Subcommittee of Committee on Energy and Commerce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (39, 'Innovation, Data, and Commerce Subcommittee', 'House', 'Subcommittee of Committee on Energy and Commerce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (40, 'Oversight and Investigations Subcommittee', 'House', 'Subcommittee of Committee on Energy and Commerce', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (41, 'Committee on Financial Services', 'House', 'Banking, financial services, and housing', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (42, 'Capital Markets Subcommittee', 'House', 'Subcommittee of Committee on Financial Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (43, 'Digital Assets, Financial Technology and Inclusion Subcommittee', 'House', 'Subcommittee of Committee on Financial Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (44, 'Financial Institutions and Monetary Policy Subcommittee', 'House', 'Subcommittee of Committee on Financial Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (45, 'Housing and Insurance Subcommittee', 'House', 'Subcommittee of Committee on Financial Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (46, 'National Security, Illicit Finance, and International Financial Institutions Subcommittee', 'House', 'Subcommittee of Committee on Financial Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (47, 'Oversight and Investigations Subcommittee', 'House', 'Subcommittee of Committee on Financial Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (48, 'Committee on Foreign Affairs', 'House', 'Foreign policy and international relations', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (49, 'Africa Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (50, 'Europe Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (51, 'Indo-Pacific Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (52, 'Middle East, North Africa and Central Asia Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (53, 'Oversight and Accountability Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (54, 'Global Health, Global Human Rights, and International Organizations Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (55, 'Western Hemisphere Subcommittee', 'House', 'Subcommittee of Committee on Foreign Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (56, 'Committee on Homeland Security', 'House', 'Homeland security and emergency management', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (57, 'Border Security and Enforcement Subcommittee', 'House', 'Subcommittee of Committee on Homeland Security', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (58, 'Counterterrorism, Law Enforcement, and Intelligence Subcommittee', 'House', 'Subcommittee of Committee on Homeland Security', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (59, 'Cybersecurity and Infrastructure Protection Subcommittee', 'House', 'Subcommittee of Committee on Homeland Security', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (60, 'Emergency Management and Technology Subcommittee', 'House', 'Subcommittee of Committee on Homeland Security', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (61, 'Oversight, Investigations, and Accountability Subcommittee', 'House', 'Subcommittee of Committee on Homeland Security', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (62, 'Transportation and Maritime Security Subcommittee', 'House', 'Subcommittee of Committee on Homeland Security', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (63, 'Committee on House Administration', 'House', 'House operations and administration', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (64, 'Committee on the Judiciary', 'House', 'Federal courts, constitutional law, and civil rights', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (65, 'Courts, Intellectual Property, and the Internet Subcommittee', 'House', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (66, 'Crime and Federal Government Surveillance Subcommittee', 'House', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (67, 'Immigration Integrity, Security, and Enforcement Subcommittee', 'House', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (68, 'Responsiveness and Accountability to Oversight Subcommittee', 'House', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (69, 'the Constitution and Limited Government Subcommittee', 'House', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (70, 'Committee on Natural Resources', 'House', 'Natural resources, public lands, and environmental policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (71, 'Energy and Mineral Resources Subcommittee', 'House', 'Subcommittee of Committee on Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (72, 'Federal Lands Subcommittee', 'House', 'Subcommittee of Committee on Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (73, 'Indigenous Peoples of the United States Subcommittee', 'House', 'Subcommittee of Committee on Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (74, 'Oversight and Investigations Subcommittee', 'House', 'Subcommittee of Committee on Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (75, 'Water, Wildlife, and Fisheries Subcommittee', 'House', 'Subcommittee of Committee on Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (76, 'Committee on Oversight and Accountability', 'House', 'Government oversight and accountability', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (77, 'Cybersecurity, Information Technology, and Government Innovation Subcommittee', 'House', 'Subcommittee of Committee on Oversight and Accountability', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (78, 'Economic Growth, Energy Policy, and Regulatory Affairs Subcommittee', 'House', 'Subcommittee of Committee on Oversight and Accountability', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (79, 'Government Operations and the Federal Workforce Subcommittee', 'House', 'Subcommittee of Committee on Oversight and Accountability', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (80, 'Health Care and Financial Services Subcommittee', 'House', 'Subcommittee of Committee on Oversight and Accountability', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (81, 'National Security, the Border, and Foreign Affairs Subcommittee', 'House', 'Subcommittee of Committee on Oversight and Accountability', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (82, 'Committee on Rules', 'House', 'House rules and procedures', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (83, 'Committee on Science, Space, and Technology', 'House', 'Science, space, and technology policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (84, 'Energy Subcommittee', 'House', 'Subcommittee of Committee on Science, Space, and Technology', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (85, 'Environment Subcommittee', 'House', 'Subcommittee of Committee on Science, Space, and Technology', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (86, 'Investigations and Oversight Subcommittee', 'House', 'Subcommittee of Committee on Science, Space, and Technology', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (87, 'Research and Technology Subcommittee', 'House', 'Subcommittee of Committee on Science, Space, and Technology', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (88, 'Space and Aeronautics Subcommittee', 'House', 'Subcommittee of Committee on Science, Space, and Technology', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (89, 'Committee on Small Business', 'House', 'Small business policy and programs', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (90, 'Economic Growth, Tax, and Capital Access Subcommittee', 'House', 'Subcommittee of Committee on Small Business', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (91, 'Innovation, Entrepreneurship, and Workforce Development Subcommittee', 'House', 'Subcommittee of Committee on Small Business', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (92, 'Oversight, Investigations, and Regulations Subcommittee', 'House', 'Subcommittee of Committee on Small Business', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (93, 'Rural Development, Energy, and Supply Chains Subcommittee', 'House', 'Subcommittee of Committee on Small Business', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (94, 'Underserved, Agricultural, and Rural Business Development Subcommittee', 'House', 'Subcommittee of Committee on Small Business', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (95, 'Committee on Transportation and Infrastructure', 'House', 'Transportation, infrastructure, and public works', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (96, 'Aviation Subcommittee', 'House', 'Subcommittee of Committee on Transportation and Infrastructure', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (97, 'Coast Guard and Maritime Transportation Subcommittee', 'House', 'Subcommittee of Committee on Transportation and Infrastructure', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (98, 'Economic Development, Public Buildings, and Emergency Management Subcommittee', 'House', 'Subcommittee of Committee on Transportation and Infrastructure', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (99, 'Highways and Transit Subcommittee', 'House', 'Subcommittee of Committee on Transportation and Infrastructure', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (100, 'Railroads, Pipelines, and Hazardous Materials Subcommittee', 'House', 'Subcommittee of Committee on Transportation and Infrastructure', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (101, 'Water Resources and Environment Subcommittee', 'House', 'Subcommittee of Committee on Transportation and Infrastructure', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (102, 'Committee on Veterans'' Affairs', 'House', 'Veterans programs and benefits', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (103, 'Disability Assistance and Memorial Affairs Subcommittee', 'House', 'Subcommittee of Committee on Veterans'' Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (104, 'Economic Opportunity Subcommittee', 'House', 'Subcommittee of Committee on Veterans'' Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (105, 'Health Subcommittee', 'House', 'Subcommittee of Committee on Veterans'' Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (106, 'Oversight and Investigations Subcommittee', 'House', 'Subcommittee of Committee on Veterans'' Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (107, 'Technology Modernization Subcommittee', 'House', 'Subcommittee of Committee on Veterans'' Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (108, 'Committee on Ways and Means', 'House', 'Taxation, trade, and revenue', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (109, 'Health Subcommittee', 'House', 'Subcommittee of Committee on Ways and Means', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (110, 'Oversight Subcommittee', 'House', 'Subcommittee of Committee on Ways and Means', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (111, 'Select Revenue Measures Subcommittee', 'House', 'Subcommittee of Committee on Ways and Means', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (112, 'Social Security Subcommittee', 'House', 'Subcommittee of Committee on Ways and Means', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (113, 'Trade Subcommittee', 'House', 'Subcommittee of Committee on Ways and Means', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (114, 'Worker and Family Support Subcommittee', 'House', 'Subcommittee of Committee on Ways and Means', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (115, 'Committee on Agriculture, Nutrition, and Forestry', 'Senate', 'Agriculture, nutrition, and forestry policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (116, 'Commodities, Risk Management, and Trade Subcommittee', 'Senate', 'Subcommittee of Committee on Agriculture, Nutrition, and Forestry', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (117, 'Conservation, Climate, Forestry, and Natural Resources Subcommittee', 'Senate', 'Subcommittee of Committee on Agriculture, Nutrition, and Forestry', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (118, 'Food and Nutrition, Specialty Crops, Organics, and Research Subcommittee', 'Senate', 'Subcommittee of Committee on Agriculture, Nutrition, and Forestry', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (119, 'Livestock, Dairy, Poultry, Local Food Systems, and Food Safety and Security Subcommittee', 'Senate', 'Subcommittee of Committee on Agriculture, Nutrition, and Forestry', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (120, 'Rural Development and Energy Subcommittee', 'Senate', 'Subcommittee of Committee on Agriculture, Nutrition, and Forestry', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (121, 'Committee on Appropriations', 'Senate', 'Federal government spending and appropriations', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (122, 'Agriculture, Rural Development, Food and Drug Administration Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (123, 'Commerce, Justice, Science, and Related Agencies Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (124, 'Defense Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (125, 'Energy and Water Development Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (126, 'Financial Services and General Government Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (127, 'Homeland Security Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (128, 'Interior, Environment, and Related Agencies Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (129, 'Labor, Health and Human Services, Education Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (130, 'Legislative Branch Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (131, 'Military Construction, Veterans Affairs Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (132, 'State, Foreign Operations, and Related Programs Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (133, 'Transportation, Housing and Urban Development Subcommittee', 'Senate', 'Subcommittee of Committee on Appropriations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (134, 'Committee on Armed Services', 'Senate', 'National defense and military affairs', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (135, 'Airland Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (136, 'Cybersecurity Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (137, 'Emerging Threats and Capabilities Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (138, 'Personnel Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (139, 'Readiness and Management Support Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (140, 'Seapower Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (141, 'Strategic Forces Subcommittee', 'Senate', 'Subcommittee of Committee on Armed Services', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (142, 'Committee on Banking, Housing, and Urban Affairs', 'Senate', 'Banking, housing, and urban development', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (143, 'Economic Policy Subcommittee', 'Senate', 'Subcommittee of Committee on Banking, Housing, and Urban Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (144, 'Financial Institutions and Consumer Protection Subcommittee', 'Senate', 'Subcommittee of Committee on Banking, Housing, and Urban Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (145, 'Housing, Transportation, and Community Development Subcommittee', 'Senate', 'Subcommittee of Committee on Banking, Housing, and Urban Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (146, 'National Security and International Trade and Finance Subcommittee', 'Senate', 'Subcommittee of Committee on Banking, Housing, and Urban Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (147, 'Securities, Insurance, and Investment Subcommittee', 'Senate', 'Subcommittee of Committee on Banking, Housing, and Urban Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (148, 'Committee on the Budget', 'Senate', 'Federal budget process and fiscal policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (149, 'Committee on Commerce, Science, and Transportation', 'Senate', 'Commerce, science, and transportation policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (150, 'Aviation Safety, Operations, and Innovation Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (151, 'Communications, Media, and Broadband Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (152, 'Consumer Protection, Product Safety, and Data Security Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (153, 'Oceans, Fisheries, Climate Change, and Manufacturing Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (154, 'Space and Science Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (155, 'Surface Transportation, Maritime, Freight, and Ports Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (156, 'Tourism, Trade, and Export Promotion Subcommittee', 'Senate', 'Subcommittee of Committee on Commerce, Science, and Transportation', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (157, 'Committee on Energy and Natural Resources', 'Senate', 'Energy and natural resources policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (158, 'Energy Subcommittee', 'Senate', 'Subcommittee of Committee on Energy and Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (159, 'National Parks Subcommittee', 'Senate', 'Subcommittee of Committee on Energy and Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (160, 'Public Lands, Forests, and Mining Subcommittee', 'Senate', 'Subcommittee of Committee on Energy and Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (161, 'Water and Power Subcommittee', 'Senate', 'Subcommittee of Committee on Energy and Natural Resources', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (162, 'Committee on Environment and Public Works', 'Senate', 'Environmental protection and public works', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (163, 'Chemical Safety, Waste Management, Environmental Justice, and Regulatory Oversight Subcommittee', 'Senate', 'Subcommittee of Committee on Environment and Public Works', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (164, 'Clean Air, Climate, and Nuclear Safety Subcommittee', 'Senate', 'Subcommittee of Committee on Environment and Public Works', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (165, 'Fisheries, Water, and Wildlife Subcommittee', 'Senate', 'Subcommittee of Committee on Environment and Public Works', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (166, 'Transportation and Infrastructure Subcommittee', 'Senate', 'Subcommittee of Committee on Environment and Public Works', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (167, 'Committee on Finance', 'Senate', 'Taxation, trade, and social security', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (168, 'Energy, Natural Resources, and Infrastructure Subcommittee', 'Senate', 'Subcommittee of Committee on Finance', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (169, 'Fiscal Responsibility and Economic Growth Subcommittee', 'Senate', 'Subcommittee of Committee on Finance', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (170, 'Health Care Subcommittee', 'Senate', 'Subcommittee of Committee on Finance', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (171, 'International Trade, Customs, and Global Competitiveness Subcommittee', 'Senate', 'Subcommittee of Committee on Finance', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (172, 'Social Security, Pensions, and Family Policy Subcommittee', 'Senate', 'Subcommittee of Committee on Finance', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (173, 'Committee on Foreign Relations', 'Senate', 'Foreign policy and international relations', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (174, 'Africa and Global Health Policy Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (175, 'East Asia, the Pacific, and International Cybersecurity Policy Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (176, 'Europe and Regional Security Cooperation Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (177, 'International Development and Multilateral Institutions Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (178, 'Near East, South Asia, Central Asia, and Counterterrorism Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (179, 'State Department and USAID Management, International Operations, and Bilateral International Development Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (180, 'Western Hemisphere, Transnational Crime, Civilian Security, Democracy, Human Rights, and Global Women''s Issues Subcommittee', 'Senate', 'Subcommittee of Committee on Foreign Relations', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (181, 'Committee on Health, Education, Labor and Pensions', 'Senate', 'Health, education, and labor policy', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (182, 'Children and Families Subcommittee', 'Senate', 'Subcommittee of Committee on Health, Education, Labor and Pensions', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (183, 'Employment and Workplace Safety Subcommittee', 'Senate', 'Subcommittee of Committee on Health, Education, Labor and Pensions', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (184, 'Primary Health and Retirement Security Subcommittee', 'Senate', 'Subcommittee of Committee on Health, Education, Labor and Pensions', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (185, 'Committee on Homeland Security and Governmental Affairs', 'Senate', 'Homeland security and government operations', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (186, 'Emerging Threats and Spending Oversight Subcommittee', 'Senate', 'Subcommittee of Committee on Homeland Security and Governmental Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (187, 'Government Operations and Border Management Subcommittee', 'Senate', 'Subcommittee of Committee on Homeland Security and Governmental Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (188, 'Investigations Subcommittee', 'Senate', 'Subcommittee of Committee on Homeland Security and Governmental Affairs', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (189, 'Committee on the Judiciary', 'Senate', 'Federal courts, constitutional law, and immigration', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (190, 'Competition Policy, Antitrust, and Consumer Rights Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (191, 'Criminal Justice and Counterterrorism Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (192, 'Federal Courts, Oversight, Agency Action, and Federal Rights Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (193, 'Human Rights and the Law Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (194, 'Immigration, Citizenship, and Border Safety Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (195, 'Intellectual Property Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (196, 'Privacy, Technology, and the Law Subcommittee', 'Senate', 'Subcommittee of Committee on the Judiciary', true, true, 'Subcommittee');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (197, 'Committee on Rules and Administration', 'Senate', 'Senate rules and election administration', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (198, 'Committee on Small Business and Entrepreneurship', 'Senate', 'Small business policy and programs', true, false, 'Standing');
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES (199, 'Committee on Veterans'' Affairs', 'Senate', 'Veterans programs and benefits', true, false, 'Standing');

-- Insert committee memberships
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (208, 1, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (208, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (440, 102, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (402, 41, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (221, 102, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (317, 1, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (111, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (191, 20, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (414, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (95, 76, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (248, 70, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (248, 41, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (63, 63, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (206, 76, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (206, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (284, 70, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (155, 20, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (155, 34, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (537, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (24, 64, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (454, 7, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (291, 108, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (373, 76, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (373, 83, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (245, 102, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (245, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (19, 70, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (337, 20, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (161, 34, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (442, 76, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (216, 102, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (120, 102, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (120, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (427, 34, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (252, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (252, 95, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (62, 63, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (119, 70, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (73, 95, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (73, 1, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (421, 70, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (355, 7, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (327, 89, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (538, 29, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (531, 56, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (367, 102, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (367, 41, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (132, 70, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (132, 83, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (534, 20, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (290, 48, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (130, 7, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (130, 48, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (117, 95, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (109, 29, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (151, 48, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (448, 142, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (448, 181, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (535, 121, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (535, 181, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (535, 198, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (536, 181, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (536, 189, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (536, 197, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (533, 148, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (533, 157, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (533, 134, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (532, 198, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (532, 189, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (532, 197, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (532, 167, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (449, 115, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (449, 121, 'Member', true);
INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES (449, 189, 'Member', true);
