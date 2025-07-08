-- Add committees column to members table if not exists
ALTER TABLE members ADD COLUMN IF NOT EXISTS committees JSONB DEFAULT '[]'::jsonb;

-- Update member committee assignments
-- Update Chuck Grassley (IA)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}, {"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 510;

-- Update Lindsey Graham (SC)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 515;

-- Update John Cornyn (TX)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}, {"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 525;

-- Update Mike Lee (UT)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 496;

-- Update Ted Cruz (TX)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 517;

-- Update Josh Hawley (MO)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 4;

-- Update Tom Cotton (AR)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}, {"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 524;

-- Update John Kennedy (LA)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 499;

-- Update Sheldon Whitehouse (RI)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}, {"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 459;

-- Update Amy Klobuchar (MN)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 495;

-- Update Richard Blumenthal (CT)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}, {"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 533;

-- Update Mazie Hirono (HI)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}, {"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 505;

-- Update Cory Booker (NJ)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 532;

-- Update Alex Padilla (CA)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 481;

-- Update Jon Ossoff (GA)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 482;

-- Update Peter Welch (VT)
UPDATE members SET committees = '[{"id": 189, "name": "Committee on the Judiciary", "role": "Member"}]'::jsonb WHERE id = 5;

-- Update Roger Wicker (MS)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 461;

-- Update Deb Fischer (NE)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 513;

-- Update Mike Rounds (SD)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 470;

-- Update Joni Ernst (IA)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 516;

-- Update Dan Sullivan (AK)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 466;

-- Update Kevin Cramer (ND)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 523;

-- Update Rick Scott (FL)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 468;

-- Update Jack Reed (RI)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 480;

-- Update Jeanne Shaheen (NH)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 469;

-- Update Kirsten Gillibrand (NY)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 514;

-- Update Tim Kaine (VA)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 500;

-- Update Angus King (ME)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 494;

-- Update Martin Heinrich (NM)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 509;

-- Update Elizabeth Warren (MA)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}, {"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 458;

-- Update Gary Peters (MI)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 478;

-- Update Jacky Rosen (NV)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 477;

-- Update Mark Kelly (AZ)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 498;

-- Update Elissa Slotkin (MI)
UPDATE members SET committees = '[{"id": 134, "name": "Committee on Armed Services", "role": "Member"}]'::jsonb WHERE id = 451;

-- Update Mike Crapo (ID)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 521;

-- Update John Thune (SD)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 467;

-- Update Tim Scott (SC)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 472;

-- Update Bill Cassidy (LA)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 527;

-- Update James Lankford (OK)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 497;

-- Update Steve Daines (MT)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 518;

-- Update Todd Young (IN)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 455;

-- Update Ron Wyden (OR)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 456;

-- Update Maria Cantwell (WA)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 530;

-- Update Michael Bennet (CO)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 536;

-- Update Mark Warner (VA)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 460;

-- Update Catherine Cortez Masto (NV)
UPDATE members SET committees = '[{"id": 167, "name": "Committee on Finance", "role": "Member"}]'::jsonb WHERE id = 522;

-- Create index for committee queries
CREATE INDEX IF NOT EXISTS idx_members_committees ON members USING gin(committees);
