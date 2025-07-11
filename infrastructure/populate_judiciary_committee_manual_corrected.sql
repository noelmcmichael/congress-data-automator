-- Final Curation for Senate Judiciary Committee (Corrected)
-- Manually curated on 2025-07-10
BEGIN;

-- Clear existing assignments for the Judiciary Committee (ID=1)
DELETE FROM member_assignments WHERE committee_id = 1;

-- Insert the 21 verified members with specific first and last names
-- Leadership
INSERT INTO member_assignments (member_id, committee_id, assignment_type, authority_source, status) VALUES ((SELECT id FROM members WHERE first_name = 'Chuck' AND last_name = 'Grassley' AND state = 'IA'), 1, 'chair', 'editorial', 'published');
INSERT INTO member_assignments (member_id, committee_id, assignment_type, authority_source, status) VALUES ((SELECT id FROM members WHERE first_name = 'Dick' AND last_name = 'Durbin' AND state = 'IL'), 1, 'ranking_member', 'editorial', 'published');

-- Majority Members
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Lindsey' AND last_name = 'Graham' AND state = 'SC'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'John' AND last_name = 'Cornyn' AND state = 'TX'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Mike' AND last_name = 'Lee' AND state = 'UT'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Ted' AND last_name = 'Cruz' AND state = 'TX'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Josh' AND last_name = 'Hawley' AND state = 'MO'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Thom' AND last_name = 'Tillis' AND state = 'NC'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'John' AND last_name = 'Kennedy' AND state = 'LA'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Marsha' AND last_name = 'Blackburn' AND state = 'TN'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Eric' AND last_name = 'Schmitt' AND state = 'MO'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Katie' AND last_name = 'Britt' AND state = 'AL'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Ashley' AND last_name = 'Moody' AND state = 'FL'), 1, 'published');

-- Minority Members
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Sheldon' AND last_name = 'Whitehouse' AND state = 'RI'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Amy' AND last_name = 'Klobuchar' AND state = 'MN'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Chris' AND last_name = 'Coons' AND state = 'DE'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Richard' AND last_name = 'Blumenthal' AND state = 'CT'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Mazie' AND last_name = 'Hirono' AND state = 'HI'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Cory' AND last_name = 'Booker' AND state = 'NJ'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Alex' AND last_name = 'Padilla' AND state = 'CA'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Peter' AND last_name = 'Welch' AND state = 'VT'), 1, 'published');
INSERT INTO member_assignments (member_id, committee_id, status) VALUES ((SELECT id FROM members WHERE first_name = 'Adam' AND last_name = 'Schiff' AND state = 'CA'), 1, 'published');

COMMIT;
