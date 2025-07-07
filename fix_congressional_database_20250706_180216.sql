-- Clear existing committee and relationship data
DELETE FROM committee_memberships;
DELETE FROM committees;

-- Insert real congressional committees
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (1, 'Committee on Agriculture', 'House', 'Agriculture, nutrition, and related programs', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (7, 'Committee on Appropriations', 'House', 'Federal government spending and budget appropriations', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (20, 'Committee on Armed Services', 'House', 'National defense and military affairs', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (28, 'Committee on the Budget', 'House', 'Federal budget process and fiscal policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (29, 'Committee on Education and the Workforce', 'House', 'Education and labor policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (34, 'Committee on Energy and Commerce', 'House', 'Energy, commerce, telecommunications, and consumer protection', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (41, 'Committee on Financial Services', 'House', 'Banking, financial services, and housing', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (48, 'Committee on Foreign Affairs', 'House', 'Foreign policy and international relations', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (56, 'Committee on Homeland Security', 'House', 'Homeland security and emergency management', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (63, 'Committee on House Administration', 'House', 'House operations and administration', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (64, 'Committee on the Judiciary', 'House', 'Federal courts, constitutional law, and civil rights', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (70, 'Committee on Natural Resources', 'House', 'Natural resources, public lands, and environmental policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (76, 'Committee on Oversight and Accountability', 'House', 'Government oversight and accountability', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (82, 'Committee on Rules', 'House', 'House rules and procedures', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (83, 'Committee on Science, Space, and Technology', 'House', 'Science, space, and technology policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (89, 'Committee on Small Business', 'House', 'Small business policy and programs', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (95, 'Committee on Transportation and Infrastructure', 'House', 'Transportation, infrastructure, and public works', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (102, 'Committee on Veterans'' Affairs', 'House', 'Veterans programs and benefits', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (108, 'Committee on Ways and Means', 'House', 'Taxation, trade, and revenue', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (115, 'Committee on Agriculture, Nutrition, and Forestry', 'Senate', 'Agriculture, nutrition, and forestry policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (121, 'Committee on Appropriations', 'Senate', 'Federal government spending and appropriations', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (134, 'Committee on Armed Services', 'Senate', 'National defense and military affairs', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (142, 'Committee on Banking, Housing, and Urban Affairs', 'Senate', 'Banking, housing, and urban development', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (148, 'Committee on the Budget', 'Senate', 'Federal budget process and fiscal policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (149, 'Committee on Commerce, Science, and Transportation', 'Senate', 'Commerce, science, and transportation policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (157, 'Committee on Energy and Natural Resources', 'Senate', 'Energy and natural resources policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (162, 'Committee on Environment and Public Works', 'Senate', 'Environmental protection and public works', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (167, 'Committee on Finance', 'Senate', 'Taxation, trade, and social security', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (173, 'Committee on Foreign Relations', 'Senate', 'Foreign policy and international relations', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (181, 'Committee on Health, Education, Labor and Pensions', 'Senate', 'Health, education, and labor policy', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (185, 'Committee on Homeland Security and Governmental Affairs', 'Senate', 'Homeland security and government operations', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (189, 'Committee on the Judiciary', 'Senate', 'Federal courts, constitutional law, and immigration', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (197, 'Committee on Rules and Administration', 'Senate', 'Senate rules and election administration', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (198, 'Committee on Small Business and Entrepreneurship', 'Senate', 'Small business policy and programs', true, false);
INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES (199, 'Committee on Veterans'' Affairs', 'Senate', 'Veterans programs and benefits', true, false);

-- Insert committee memberships
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (208, 1, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (208, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (440, 102, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (402, 41, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (221, 102, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (317, 1, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (111, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (191, 20, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (414, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (95, 76, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (248, 70, 'Ranking Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (248, 41, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (63, 63, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (206, 76, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (206, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (284, 70, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (155, 20, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (155, 34, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (537, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (24, 64, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (454, 7, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (291, 108, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (373, 76, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (373, 83, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (245, 102, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (245, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (19, 70, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (337, 20, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (161, 34, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (442, 76, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (216, 102, 'Ranking Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (120, 102, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (120, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (427, 34, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (252, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (252, 95, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (62, 63, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (119, 70, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (73, 95, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (73, 1, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (421, 70, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (355, 7, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (327, 89, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (538, 29, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (531, 56, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (367, 102, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (367, 41, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (132, 70, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (132, 83, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (534, 20, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (290, 48, 'Chair', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (130, 7, 'Ranking Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (130, 48, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (117, 95, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (109, 29, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (151, 48, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (448, 142, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (448, 181, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (535, 121, 'Ranking Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (535, 181, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (535, 198, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (536, 181, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (536, 189, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (536, 197, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (533, 148, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (533, 157, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (533, 134, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (532, 198, 'Chair', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (532, 189, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (532, 197, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (532, 167, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (449, 115, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (449, 121, 'Member', true, '2023-01-01');
INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES (449, 189, 'Member', true, '2023-01-01');