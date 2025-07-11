-- Data Integrity: Merge Duplicate Member Records
-- Generated on 2025-07-10
BEGIN;

-- Group 1: John Boozman (AR) - Keep ID 15, Remove 566
UPDATE member_assignments SET member_id = 15 WHERE member_id = 566;
DELETE FROM members WHERE id = 566;

-- Group 2: Maria Cantwell (WA) - Keep ID 16, Remove 562
UPDATE member_assignments SET member_id = 16 WHERE member_id = 562;
DELETE FROM members WHERE id = 562;

-- Group 3: Bill Cassidy (LA) - Keep ID 4, Remove 559
UPDATE member_assignments SET member_id = 4 WHERE member_id = 559;
DELETE FROM members WHERE id = 559;

-- Group 4: Tom Cole (OK) - Keep ID 32, Remove 168
UPDATE member_assignments SET member_id = 32 WHERE member_id = 168;
DELETE FROM members WHERE id = 168;

-- Group 5: Mike Crapo (ID) - Keep ID 18, Remove 553
UPDATE member_assignments SET member_id = 18 WHERE member_id = 553;
DELETE FROM members WHERE id = 553;

-- Group 6: Ted Cruz (TX) - Keep ID 30, Remove 549
UPDATE member_assignments SET member_id = 30 WHERE member_id = 549;
DELETE FROM members WHERE id = 549;

-- Group 7: Chuck Grassley (IA) - Keep ID 6, Remove 542
UPDATE member_assignments SET member_id = 6 WHERE member_id = 542;
DELETE FROM members WHERE id = 542;

-- Group 8: Brett Guthrie (KY) - Keep ID 5, Remove 326
UPDATE member_assignments SET member_id = 5 WHERE member_id = 326;
DELETE FROM members WHERE id = 326;

-- Group 9: Martin Heinrich (NM) - Keep ID 17, Remove 541
UPDATE member_assignments SET member_id = 17 WHERE member_id = 541;
DELETE FROM members WHERE id = 541;

-- Group 10: Amy Klobuchar (MN) - Keep ID 2, Remove 527
UPDATE member_assignments SET member_id = 2 WHERE member_id = 527;
DELETE FROM members WHERE id = 527;

-- Group 11: Mike Lee (UT) - Keep ID 19, Remove 528
UPDATE member_assignments SET member_id = 19 WHERE member_id = 528;
DELETE FROM members WHERE id = 528;

-- Group 12: Patty Murray (WA) - Keep ID 21, Remove 516
UPDATE member_assignments SET member_id = 21 WHERE member_id = 516;
DELETE FROM members WHERE id = 516;

-- Group 13: Frank Pallone (NJ) - Keep ID 9, Remove 226
UPDATE member_assignments SET member_id = 9 WHERE member_id = 226;
DELETE FROM members WHERE id = 226;

-- Group 14: Rand Paul (KY) - Keep ID 22, Remove 515
UPDATE member_assignments SET member_id = 22 WHERE member_id = 515;
DELETE FROM members WHERE id = 515;

-- Group 15: Jack Reed (RI) - Keep ID 11, Remove 512
UPDATE member_assignments SET member_id = 11 WHERE member_id = 512;
DELETE FROM members WHERE id = 512;

-- Group 16: Tim Scott (SC) - Keep ID 31, Remove 504
UPDATE member_assignments SET member_id = 31 WHERE member_id = 504;
DELETE FROM members WHERE id = 504;

-- Group 17: Jeanne Shaheen (NH) - Keep ID 13, Remove 501
UPDATE member_assignments SET member_id = 13 WHERE member_id = 501;
DELETE FROM members WHERE id = 501;

-- Group 18: Adam Smith (WA) - Keep ID 1, Remove 69
UPDATE member_assignments SET member_id = 1 WHERE member_id = 69;
DELETE FROM members WHERE id = 69;

-- Group 19: Jason Smith (MO) - Keep ID 12, Remove 268
UPDATE member_assignments SET member_id = 12 WHERE member_id = 268;
DELETE FROM members WHERE id = 268;

-- Group 20: Elizabeth Warren (MA) - Keep ID 8, Remove 490
UPDATE member_assignments SET member_id = 8 WHERE member_id = 490;
DELETE FROM members WHERE id = 490;

-- Group 21: Sheldon Whitehouse (RI) - Keep ID 27, Remove 491
UPDATE member_assignments SET member_id = 27 WHERE member_id = 491;
DELETE FROM members WHERE id = 491;

-- Group 22: Ron Wyden (OR) - Keep ID 25, Remove 488
UPDATE member_assignments SET member_id = 25 WHERE member_id = 488;
DELETE FROM members WHERE id = 488;

COMMIT;
