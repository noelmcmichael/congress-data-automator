-- Final, Definitive Curation for Senate Judiciary Committee
-- Manually curated on 2025-07-10 with hardcoded IDs
BEGIN;

-- Clear existing assignments for the Judiciary Committee (ID=1)
DELETE FROM member_assignments WHERE committee_id = 1;

-- Insert the 21 verified members with hardcoded IDs
-- Leadership
INSERT INTO member_assignments (member_id, committee_id, assignment_type, authority_source, status) VALUES (542, 1, 'chair', 'editorial', 'published'); -- Chuck Grassley
INSERT INTO member_assignments (member_id, committee_id, assignment_type, authority_source, status) VALUES (552, 1, 'ranking_member', 'editorial', 'published'); -- Dick Durbin

-- Majority Members
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (547, 1, 'published'); -- Lindsey Graham
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (557, 1, 'published'); -- John Cornyn
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (528, 1, 'published'); -- Mike Lee
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (549, 1, 'published'); -- Ted Cruz
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (36, 1, 'published'); -- Josh Hawley
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (497, 1, 'published'); -- Thom Tillis
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (531, 1, 'published'); -- John Kennedy
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (570, 1, 'published'); -- Marsha Blackburn
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (479, 1, 'published'); -- Eric Schmitt
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (481, 1, 'published'); -- Katie Britt
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (41, 1, 'published'); -- Ashley Moody

-- Minority Members
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (491, 1, 'published'); -- Sheldon Whitehouse
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (527, 1, 'published'); -- Amy Klobuchar
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (558, 1, 'published'); -- Chris Coons
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (565, 1, 'published'); -- Richard Blumenthal
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (537, 1, 'published'); -- Mazie Hirono
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (564, 1, 'published'); -- Cory Booker
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (513, 1, 'published'); -- Alex Padilla
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (37, 1, 'published'); -- Peter Welch
INSERT INTO member_assignments (member_id, committee_id, status) VALUES (507, 1, 'published'); -- Adam Schiff

COMMIT;
