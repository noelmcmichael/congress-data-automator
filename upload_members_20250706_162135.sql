
-- Clear existing members (they'll be replaced with complete dataset)
DELETE FROM committee_memberships;
DELETE FROM members;

-- Insert all collected members

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000617', 'Ramirez, Delia C.', '', '', 'Democratic', 'Illinois', 'House', 3, 'https://www.congress.gov/img/member/684c2356333714e4aee2e1fd_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001232', 'Sheehy, Tim', '', '', 'Republican', 'Montana', 'Senate', 0, 'https://www.congress.gov/img/member/677d8231fdb6cf36bbb6498b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000570', 'Luján, Ben Ray', '', '', 'Democratic', 'New Mexico', 'Senate', 0, 'https://www.congress.gov/img/member/l000570_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001089', 'Hawley, Josh', '', '', 'Republican', 'Missouri', 'Senate', 0, 'https://www.congress.gov/img/member/h001089_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000800', 'Welch, Peter', '', '', 'Democratic', 'Vermont', 'Senate', 0, 'https://www.congress.gov/img/member/fd3cb364b8bf93c25834cff750637802_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001242', 'Moreno, Bernie', '', '', 'Republican', 'Ohio', 'Senate', 0, 'https://www.congress.gov/img/member/67c8694e6159152e59828afb_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001229', 'McIver, LaMonica', '', '', 'Democratic', 'New Jersey', 'House', 10, 'https://www.congress.gov/img/member/681dfed94fc893ce843e24b8_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001085', 'Houlahan, Chrissy', '', '', 'Democratic', 'Pennsylvania', 'House', 6, 'https://www.congress.gov/img/member/681bc0e6b763f94d6e471f50_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001244', 'Moody, Ashley', '', '', 'Republican', 'Florida', 'Senate', 0, '', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001226', 'Menendez, Robert', '', '', 'Democratic', 'New Jersey', 'House', 8, 'https://www.congress.gov/img/member/681231f6246d1b6bd8d9f6b4_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000477', 'Foushee, Valerie P.', '', '', 'Democratic', 'North Carolina', 'House', 4, 'https://www.congress.gov/img/member/68122e57246d1b6bd8d9f6ab_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000488', 'Thanedar, Shri', '', '', 'Democratic', 'Michigan', 'House', 13, 'https://www.congress.gov/img/member/68122bf2246d1b6bd8d9f6a2_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000622', 'Patronis, Jimmy', '', '', 'Republican', 'Florida', 'House', 1, 'https://www.congress.gov/img/member/67efdb991b05a5a598f7fde9_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000484', 'Fine, Randy', '', '', 'Republican', 'Florida', 'House', 6, 'https://www.congress.gov/img/member/67efda8c1b05a5a598f7fde0_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001221', 'Scholten, Hillary J.', '', '', 'Democratic', 'Michigan', 'House', 3, 'https://www.congress.gov/img/member/s001221_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000299', 'Johnson, Mike', '', '', 'Republican', 'Louisiana', 'House', 4, 'https://www.congress.gov/img/member/67ffcb2af22eaf56065817c4_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000621', 'Randall, Emily', '', '', 'Democratic', 'Washington', 'House', 6, 'https://www.congress.gov/img/member/67745dcf0b34857ecc909173_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001235', 'Moore, Riley M.', '', '', 'Republican', 'West Virginia', 'House', 2, 'https://www.congress.gov/img/member/677449fd0b34857ecc909131_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001322', 'Baumgartner, Michael', '', '', 'Republican', 'Washington', 'House', 5, 'https://www.congress.gov/img/member/6774212e0b34857ecc90903a_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000829', 'Wied, Tony', '', '', 'Republican', 'Wisconsin', 'House', 8, 'https://www.congress.gov/img/member/6734b6724c72e343a6aff9e6_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000135', 'Van Orden, Derrick', '', '', 'Republican', 'Wisconsin', 'House', 3, 'https://www.congress.gov/img/member/v000135_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000600', 'Perez, Marie Gluesenkamp', '', '', 'Democratic', 'Washington', 'House', 3, 'https://www.congress.gov/img/member/g000600_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001096', 'Hageman, Harriet M.', '', '', 'Republican', 'Wyoming', 'House', 0, 'https://www.congress.gov/img/member/h001096_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001318', 'Balint, Becca', '', '', 'Democratic', 'Vermont', 'House', 0, 'https://www.congress.gov/img/member/b001318_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001159', 'Strickland, Marilyn', '', '', 'Democratic', 'Washington', 'House', 10, 'https://www.congress.gov/img/member/s001159_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000471', 'Fitzgerald, Scott', '', '', 'Republican', 'Wisconsin', 'House', 5, 'https://www.congress.gov/img/member/f000471_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000165', 'Tiffany, Thomas P.', '', '', 'Republican', 'Wisconsin', 'House', 7, 'https://www.congress.gov/img/member/t000165_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001205', 'Miller, Carol D.', '', '', 'Republican', 'West Virginia', 'House', 1, 'https://www.congress.gov/img/member/m001205_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001213', 'Steil, Bryan', '', '', 'Republican', 'Wisconsin', 'House', 1, 'https://www.congress.gov/img/member/s001213_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001216', 'Schrier, Kim', '', '', 'Democratic', 'Washington', 'House', 8, 'https://www.congress.gov/img/member/s001216_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000298', 'Jayapal, Pramila', '', '', 'Democratic', 'Washington', 'House', 7, 'https://www.congress.gov/img/member/116_rp_wa_7_jayapal_pramila_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000576', 'Grothman, Glenn', '', '', 'Republican', 'Wisconsin', 'House', 6, 'https://www.congress.gov/img/member/116_rp_wi_6_grothman_glenn_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000189', 'Newhouse, Dan', '', '', 'Republican', 'Washington', 'House', 4, 'https://www.congress.gov/img/member/116_rp_wa_4_newhouse_dan_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000610', 'Plaskett, Stacey E.', '', '', 'Democratic', 'Virgin Islands', 'House', 0, 'https://www.congress.gov/img/member/116_dg_vi_plaskett_stacey_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000607', 'Pocan, Mark', '', '', 'Democratic', 'Wisconsin', 'House', 2, 'https://www.congress.gov/img/member/p000607_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000617', 'DelBene, Suzan K.', '', '', 'Democratic', 'Washington', 'House', 1, 'https://www.congress.gov/img/member/d000617_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000510', 'Smith, Adam', '', '', 'Democratic', 'Washington', 'House', 9, 'https://www.congress.gov/img/member/116_rp_wa_9_smith_adam_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001160', 'Moore, Gwen', '', '', 'Democratic', 'Wisconsin', 'House', 4, 'https://www.congress.gov/img/member/116_rp_wi_4_moore_gwen_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000560', 'Larsen, Rick', '', '', 'Democratic', 'Washington', 'House', 2, 'https://www.congress.gov/img/member/116_rp_wa_2_larsen_rick_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000138', 'Vindman, Eugene Simon', '', '', 'Democratic', 'Virginia', 'House', 7, 'https://www.congress.gov/img/member/6774617a0b34857ecc9091b5_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001230', 'Subramanyam, Suhas', '', '', 'Democratic', 'Virginia', 'House', 10, 'https://www.congress.gov/img/member/6797be8bc75fbc6f720e476a_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001239', 'McGuire, John J.', '', '', 'Republican', 'Virginia', 'House', 5, 'https://www.congress.gov/img/member/67744ba20b34857ecc909149_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000403', 'Kennedy, Mike', '', '', 'Republican', 'Utah', 'House', 3, 'https://www.congress.gov/img/member/67742e7c0b34857ecc9090f5_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000310', 'Johnson, Julie', '', '', 'Democratic', 'Texas', 'House', 32, 'https://www.congress.gov/img/member/67742df60b34857ecc9090e9_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000603', 'Gill, Brandon', '', '', 'Republican', 'Texas', 'House', 26, 'https://www.congress.gov/img/member/677428ac0b34857ecc9090b3_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001228', 'Maloy, Celeste', '', '', 'Republican', 'Utah', 'House', 2, 'https://www.congress.gov/img/member/m001228_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001227', 'McClellan, Jennifer L.', '', '', 'Democratic', 'Virginia', 'House', 4, 'https://www.congress.gov/img/member/m001227_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000399', 'Kiggans, Jennifer A.', '', '', 'Republican', 'Virginia', 'House', 2, 'https://www.congress.gov/img/member/66b0ce45b0288a917d98f619_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001095', 'Hunt, Wesley', '', '', 'Republican', 'Texas', 'House', 38, 'https://www.congress.gov/img/member/h001095_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001130', 'Crockett, Jasmine', '', '', 'Democratic', 'Texas', 'House', 30, 'https://www.congress.gov/img/member/c001130_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001131', 'Casar, Greg', '', '', 'Democratic', 'Texas', 'House', 35, 'https://www.congress.gov/img/member/c001131_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000134', 'Van Duyne, Beth', '', '', 'Republican', 'Texas', 'House', 24, 'https://www.congress.gov/img/member/677461060b34857ecc9091af_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000086', 'Owens, Burgess', '', '', 'Republican', 'Utah', 'House', 4, 'https://www.congress.gov/img/member/o000086_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000026', 'Nehls, Troy E.', '', '', 'Republican', 'Texas', 'House', 22, 'https://www.congress.gov/img/member/n000026_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001213', 'Moore, Blake D.', '', '', 'Republican', 'Utah', 'House', 1, 'https://www.congress.gov/img/member/m001213_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000594', 'Gonzales, Tony', '', '', 'Republican', 'Texas', 'House', 23, 'https://www.congress.gov/img/member/g000594_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001118', 'Cline, Ben', '', '', 'Republican', 'Virginia', 'House', 6, 'https://www.congress.gov/img/member/c001118_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000587', 'Garcia, Sylvia R.', '', '', 'Democratic', 'Texas', 'House', 29, 'https://www.congress.gov/img/member/g000587_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000614', 'Roy, Chip', '', '', 'Republican', 'Texas', 'House', 21, 'https://www.congress.gov/img/member/r000614_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001115', 'Cloud, Michael', '', '', 'Republican', 'Texas', 'House', 27, 'https://www.congress.gov/img/member/115_rp_tx_27_cloud_michael_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000581', 'Gonzalez, Vicente', '', '', 'Democratic', 'Texas', 'House', 34, 'https://www.congress.gov/img/member/115_rp_tx_15_gonzalez_vicente_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001292', 'Beyer, Donald S.', '', '', 'Democratic', 'Virginia', 'House', 8, 'https://www.congress.gov/img/member/b001292_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001291', 'Babin, Brian', '', '', 'Republican', 'Texas', 'House', 36, 'https://www.congress.gov/img/member/b001291_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000131', 'Veasey, Marc A.', '', '', 'Democratic', 'Texas', 'House', 33, 'https://www.congress.gov/img/member/v000131_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000816', 'Williams, Roger', '', '', 'Republican', 'Texas', 'House', 25, 'https://www.congress.gov/img/member/w000816_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000804', 'Wittman, Robert J.', '', '', 'Republican', 'Virginia', 'House', 1, 'https://www.congress.gov/img/member/w000804_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000568', 'Griffith, H. Morgan', '', '', 'Republican', 'Virginia', 'House', 9, 'https://www.congress.gov/img/member/68094df86c2e6631263de737_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000185', 'Scott, Robert C. "Bobby"', '', '', 'Democratic', 'Virginia', 'House', 3, 'https://www.congress.gov/img/member/s000185_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001063', 'Cuellar, Henry', '', '', 'Democratic', 'Texas', 'House', 28, 'https://www.congress.gov/img/member/116_rp_tx_28_cuellar_henry_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001051', 'Carter, John R.', '', '', 'Republican', 'Texas', 'House', 31, 'https://www.congress.gov/img/member/c001051_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000399', 'Doggett, Lloyd', '', '', 'Democratic', 'Texas', 'House', 37, 'https://www.congress.gov/img/member/d000399_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000601', 'Goldman, Craig A.', '', '', 'Republican', 'Texas', 'House', 12, 'https://www.congress.gov/img/member/6774277d0b34857ecc9090a7_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001325', 'Biggs, Sheri', '', '', 'Republican', 'South Carolina', 'House', 3, 'https://www.congress.gov/img/member/677422990b34857ecc909052_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001224', 'Self, Keith', '', '', 'Republican', 'Texas', 'House', 3, 'https://www.congress.gov/img/member/s001224_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000175', 'Ogles, Andrew', '', '', 'Republican', 'Tennessee', 'House', 5, 'https://www.congress.gov/img/member/o000175_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001224', 'Moran, Nathaniel', '', '', 'Republican', 'Texas', 'House', 1, 'https://www.congress.gov/img/member/680008c5f22eaf56065817f4_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000603', 'Luttrell, Morgan', '', '', 'Republican', 'Texas', 'House', 8, 'https://www.congress.gov/img/member/l000603_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000478', 'Fry, Russell', '', '', 'Republican', 'South Carolina', 'House', 7, 'https://www.congress.gov/img/member/f000478_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000594', 'De La Cruz, Monica', '', '', 'Republican', 'Texas', 'House', 15, 'https://www.congress.gov/img/member/66d9fd54f440bf1dc174fbf6_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000071', 'Ellzey, Jake', '', '', 'Republican', 'Texas', 'House', 6, 'https://www.congress.gov/img/member/e000071_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000048', 'Pfluger, August', '', '', 'Republican', 'Texas', 'House', 11, 'https://www.congress.gov/img/member/p000048_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000304', 'Jackson, Ronny', '', '', 'Republican', 'Texas', 'House', 13, 'https://www.congress.gov/img/member/j000304_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001086', 'Harshbarger, Diana', '', '', 'Republican', 'Tennessee', 'House', 1, 'https://www.congress.gov/img/member/h001086_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000246', 'Fallon, Pat', '', '', 'Republican', 'Texas', 'House', 4, 'https://www.congress.gov/img/member/f000246_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000299', 'Escobar, Veronica', '', '', 'Democratic', 'Texas', 'House', 16, 'https://www.congress.gov/img/member/e000299_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000468', 'Fletcher, Lizzie', '', '', 'Democratic', 'Texas', 'House', 7, 'https://www.congress.gov/img/member/67813f931f9ad6ea6fb1eb6f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000589', 'Gooden, Lance', '', '', 'Republican', 'Texas', 'House', 5, 'https://www.congress.gov/img/member/g000589_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001120', 'Crenshaw, Dan', '', '', 'Republican', 'Texas', 'House', 2, 'https://www.congress.gov/img/member/c001120_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000590', 'Green, Mark E.', '', '', 'Republican', 'Tennessee', 'House', 7, 'https://www.congress.gov/img/member/g000590_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000612', 'Rose, John W.', '', '', 'Republican', 'Tennessee', 'House', 6, 'https://www.congress.gov/img/member/r000612_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001309', 'Burchett, Tim', '', '', 'Republican', 'Tennessee', 'House', 2, 'https://www.congress.gov/img/member/b001309_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000301', 'Johnson, Dusty', '', '', 'Republican', 'South Dakota', 'House', 0, 'https://www.congress.gov/img/member/j000301_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000480', 'Timmons, William R.', '', '', 'Republican', 'South Carolina', 'House', 4, 'https://www.congress.gov/img/member/t000480_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000190', 'Norman, Ralph', '', '', 'Republican', 'South Carolina', 'House', 5, 'https://www.congress.gov/img/member/n000190_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000375', 'Arrington, Jodey C.', '', '', 'Republican', 'Texas', 'House', 19, 'https://www.congress.gov/img/member/115_rp_tx_19_arrington_jodey_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000392', 'Kustoff, David', '', '', 'Republican', 'Tennessee', 'House', 8, 'https://www.congress.gov/img/member/116_rp_tn_8_kustoff_david_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001091', 'Castro, Joaquin', '', '', 'Democratic', 'Texas', 'House', 20, 'https://www.congress.gov/img/member/c001091_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000814', 'Weber, Randy K. Sr.', '', '', 'Republican', 'Texas', 'House', 14, 'https://www.congress.gov/img/member/w000814_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000616', 'DesJarlais, Scott', '', '', 'Republican', 'Tennessee', 'House', 4, 'https://www.congress.gov/img/member/d000616_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000459', 'Fleischmann, Charles J. "Chuck"', '', '', 'Republican', 'Tennessee', 'House', 3, 'https://www.congress.gov/img/member/f000459_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001068', 'Cohen, Steve', '', '', 'Democratic', 'Tennessee', 'House', 9, 'https://www.congress.gov/img/member/c001068_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000250', 'Sessions, Pete', '', '', 'Republican', 'Texas', 'House', 17, 'https://www.congress.gov/img/member/115_rp_tx_32_sessions_pete_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001157', 'McCaul, Michael T.', '', '', 'Republican', 'Texas', 'House', 10, 'https://www.congress.gov/img/member/116_rp_tx_10_mccaul_michael_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000553', 'Green, Al', '', '', 'Democratic', 'Texas', 'House', 9, 'https://www.congress.gov/img/member/116_rp_tx_9_green_al_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C000537', 'Clyburn, James E.', '', '', 'Democratic', 'South Carolina', 'House', 6, 'https://www.congress.gov/img/member/c000537_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001230', 'Mackenzie, Ryan', '', '', 'Republican', 'Pennsylvania', 'House', 7, 'https://www.congress.gov/img/member/677430a40b34857ecc909113_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001103', 'Hernández, Pablo Jose', '', '', 'Democratic', 'Puerto Rico', 'House', 0, 'https://www.congress.gov/img/member/67742d980b34857ecc9090e3_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000635', 'Dexter, Maxine', '', '', 'Democratic', 'Oregon', 'House', 3, 'https://www.congress.gov/img/member/677425260b34857ecc90907d_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001327', 'Bresnahan, Robert P.', '', '', 'Republican', 'Pennsylvania', 'House', 8, 'https://www.congress.gov/img/member/6774236f0b34857ecc90905f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001326', 'Bynum, Janelle S.', '', '', 'Democratic', 'Oregon', 'House', 5, 'https://www.congress.gov/img/member/677423150b34857ecc909059_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000380', 'Amo, Gabe', '', '', 'Democratic', 'Rhode Island', 'House', 1, 'https://www.congress.gov/img/member/669ace45fa2fb0d731226768_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001226', 'Salinas, Andrea', '', '', 'Democratic', 'Oregon', 'House', 6, 'https://www.congress.gov/img/member/s001226_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001223', 'Magaziner, Seth', '', '', 'Democratic', 'Rhode Island', 'House', 2, 'https://www.congress.gov/img/member/m001223_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000602', 'Lee, Summer L.', '', '', 'Democratic', 'Pennsylvania', 'House', 12, 'https://www.congress.gov/img/member/l000602_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001094', 'Hoyle, Val T.', '', '', 'Democratic', 'Oregon', 'House', 4, 'https://www.congress.gov/img/member/h001094_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000530', 'Deluzio, Christopher R.', '', '', 'Democratic', 'Pennsylvania', 'House', 17, 'https://www.congress.gov/img/member/d000530_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001317', 'Brecheen, Josh', '', '', 'Republican', 'Oklahoma', 'House', 2, 'https://www.congress.gov/img/member/b001317_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000194', 'Mace, Nancy', '', '', 'Republican', 'South Carolina', 'House', 1, 'https://www.congress.gov/img/member/m000194_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B000740', 'Bice, Stephanie I.', '', '', 'Republican', 'Oklahoma', 'House', 5, 'https://www.congress.gov/img/member/b000740_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B000668', 'Bentz, Cliff', '', '', 'Republican', 'Oregon', 'House', 2, 'https://www.congress.gov/img/member/b000668_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000610', 'Reschenthaler, Guy', '', '', 'Republican', 'Pennsylvania', 'House', 14, 'https://www.congress.gov/img/member/r000610_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000302', 'Joyce, John', '', '', 'Republican', 'Pennsylvania', 'House', 13, 'https://www.congress.gov/img/member/j000302_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001204', 'Meuser, Daniel', '', '', 'Republican', 'Pennsylvania', 'House', 9, 'https://www.congress.gov/img/member/6776ebbf4f8a93753830ca7d_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000631', 'Dean, Madeleine', '', '', 'Democratic', 'Pennsylvania', 'House', 4, 'https://www.congress.gov/img/member/d000631_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001082', 'Hern, Kevin', '', '', 'Republican', 'Oklahoma', 'House', 1, 'https://www.congress.gov/img/member/h001082_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001205', 'Scanlon, Mary Gay', '', '', 'Democratic', 'Pennsylvania', 'House', 5, 'https://www.congress.gov/img/member/116_rp_pa_5_scanlon_mary_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001199', 'Smucker, Lloyd', '', '', 'Republican', 'Pennsylvania', 'House', 11, 'https://www.congress.gov/img/member/s001199_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000466', 'Fitzpatrick, Brian K.', '', '', 'Republican', 'Pennsylvania', 'House', 1, 'https://www.congress.gov/img/member/116_rp_pa_1_fitzpatrick_brian_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000296', 'Evans, Dwight', '', '', 'Democratic', 'Pennsylvania', 'House', 3, 'https://www.congress.gov/img/member/115_rp_pa_2_evans_dwight_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001296', 'Boyle, Brendan F.', '', '', 'Democratic', 'Pennsylvania', 'House', 2, 'https://www.congress.gov/img/member/115_rp_pa_13_boyle_brendan_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000605', 'Perry, Scott', '', '', 'Republican', 'Pennsylvania', 'House', 10, 'https://www.congress.gov/img/member/677ec7d3514c773869b6b915_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001278', 'Bonamici, Suzanne', '', '', 'Democratic', 'Oregon', 'House', 1, 'https://www.congress.gov/img/member/b001278_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000376', 'Kelly, Mike', '', '', 'Republican', 'Pennsylvania', 'House', 16, 'https://www.congress.gov/img/member/k000376_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000467', 'Thompson, Glenn', '', '', 'Republican', 'Pennsylvania', 'House', 15, 'https://www.congress.gov/img/member/115_rp_pa_5_thompson_glenn_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000491', 'Lucas, Frank D.', '', '', 'Republican', 'Oklahoma', 'House', 3, 'https://www.congress.gov/img/member/116_rp_ok_3_lucas_frank_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001053', 'Cole, Tom', '', '', 'Republican', 'Oklahoma', 'House', 4, 'https://www.congress.gov/img/member/c001053_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000795', 'Wilson, Joe', '', '', 'Republican', 'South Carolina', 'House', 2, 'https://www.congress.gov/img/member/116_rp_sc_2_wilson_joe_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000490', 'Taylor, David J.', '', '', 'Republican', 'Ohio', 'House', 2, 'https://www.congress.gov/img/member/677460190b34857ecc9091a3_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000622', 'Riley, Josh', '', '', 'Democratic', 'New York', 'House', 19, 'https://www.congress.gov/img/member/67745e360b34857ecc909179_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001231', 'Mannion, John W.', '', '', 'Democratic', 'New York', 'House', 22, 'https://www.congress.gov/img/member/677446860b34857ecc909119_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000606', 'Latimer, George', '', '', 'Democratic', 'New York', 'House', 16, 'https://www.congress.gov/img/member/6774301b0b34857ecc909107_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000619', 'Rulli, Michael A.', '', '', 'Republican', 'Ohio', 'House', 6, 'https://www.congress.gov/img/member/668e9425658443009a697c95_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000402', 'Kennedy, Timothy M.', '', '', 'Democratic', 'New York', 'House', 26, 'https://www.congress.gov/img/member/668e9306658443009a697c8c_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001223', 'Sykes, Emilia Strong', '', '', 'Democratic', 'Ohio', 'House', 13, 'https://www.congress.gov/img/member/s001223_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001222', 'Miller, Max L.', '', '', 'Republican', 'Ohio', 'House', 7, 'https://www.congress.gov/img/member/680908fb6c2e6631263de71f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000599', 'Lawler, Michael', '', '', 'Republican', 'New York', 'House', 17, 'https://www.congress.gov/img/member/l000599_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000600', 'Langworthy, Nicholas A.', '', '', 'Republican', 'New York', 'House', 23, 'https://www.congress.gov/img/member/680901e76c2e6631263de716_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000601', 'Landsman, Greg', '', '', 'Democratic', 'Ohio', 'House', 1, 'https://www.congress.gov/img/member/l000601_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000579', 'Ryan, Patrick', '', '', 'Democratic', 'New York', 'House', 18, 'https://www.congress.gov/img/member/r000579_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001126', 'Carey, Mike', '', '', 'Republican', 'Ohio', 'House', 15, 'https://www.congress.gov/img/member/c001126_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001313', 'Brown, Shontel M.', '', '', 'Democratic', 'Ohio', 'House', 11, 'https://www.congress.gov/img/member/b001313_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000486', 'Torres, Ritchie', '', '', 'Democratic', 'New York', 'House', 15, 'https://www.congress.gov/img/member/t000486_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000172', 'Ocasio-Cortez, Alexandria', '', '', 'Democratic', 'New York', 'House', 14, 'https://www.congress.gov/img/member/o000172_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001206', 'Morelle, Joseph D.', '', '', 'Democratic', 'New York', 'House', 25, 'https://www.congress.gov/img/member/67ffc962f22eaf56065817bb_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001306', 'Balderson, Troy', '', '', 'Republican', 'Ohio', 'House', 12, 'https://www.congress.gov/img/member/116_rp_oh_12_balderson_troy_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000478', 'Tenney, Claudia', '', '', 'Republican', 'New York', 'House', 24, 'https://www.congress.gov/img/member/t000478_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000297', 'Espaillat, Adriano', '', '', 'Democratic', 'New York', 'House', 13, 'https://www.congress.gov/img/member/e000297_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000626', 'Davidson, Warren', '', '', 'Republican', 'Ohio', 'House', 8, 'https://www.congress.gov/img/member/115_rp_oh_8_davidson_warren_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001196', 'Stefanik, Elise M.', '', '', 'Republican', 'New York', 'House', 21, 'https://www.congress.gov/img/member/s001196_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000295', 'Joyce, David P.', '', '', 'Republican', 'Ohio', 'House', 14, 'https://www.congress.gov/img/member/j000295_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001281', 'Beatty, Joyce', '', '', 'Democratic', 'Ohio', 'House', 3, 'https://www.congress.gov/img/member/b001281_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000566', 'Latta, Robert E.', '', '', 'Republican', 'Ohio', 'House', 5, 'https://www.congress.gov/img/member/l000566_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000289', 'Jordan, Jim', '', '', 'Republican', 'Ohio', 'House', 4, 'https://www.congress.gov/img/member/j000289_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000469', 'Tonko, Paul', '', '', 'Democratic', 'New York', 'House', 20, 'https://www.congress.gov/img/member/t000469_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000002', 'Nadler, Jerrold', '', '', 'Democratic', 'New York', 'House', 12, 'https://www.congress.gov/img/member/n000002_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000463', 'Turner, Michael R.', '', '', 'Republican', 'Ohio', 'House', 10, 'https://www.congress.gov/img/member/68014c674e51529406f18e56_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000009', 'Kaptur, Marcy', '', '', 'Democratic', 'Ohio', 'House', 9, 'https://www.congress.gov/img/member/k000009_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000621', 'Pou, Nellie', '', '', 'Democratic', 'New Jersey', 'House', 9, 'https://www.congress.gov/img/member/67745d3b0b34857ecc909167_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000604', 'Goodlander, Maggie', '', '', 'Democratic', 'New Hampshire', 'House', 2, 'https://www.congress.gov/img/member/678ff62d66bf616cf1a7ce13_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000602', 'Gillen, Laura', '', '', 'Democratic', 'New York', 'House', 4, 'https://www.congress.gov/img/member/677427de0b34857ecc9090ad_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001136', 'Conaway, Herbert C.', '', '', 'Democratic', 'New Jersey', 'House', 3, 'https://www.congress.gov/img/member/6774243a0b34857ecc90906b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000136', 'Vasquez, Gabe', '', '', 'Democratic', 'New Mexico', 'House', 2, 'https://www.congress.gov/img/member/v000136_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000598', 'LaLota, Nick', '', '', 'Republican', 'New York', 'House', 1, 'https://www.congress.gov/img/member/l000598_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000398', 'Kean, Thomas H.', '', '', 'Republican', 'New Jersey', 'House', 7, 'https://www.congress.gov/img/member/k000398_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000599', 'Goldman, Daniel S.', '', '', 'Democratic', 'New York', 'House', 10, 'https://www.congress.gov/img/member/g000599_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001218', 'Stansbury, Melanie A.', '', '', 'Democratic', 'New Mexico', 'House', 1, 'https://www.congress.gov/img/member/s001218_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000317', 'Malliotakis, Nicole', '', '', 'Republican', 'New York', 'House', 11, 'https://www.congress.gov/img/member/m000317_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000273', 'Leger Fernandez, Teresa', '', '', 'Democratic', 'New Mexico', 'House', 3, 'https://www.congress.gov/img/member/l000273_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000597', 'Garbarino, Andrew R.', '', '', 'Republican', 'New York', 'House', 2, 'https://www.congress.gov/img/member/g000597_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000590', 'Lee, Susie', '', '', 'Democratic', 'Nevada', 'House', 3, 'https://www.congress.gov/img/member/l000590_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001207', 'Sherrill, Mikie', '', '', 'Democratic', 'New Jersey', 'House', 11, 'https://www.congress.gov/img/member/s001207_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000133', 'Van Drew, Jefferson', '', '', 'Republican', 'New Jersey', 'House', 2, 'https://www.congress.gov/img/member/67c0c39d53fe81a4b3c0cac1_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000614', 'Pappas, Chris', '', '', 'Democratic', 'New Hampshire', 'House', 1, 'https://www.congress.gov/img/member/p000614_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001201', 'Suozzi, Thomas R.', '', '', 'Democratic', 'New York', 'House', 3, 'https://www.congress.gov/img/member/116_rp_ny_3_suozzi_thomas_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000583', 'Gottheimer, Josh', '', '', 'Democratic', 'New Jersey', 'House', 5, 'https://www.congress.gov/img/member/115_rp_nj_5_gottheimer_josh_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000822', 'Watson Coleman, Bonnie', '', '', 'Democratic', 'New Jersey', 'House', 12, 'https://www.congress.gov/img/member/w000822_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000188', 'Norcross, Donald', '', '', 'Democratic', 'New Jersey', 'House', 1, 'https://www.congress.gov/img/member/n000188_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000294', 'Jeffries, Hakeem S.', '', '', 'Democratic', 'New York', 'House', 8, 'https://www.congress.gov/img/member/j000294_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001188', 'Meng, Grace', '', '', 'Democratic', 'New York', 'House', 6, 'https://www.congress.gov/img/member/m001188_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001066', 'Horsford, Steven', '', '', 'Democratic', 'Nevada', 'House', 4, 'https://www.congress.gov/img/member/h001066_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000369', 'Amodei, Mark E.', '', '', 'Republican', 'Nevada', 'House', 2, 'https://www.congress.gov/img/member/a000369_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001067', 'Clarke, Yvette D.', '', '', 'Democratic', 'New York', 'House', 9, 'https://www.congress.gov/img/member/674dfc6b5c48ff736e6e1762_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000468', 'Titus, Dina', '', '', 'Democratic', 'Nevada', 'House', 1, 'https://www.congress.gov/img/member/6809296b6c2e6631263de728_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000034', 'Pallone, Frank', '', '', 'Democratic', 'New Jersey', 'House', 6, 'https://www.congress.gov/img/member/p000034_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001137', 'Meeks, Gregory W.', '', '', 'Democratic', 'New York', 'House', 5, 'https://www.congress.gov/img/member/m001137_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000081', 'Velázquez, Nydia M.', '', '', 'Democratic', 'New York', 'House', 7, 'https://www.congress.gov/img/member/v000081_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000522', 'Smith, Christopher H.', '', '', 'Republican', 'New Jersey', 'House', 4, 'https://www.congress.gov/img/member/s000522_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001240', 'McDowell, Addison P.', '', '', 'Republican', 'North Carolina', 'House', 6, 'https://www.congress.gov/img/member/67744e930b34857ecc90914f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001236', 'Moore, Tim', '', '', 'Republican', 'North Carolina', 'House', 14, 'https://www.congress.gov/img/member/67744a540b34857ecc909137_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000405', 'Knott, Brad', '', '', 'Republican', 'North Carolina', 'House', 13, 'https://www.congress.gov/img/member/67742fc60b34857ecc909101_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001102', 'Harris, Mark', '', '', 'Republican', 'North Carolina', 'House', 8, 'https://www.congress.gov/img/member/67742d1b0b34857ecc9090dd_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001101', 'Harrigan, Pat', '', '', 'Republican', 'North Carolina', 'House', 10, 'https://www.congress.gov/img/member/67742ca40b34857ecc9090d7_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000482', 'Fedorchak, Julie', '', '', 'Republican', 'North Dakota', 'House', 0, 'https://www.congress.gov/img/member/677426c20b34857ecc90909b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000246', 'Edwards, Chuck', '', '', 'Republican', 'North Carolina', 'House', 11, 'https://www.congress.gov/img/member/e000246_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000474', 'Flood, Mike', '', '', 'Republican', 'Nebraska', 'House', 1, 'https://www.congress.gov/img/member/67b4de4a61bd80d04553b0a5_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001298', 'Bacon, Don', '', '', 'Republican', 'Nebraska', 'House', 2, 'https://www.congress.gov/img/member/115_rp_ne_2_bacon_don_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000603', 'Rouzer, David', '', '', 'Republican', 'North Carolina', 'House', 7, 'https://www.congress.gov/img/member/r000603_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000370', 'Adams, Alma S.', '', '', 'Democratic', 'North Carolina', 'House', 12, 'https://www.congress.gov/img/member/a000370_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001067', 'Hudson, Richard', '', '', 'Republican', 'North Carolina', 'House', 9, 'https://www.congress.gov/img/member/h001067_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001172', 'Smith, Adrian', '', '', 'Republican', 'Nebraska', 'House', 3, 'https://www.congress.gov/img/member/s001172_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000450', 'Foxx, Virginia', '', '', 'Republican', 'North Carolina', 'House', 5, 'https://www.congress.gov/img/member/116_rp_nc_5_foxx_virginia_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000177', 'Onder, Robert F.', '', '', 'Republican', 'Missouri', 'House', 3, 'https://www.congress.gov/img/member/67744f970b34857ecc909161_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001234', 'Morrison, Kelly', '', '', 'Democratic', 'Minnesota', 'House', 3, 'https://www.congress.gov/img/member/677449a70b34857ecc90912b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000404', 'King-Hinds, Kimberlyn', '', '', 'Republican', 'Northern Mariana Islands', 'House', 0, 'https://www.congress.gov/img/member/67742f0a0b34857ecc9090fb_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000634', 'Downing, Troy', '', '', 'Republican', 'Montana', 'House', 2, 'https://www.congress.gov/img/member/677424da0b34857ecc909077_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001324', 'Bell, Wesley', '', '', 'Democratic', 'Missouri', 'House', 1, 'https://www.congress.gov/img/member/677422240b34857ecc90904a_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000307', 'James, John', '', '', 'Republican', 'Michigan', 'House', 10, 'https://www.congress.gov/img/member/j000307_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000235', 'Ezell, Mike', '', '', 'Republican', 'Mississippi', 'House', 4, 'https://www.congress.gov/img/member/e000235_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000230', 'Davis, Donald G.', '', '', 'Democratic', 'North Carolina', 'House', 1, 'https://www.congress.gov/img/member/d000230_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001316', 'Burlison, Eric', '', '', 'Republican', 'Missouri', 'House', 7, 'https://www.congress.gov/img/member/b001316_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000379', 'Alford, Mark', '', '', 'Republican', 'Missouri', 'House', 4, 'https://www.congress.gov/img/member/a000379_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000475', 'Finstad, Brad', '', '', 'Republican', 'Minnesota', 'House', 1, 'https://www.congress.gov/img/member/f000475_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000305', 'Ross, Deborah K.', '', '', 'Democratic', 'North Carolina', 'House', 2, 'https://www.congress.gov/img/member/r000305_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000470', 'Fischbach, Michelle', '', '', 'Republican', 'Minnesota', 'House', 7, 'https://www.congress.gov/img/member/f000470_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001210', 'Murphy, Gregory F.', '', '', 'Republican', 'North Carolina', 'House', 3, 'https://www.congress.gov/img/member/m001210_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000591', 'Guest, Michael', '', '', 'Republican', 'Mississippi', 'House', 3, 'https://www.congress.gov/img/member/g000591_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001212', 'Stauber, Pete', '', '', 'Republican', 'Minnesota', 'House', 8, 'https://www.congress.gov/img/member/s001212_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000173', 'Omar, Ilhan', '', '', 'Democratic', 'Minnesota', 'House', 5, 'https://www.congress.gov/img/member/o000173_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001119', 'Craig, Angie', '', '', 'Democratic', 'Minnesota', 'House', 2, 'https://www.congress.gov/img/member/c001119_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000481', 'Tlaib, Rashida', '', '', 'Democratic', 'Michigan', 'House', 12, 'https://www.congress.gov/img/member/t000481_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001215', 'Stevens, Haley M.', '', '', 'Democratic', 'Michigan', 'House', 11, 'https://www.congress.gov/img/member/s001215_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000388', 'Kelly, Trent', '', '', 'Republican', 'Mississippi', 'House', 1, 'https://www.congress.gov/img/member/116_rp_ms_1_kelly_trent_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('Z000018', 'Zinke, Ryan K.', '', '', 'Republican', 'Montana', 'House', 1, 'https://www.congress.gov/img/member/117_rp_mt_1_zinke_ryan_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000294', 'Emmer, Tom', '', '', 'Republican', 'Minnesota', 'House', 6, 'https://www.congress.gov/img/member/e000294_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000812', 'Wagner, Ann', '', '', 'Republican', 'Missouri', 'House', 2, 'https://www.congress.gov/img/member/w000812_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001195', 'Smith, Jason', '', '', 'Republican', 'Missouri', 'House', 8, 'https://www.congress.gov/img/member/s001195_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000193', 'Thompson, Bennie G.', '', '', 'Democratic', 'Mississippi', 'House', 2, 'https://www.congress.gov/img/member/t000193_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001061', 'Cleaver, Emanuel', '', '', 'Democratic', 'Missouri', 'House', 5, 'https://www.congress.gov/img/member/116_rp_mo_5_cleaver_emanuel_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000546', 'Graves, Sam', '', '', 'Republican', 'Missouri', 'House', 6, 'https://www.congress.gov/img/member/g000546_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001143', 'McCollum, Betty', '', '', 'Democratic', 'Minnesota', 'House', 4, 'https://www.congress.gov/img/member/116_rp_mn_4_mccollum_betty_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000176', 'Olszewski, Johnny', '', '', 'Democratic', 'Maryland', 'House', 2, 'https://www.congress.gov/img/member/67744f4e0b34857ecc90915b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001237', 'McDonald Rivet, Kristen', '', '', 'Democratic', 'Michigan', 'House', 8, 'https://www.congress.gov/img/member/67744afa0b34857ecc90913d_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001232', 'McClain Delaney, April', '', '', 'Democratic', 'Maryland', 'House', 6, 'https://www.congress.gov/img/member/677446d80b34857ecc90911f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000301', 'Elfreth, Sarah', '', '', 'Democratic', 'Maryland', 'House', 3, 'https://www.congress.gov/img/member/677425dc0b34857ecc909089_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001321', 'Barrett, Tom', '', '', 'Republican', 'Michigan', 'House', 7, 'https://www.congress.gov/img/member/6774207d0b34857ecc909034_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('I000058', 'Ivey, Glenn', '', '', 'Democratic', 'Maryland', 'House', 4, 'https://www.congress.gov/img/member/i000058_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001136', 'McClain, Lisa C.', '', '', 'Republican', 'Michigan', 'House', 9, 'https://www.congress.gov/img/member/677836d41658e791a384976d_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000148', 'Auchincloss, Jake', '', '', 'Democratic', 'Massachusetts', 'House', 4, 'https://www.congress.gov/img/member/67817e391f9ad6ea6fb1ebda_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000592', 'Golden, Jared F.', '', '', 'Democratic', 'Maine', 'House', 2, 'https://www.congress.gov/img/member/g000592_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000617', 'Pressley, Ayanna', '', '', 'Democratic', 'Massachusetts', 'House', 7, 'https://www.congress.gov/img/member/p000617_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000482', 'Trahan, Lori', '', '', 'Democratic', 'Massachusetts', 'House', 3, 'https://www.congress.gov/img/member/t000482_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001301', 'Bergman, Jack', '', '', 'Republican', 'Michigan', 'House', 1, 'https://www.congress.gov/img/member/b001301_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000606', 'Raskin, Jamie', '', '', 'Democratic', 'Maryland', 'House', 8, 'https://www.congress.gov/img/member/r000606_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000624', 'Dingell, Debbie', '', '', 'Democratic', 'Michigan', 'House', 6, 'https://www.congress.gov/img/member/d000624_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001194', 'Moolenaar, John R.', '', '', 'Republican', 'Michigan', 'House', 2, 'https://www.congress.gov/img/member/m001194_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001196', 'Moulton, Seth', '', '', 'Democratic', 'Massachusetts', 'House', 6, 'https://www.congress.gov/img/member/m001196_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001101', 'Clark, Katherine M.', '', '', 'Democratic', 'Massachusetts', 'House', 5, 'https://www.congress.gov/img/member/c001101_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001058', 'Huizenga, Bill', '', '', 'Republican', 'Michigan', 'House', 4, 'https://www.congress.gov/img/member/h001058_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001052', 'Harris, Andy', '', '', 'Republican', 'Maryland', 'House', 1, 'https://www.congress.gov/img/member/117_rp_md_1_harris_andy_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000375', 'Keating, William R.', '', '', 'Democratic', 'Massachusetts', 'House', 9, 'https://www.congress.gov/img/member/k000375_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000798', 'Walberg, Tim', '', '', 'Republican', 'Michigan', 'House', 5, 'https://www.congress.gov/img/member/w000798_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000597', 'Pingree, Chellie', '', '', 'Democratic', 'Maine', 'House', 1, 'https://www.congress.gov/img/member/p000597_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000312', 'McGovern, James P.', '', '', 'Democratic', 'Massachusetts', 'House', 2, 'https://www.congress.gov/img/member/117_rp_ma_2_mcgovern_james_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000015', 'Neal, Richard E.', '', '', 'Democratic', 'Massachusetts', 'House', 1, 'https://www.congress.gov/img/member/n000015_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000687', 'Mfume, Kweisi', '', '', 'Democratic', 'Maryland', 'House', 7, 'https://www.congress.gov/img/member/m000687_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000562', 'Lynch, Stephen F.', '', '', 'Democratic', 'Massachusetts', 'House', 8, 'https://www.congress.gov/img/member/l000562_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000110', 'Fields, Cleo', '', '', 'Democratic', 'Louisiana', 'House', 6, 'https://www.congress.gov/img/member/677426250b34857ecc90908f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H000874', 'Hoyer, Steny H.', '', '', 'Democratic', 'Maryland', 'House', 5, 'https://www.congress.gov/img/member/116_rp_md_5_hoyer_steny_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001229', 'Shreve, Jefferson', '', '', 'Republican', 'Indiana', 'House', 6, 'https://www.congress.gov/img/member/67745f0e0b34857ecc90918b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001228', 'Schmidt, Derek', '', '', 'Republican', 'Kansas', 'House', 2, 'https://www.congress.gov/img/member/67745ec50b34857ecc909185_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001233', 'Messmer, Mark B.', '', '', 'Republican', 'Indiana', 'House', 8, 'https://www.congress.gov/img/member/677448630b34857ecc909125_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001225', 'Sorensen, Eric', '', '', 'Democratic', 'Illinois', 'House', 17, 'https://www.congress.gov/img/member/s001225_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001220', 'McGarvey, Morgan', '', '', 'Democratic', 'Kentucky', 'House', 3, 'https://www.congress.gov/img/member/m001220_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001093', 'Houchin, Erin', '', '', 'Republican', 'Indiana', 'House', 9, 'https://www.congress.gov/img/member/h001093_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001315', 'Budzinski, Nikki', '', '', 'Democratic', 'Illinois', 'House', 13, 'https://www.congress.gov/img/member/b001315_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('Y000067', 'Yakym, Rudy', '', '', 'Republican', 'Indiana', 'House', 2, 'https://www.congress.gov/img/member/y000067_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001125', 'Carter, Troy A.', '', '', 'Democratic', 'Louisiana', 'House', 2, 'https://www.congress.gov/img/member/c001125_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000595', 'Letlow, Julia', '', '', 'Republican', 'Louisiana', 'House', 5, 'https://www.congress.gov/img/member/l000595_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000929', 'Spartz, Victoria', '', '', 'Republican', 'Indiana', 'House', 5, 'https://www.congress.gov/img/member/s000929_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001214', 'Mrvan, Frank J.', '', '', 'Democratic', 'Indiana', 'House', 1, 'https://www.congress.gov/img/member/m001214_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001211', 'Miller, Mary E.', '', '', 'Republican', 'Illinois', 'House', 15, 'https://www.congress.gov/img/member/m001211_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000871', 'Mann, Tracey', '', '', 'Republican', 'Kansas', 'House', 1, 'https://www.congress.gov/img/member/m000871_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000629', 'Davids, Sharice', '', '', 'Democratic', 'Kansas', 'House', 3, 'https://www.congress.gov/img/member/d000629_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001307', 'Baird, James R.', '', '', 'Republican', 'Indiana', 'House', 4, 'https://www.congress.gov/img/member/b001307_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('U000040', 'Underwood, Lauren', '', '', 'Democratic', 'Illinois', 'House', 14, 'https://www.congress.gov/img/member/u000040_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000298', 'Estes, Ron', '', '', 'Republican', 'Kansas', 'House', 4, 'https://www.congress.gov/img/member/e000298_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001077', 'Higgins, Clay', '', '', 'Republican', 'Louisiana', 'House', 3, 'https://www.congress.gov/img/member/h001077_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001108', 'Comer, James', '', '', 'Republican', 'Kentucky', 'House', 1, 'https://www.congress.gov/img/member/c001108_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000585', 'LaHood, Darin', '', '', 'Republican', 'Illinois', 'House', 16, 'https://www.congress.gov/img/member/115_rp_il_18_lahood_darin_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001295', 'Bost, Mike', '', '', 'Republican', 'Illinois', 'House', 12, 'https://www.congress.gov/img/member/b001295_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001282', 'Barr, Andy', '', '', 'Republican', 'Kentucky', 'House', 6, 'https://www.congress.gov/img/member/b001282_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001184', 'Massie, Thomas', '', '', 'Republican', 'Kentucky', 'House', 4, 'https://www.congress.gov/img/member/m001184_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001188', 'Stutzman, Marlin A.', '', '', 'Republican', 'Indiana', 'House', 3, 'https://www.congress.gov/img/member/67745e7e0b34857ecc90917f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000558', 'Guthrie, Brett', '', '', 'Republican', 'Kentucky', 'House', 2, 'https://www.congress.gov/img/member/g000558_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001176', 'Scalise, Steve', '', '', 'Republican', 'Louisiana', 'House', 1, 'https://www.congress.gov/img/member/s001176_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000454', 'Foster, Bill', '', '', 'Democratic', 'Illinois', 'House', 11, 'https://www.congress.gov/img/member/f000454_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001072', 'Carson, André', '', '', 'Democratic', 'Indiana', 'House', 7, 'https://www.congress.gov/img/member/c001072_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000395', 'Rogers, Harold', '', '', 'Republican', 'Kentucky', 'House', 5, 'https://www.congress.gov/img/member/r000395_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000311', 'Jack, Brian', '', '', 'Republican', 'Georgia', 'House', 3, 'https://www.congress.gov/img/member/67742e330b34857ecc9090ef_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000487', 'Tokuda, Jill N.', '', '', 'Democratic', 'Hawaii', 'House', 2, 'https://www.congress.gov/img/member/t000487_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000193', 'Nunn, Zachary', '', '', 'Republican', 'Iowa', 'House', 3, 'https://www.congress.gov/img/member/n000193_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001219', 'Moylan, James C.', '', '', 'Republican', 'Guam', 'House', 0, 'https://www.congress.gov/img/member/m001219_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001218', 'McCormick, Richard', '', '', 'Republican', 'Georgia', 'House', 7, 'https://www.congress.gov/img/member/m001218_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000309', 'Jackson, Jonathan L.', '', '', 'Democratic', 'Illinois', 'House', 1, 'https://www.congress.gov/img/member/j000309_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001129', 'Collins, Mike', '', '', 'Republican', 'Georgia', 'House', 10, 'https://www.congress.gov/img/member/c001129_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000788', 'Williams, Nikema', '', '', 'Democratic', 'Georgia', 'House', 5, 'https://www.congress.gov/img/member/w000788_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001215', 'Miller-Meeks, Mariannette', '', '', 'Republican', 'Iowa', 'House', 1, 'https://www.congress.gov/img/member/m001215_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001091', 'Hinson, Ashley', '', '', 'Republican', 'Iowa', 'House', 2, 'https://www.congress.gov/img/member/677ed0c7514c773869b6b920_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000596', 'Greene, Marjorie Taylor', '', '', 'Republican', 'Georgia', 'House', 14, 'https://www.congress.gov/img/member/g000596_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000446', 'Feenstra, Randy', '', '', 'Republican', 'Iowa', 'House', 4, 'https://www.congress.gov/img/member/f000446_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001116', 'Clyde, Andrew S.', '', '', 'Republican', 'Georgia', 'House', 9, 'https://www.congress.gov/img/member/c001116_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001117', 'Casten, Sean', '', '', 'Democratic', 'Illinois', 'House', 6, 'https://www.congress.gov/img/member/c001117_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000586', 'García, Jesús G. "Chuy"', '', '', 'Democratic', 'Illinois', 'House', 4, 'https://www.congress.gov/img/member/g000586_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000469', 'Fulcher, Russ', '', '', 'Republican', 'Idaho', 'House', 1, 'https://www.congress.gov/img/member/f000469_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001208', 'McBath, Lucy', '', '', 'Democratic', 'Georgia', 'House', 6, 'https://www.congress.gov/img/member/m001208_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000391', 'Krishnamoorthi, Raja', '', '', 'Democratic', 'Illinois', 'House', 8, 'https://www.congress.gov/img/member/k000391_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000372', 'Allen, Rick W.', '', '', 'Republican', 'Georgia', 'House', 12, 'https://www.congress.gov/img/member/a000372_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000583', 'Loudermilk, Barry', '', '', 'Republican', 'Georgia', 'House', 11, 'https://www.congress.gov/img/member/115_rp_ga_11_loudermilk_barry_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001190', 'Schneider, Bradley Scott', '', '', 'Democratic', 'Illinois', 'House', 10, 'https://www.congress.gov/img/member/s001190_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001189', 'Scott, Austin', '', '', 'Republican', 'Georgia', 'House', 8, 'https://www.congress.gov/img/member/s001189_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000288', 'Johnson, Henry C. "Hank"', '', '', 'Democratic', 'Georgia', 'House', 4, 'https://www.congress.gov/img/member/j000288_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('Q000023', 'Quigley, Mike', '', '', 'Democratic', 'Illinois', 'House', 5, 'https://www.congress.gov/img/member/q000023_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000385', 'Kelly, Robin L.', '', '', 'Democratic', 'Illinois', 'House', 2, 'https://www.congress.gov/img/member/116_rp_il_2_kelly_robin_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001148', 'Simpson, Michael K.', '', '', 'Republican', 'Idaho', 'House', 2, 'https://www.congress.gov/img/member/678152c81f9ad6ea6fb1eb7f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001145', 'Schakowsky, Janice D.', '', '', 'Democratic', 'Illinois', 'House', 9, 'https://www.congress.gov/img/member/116_rp_il_9_schakowsky_janice_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000096', 'Davis, Danny K.', '', '', 'Democratic', 'Illinois', 'House', 7, 'https://www.congress.gov/img/member/116_rp_il_7_davis_danny_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B000490', 'Bishop, Sanford D.', '', '', 'Democratic', 'Georgia', 'House', 2, 'https://www.congress.gov/img/member/b000490_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001157', 'Scott, David', '', '', 'Democratic', 'Georgia', 'House', 13, 'https://www.congress.gov/img/member/116_rp_ga_13_scott_david_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001055', 'Case, Ed', '', '', 'Democratic', 'Hawaii', 'House', 1, 'https://www.congress.gov/img/member/c001055_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001238', 'McBride, Sarah', '', '', 'Democratic', 'Delaware', 'House', 0, 'https://www.congress.gov/img/member/67744b460b34857ecc909143_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001099', 'Haridopolos, Mike', '', '', 'Republican', 'Florida', 'House', 8, 'https://www.congress.gov/img/member/67742ab50b34857ecc9090cb_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001217', 'Moskowitz, Jared', '', '', 'Democratic', 'Florida', 'House', 23, 'https://www.congress.gov/img/member/m001217_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001216', 'Mills, Cory', '', '', 'Republican', 'Florida', 'House', 7, 'https://www.congress.gov/img/member/m001216_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000596', 'Luna, Anna Paulina', '', '', 'Republican', 'Florida', 'House', 13, 'https://www.congress.gov/img/member/l000596_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000597', 'Lee, Laurel M.', '', '', 'Republican', 'Florida', 'House', 15, 'https://www.congress.gov/img/member/l000597_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000476', 'Frost, Maxwell', '', '', 'Democratic', 'Florida', 'House', 10, 'https://www.congress.gov/img/member/f000476_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001314', 'Bean, Aaron', '', '', 'Republican', 'Florida', 'House', 4, 'https://www.congress.gov/img/member/b001314_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001127', 'Cherfilus-McCormick, Sheila', '', '', 'Democratic', 'Florida', 'House', 20, 'https://www.congress.gov/img/member/c001127_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000168', 'Salazar, Maria Elvira', '', '', 'Republican', 'Florida', 'House', 27, 'https://www.congress.gov/img/member/s000168_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000593', 'Gimenez, Carlos A.', '', '', 'Republican', 'Florida', 'House', 28, 'https://www.congress.gov/img/member/g000593_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000472', 'Franklin, Scott', '', '', 'Republican', 'Florida', 'House', 18, 'https://www.congress.gov/img/member/f000472_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000032', 'Donalds, Byron', '', '', 'Republican', 'Florida', 'House', 19, 'https://www.congress.gov/img/member/d000032_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001039', 'Cammack, Kat', '', '', 'Republican', 'Florida', 'House', 3, 'https://www.congress.gov/img/member/c001039_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001214', 'Steube, W. Gregory', '', '', 'Republican', 'Florida', 'House', 17, 'https://www.congress.gov/img/member/s001214_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001199', 'Mast, Brian J.', '', '', 'Republican', 'Florida', 'House', 21, 'https://www.congress.gov/img/member/116_rp_fl_18_mast_brian_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001200', 'Soto, Darren', '', '', 'Democratic', 'Florida', 'House', 9, 'https://www.congress.gov/img/member/115_rp_fl_9_soto_darren_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000609', 'Rutherford, John H.', '', '', 'Republican', 'Florida', 'House', 5, 'https://www.congress.gov/img/member/r000609_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000628', 'Dunn, Neal P.', '', '', 'Republican', 'Florida', 'House', 2, 'https://www.congress.gov/img/member/115_rp_fl_2_dunn_neal_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001103', 'Carter, Earl L. "Buddy"', '', '', 'Republican', 'Georgia', 'House', 1, 'https://www.congress.gov/img/member/c001103_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000462', 'Frankel, Lois', '', '', 'Democratic', 'Florida', 'House', 22, 'https://www.congress.gov/img/member/f000462_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000808', 'Wilson, Frederica S.', '', '', 'Democratic', 'Florida', 'House', 24, 'https://www.congress.gov/img/member/w000808_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000806', 'Webster, Daniel', '', '', 'Republican', 'Florida', 'House', 11, 'https://www.congress.gov/img/member/w000806_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001260', 'Buchanan, Vern', '', '', 'Republican', 'Florida', 'House', 16, 'https://www.congress.gov/img/member/b001260_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001066', 'Castor, Kathy', '', '', 'Democratic', 'Florida', 'House', 14, 'https://www.congress.gov/img/member/c001066_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001257', 'Bilirakis, Gus M.', '', '', 'Republican', 'Florida', 'House', 12, 'https://www.congress.gov/img/member/117_rp_fl_12_bilirakis_gus_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000797', 'Wasserman Schultz, Debbie', '', '', 'Democratic', 'Florida', 'House', 25, 'https://www.congress.gov/img/member/116_rp_fl_23_wassermanschultz_debbie_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000600', 'Diaz-Balart, Mario', '', '', 'Republican', 'Florida', 'House', 26, 'https://www.congress.gov/img/member/116_rp_fl_25_diazbalart_mario_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000491', 'Tran, Derek', '', '', 'Democratic', 'California', 'House', 45, 'https://www.congress.gov/img/member/6774606d0b34857ecc9091a9_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001241', 'Min, Dave', '', '', 'Democratic', 'California', 'House', 47, 'https://www.congress.gov/img/member/67744ed90b34857ecc909155_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001100', 'Hurd, Jeff', '', '', 'Republican', 'Colorado', 'House', 3, 'https://www.congress.gov/img/member/67742c5e0b34857ecc9090d1_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000300', 'Evans, Gabe', '', '', 'Republican', 'Colorado', 'House', 8, 'https://www.congress.gov/img/member/677425730b34857ecc909083_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001137', 'Crank, Jeff', '', '', 'Republican', 'Colorado', 'House', 5, 'https://www.congress.gov/img/member/677424810b34857ecc909071_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000620', 'Pettersen, Brittany', '', '', 'Democratic', 'Colorado', 'House', 7, 'https://www.congress.gov/img/member/p000620_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000598', 'Garcia, Robert', '', '', 'Democratic', 'California', 'House', 42, 'https://www.congress.gov/img/member/g000598_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000397', 'Kim, Young', '', '', 'Republican', 'California', 'House', 40, 'https://www.congress.gov/img/member/k000397_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000305', 'Jacobs, Sara', '', '', 'Democratic', 'California', 'House', 51, 'https://www.congress.gov/img/member/j000305_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B000825', 'Boebert, Lauren', '', '', 'Republican', 'Colorado', 'House', 4, 'https://www.congress.gov/img/member/b000825_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001081', 'Hayes, Jahana', '', '', 'Democratic', 'Connecticut', 'House', 5, 'https://www.congress.gov/img/member/h001081_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001121', 'Crow, Jason', '', '', 'Democratic', 'Colorado', 'House', 6, 'https://www.congress.gov/img/member/c001121_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000191', 'Neguse, Joe', '', '', 'Democratic', 'Colorado', 'House', 2, 'https://www.congress.gov/img/member/n000191_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000593', 'Levin, Mike', '', '', 'Democratic', 'California', 'House', 49, 'https://www.congress.gov/img/member/l000593_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001110', 'Correa, J. Luis', '', '', 'Democratic', 'California', 'House', 46, 'https://www.congress.gov/img/member/115_rp_ca_46_correa_j_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001300', 'Barragán, Nanette Diaz', '', '', 'Democratic', 'California', 'House', 44, 'https://www.congress.gov/img/member/b001300_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000608', 'Peters, Scott H.', '', '', 'Democratic', 'California', 'House', 50, 'https://www.congress.gov/img/member/p000608_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000130', 'Vargas, Juan', '', '', 'Democratic', 'California', 'House', 52, 'https://www.congress.gov/img/member/v000130_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000472', 'Takano, Mark', '', '', 'Democratic', 'California', 'House', 39, 'https://www.congress.gov/img/member/t000472_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001069', 'Courtney, Joe', '', '', 'Democratic', 'Connecticut', 'House', 2, 'https://www.congress.gov/img/member/c001069_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001047', 'Himes, James A.', '', '', 'Democratic', 'Connecticut', 'House', 4, 'https://www.congress.gov/img/member/h001047_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000557', 'Larson, John B.', '', '', 'Democratic', 'Connecticut', 'House', 1, 'https://www.congress.gov/img/member/l000557_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000197', 'DeGette, Diana', '', '', 'Democratic', 'Colorado', 'House', 1, 'https://www.congress.gov/img/member/116_rp_co_1_degette_diana_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000187', 'Waters, Maxine', '', '', 'Democratic', 'California', 'House', 43, 'https://www.congress.gov/img/member/w000187_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('N000147', 'Norton, Eleanor Holmes', '', '', 'Democratic', 'District of Columbia', 'House', 0, 'https://www.congress.gov/img/member/116_dg_dc_norton_eleanor_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('I000056', 'Issa, Darrell', '', '', 'Republican', 'California', 'House', 48, 'https://www.congress.gov/img/member/i000056_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C000059', 'Calvert, Ken', '', '', 'Republican', 'California', 'House', 41, 'https://www.congress.gov/img/member/c000059_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000216', 'DeLauro, Rosa L.', '', '', 'Democratic', 'Connecticut', 'House', 3, 'https://www.congress.gov/img/member/116_rp_ct_3_delauro_rosa_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000830', 'Whitesides, George', '', '', 'Democratic', 'California', 'House', 27, 'https://www.congress.gov/img/member/677461d40b34857ecc9091bb_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000620', 'Rivas, Luz M.', '', '', 'Democratic', 'California', 'House', 29, 'https://www.congress.gov/img/member/67745d860b34857ecc90916d_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000607', 'Liccardo, Sam T.', '', '', 'Democratic', 'California', 'House', 16, 'https://www.congress.gov/img/member/6774305d0b34857ecc90910d_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000605', 'Gray, Adam', '', '', 'Democratic', 'California', 'House', 13, 'https://www.congress.gov/img/member/67742a160b34857ecc9090bf_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000483', 'Friedman, Laura', '', '', 'Democratic', 'California', 'House', 30, 'https://www.congress.gov/img/member/677427070b34857ecc9090a1_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000480', 'Fong, Vince', '', '', 'Republican', 'California', 'House', 20, 'https://www.congress.gov/img/member/669ff04f5d19788d1f2034aa_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001225', 'Mullin, Kevin', '', '', 'Democratic', 'California', 'House', 15, 'https://www.congress.gov/img/member/m001225_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000400', 'Kamlager-Dove, Sydney', '', '', 'Democratic', 'California', 'House', 37, 'https://www.congress.gov/img/member/k000400_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000019', 'Obernolte, Jay', '', '', 'Republican', 'California', 'House', 23, 'https://www.congress.gov/img/member/o000019_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001123', 'Cisneros, Gilbert Ray', '', '', 'Democratic', 'California', 'House', 31, 'https://www.congress.gov/img/member/6807d8d63e52ea7df920ef05_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000585', 'Gomez, Jimmy', '', '', 'Democratic', 'California', 'House', 34, 'https://www.congress.gov/img/member/115_rp_ca_34_gomez_jimmy_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001112', 'Carbajal, Salud O.', '', '', 'Democratic', 'California', 'House', 24, 'https://www.congress.gov/img/member/115_rp_ca_24_carbajal_salud_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000613', 'Panetta, Jimmy', '', '', 'Democratic', 'California', 'House', 19, 'https://www.congress.gov/img/member/116_rp_ca_20_panetta_jimmy_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000389', 'Khanna, Ro', '', '', 'Democratic', 'California', 'House', 17, 'https://www.congress.gov/img/member/k000389_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000474', 'Torres, Norma J.', '', '', 'Democratic', 'California', 'House', 35, 'https://www.congress.gov/img/member/t000474_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000582', 'Lieu, Ted', '', '', 'Democratic', 'California', 'House', 36, 'https://www.congress.gov/img/member/l000582_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000371', 'Aguilar, Pete', '', '', 'Democratic', 'California', 'House', 33, 'https://www.congress.gov/img/member/a000371_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000599', 'Ruiz, Raul', '', '', 'Democratic', 'California', 'House', 25, 'https://www.congress.gov/img/member/66e1aec832c796cea99fe06f_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001285', 'Brownley, Julia', '', '', 'Democratic', 'California', 'House', 26, 'https://www.congress.gov/img/member/68000188f22eaf56065817e8_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000129', 'Valadao, David G.', '', '', 'Republican', 'California', 'House', 22, 'https://www.congress.gov/img/member/v000129_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001193', 'Swalwell, Eric', '', '', 'Democratic', 'California', 'House', 14, 'https://www.congress.gov/img/member/s001193_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001080', 'Chu, Judy', '', '', 'Democratic', 'California', 'House', 28, 'https://www.congress.gov/img/member/c001080_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000344', 'Sherman, Brad', '', '', 'Democratic', 'California', 'House', 32, 'https://www.congress.gov/img/member/s000344_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001059', 'Costa, Jim', '', '', 'Democratic', 'California', 'House', 21, 'https://www.congress.gov/img/member/116_rp_ca_16_costa_jim_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001156', 'Sánchez, Linda T.', '', '', 'Democratic', 'California', 'House', 38, 'https://www.congress.gov/img/member/116_rp_ca_38_snchez_linda_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000397', 'Lofgren, Zoe', '', '', 'Democratic', 'California', 'House', 18, 'https://www.congress.gov/img/member/671024d7ec807bca66057fcb_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001231', 'Simon, Lateefah', '', '', 'Democratic', 'California', 'House', 12, 'https://www.congress.gov/img/member/67745f940b34857ecc909197_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001098', 'Hamadeh, Abraham J.', '', '', 'Republican', 'Arizona', 'House', 8, 'https://www.congress.gov/img/member/67742a6f0b34857ecc9090c5_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000381', 'Ansari, Yassamin', '', '', 'Democratic', 'Arizona', 'House', 3, 'https://www.congress.gov/img/member/67741fc30b34857ecc90902e_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001220', 'Strong, Dale W.', '', '', 'Republican', 'Alabama', 'House', 5, 'https://www.congress.gov/img/member/s001220_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000401', 'Kiley, Kevin', '', '', 'Republican', 'California', 'House', 3, 'https://www.congress.gov/img/member/k000401_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001132', 'Crane, Elijah', '', '', 'Republican', 'Arizona', 'House', 2, 'https://www.congress.gov/img/member/c001132_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001133', 'Ciscomani, Juan', '', '', 'Republican', 'Arizona', 'House', 6, 'https://www.congress.gov/img/member/c001133_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001090', 'Harder, Josh', '', '', 'Democratic', 'California', 'House', 9, 'https://www.congress.gov/img/member/h001090_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001211', 'Stanton, Greg', '', '', 'Democratic', 'Arizona', 'House', 4, 'https://www.congress.gov/img/member/s001211_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001302', 'Biggs, Andy', '', '', 'Republican', 'Arizona', 'House', 5, 'https://www.congress.gov/img/member/b001302_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000623', 'DeSaulnier, Mark', '', '', 'Democratic', 'California', 'House', 10, 'https://www.congress.gov/img/member/115_rp_ca_11_desaulnier_mark_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000821', 'Westerman, Bruce', '', '', 'Republican', 'Arkansas', 'House', 4, 'https://www.congress.gov/img/member/w000821_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001072', 'Hill, J. French', '', '', 'Republican', 'Arkansas', 'House', 2, 'https://www.congress.gov/img/member/h001072_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000600', 'Radewagen, Aumua Amata Coleman', '', '', 'Republican', 'American Samoa', 'House', 0, 'https://www.congress.gov/img/member/r000600_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000609', 'Palmer, Gary J.', '', '', 'Republican', 'Alabama', 'House', 6, 'https://www.congress.gov/img/member/p000609_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001287', 'Bera, Ami', '', '', 'Democratic', 'California', 'House', 6, 'https://www.congress.gov/img/member/b001287_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001068', 'Huffman, Jared', '', '', 'Democratic', 'California', 'House', 2, 'https://www.congress.gov/img/member/h001068_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000578', 'LaMalfa, Doug', '', '', 'Republican', 'California', 'House', 1, 'https://www.congress.gov/img/member/l000578_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000559', 'Garamendi, John', '', '', 'Democratic', 'California', 'House', 8, 'https://www.congress.gov/img/member/g000559_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001183', 'Schweikert, David', '', '', 'Republican', 'Arizona', 'House', 1, 'https://www.congress.gov/img/member/s001183_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000565', 'Gosar, Paul A.', '', '', 'Republican', 'Arizona', 'House', 9, 'https://www.congress.gov/img/member/g000565_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000809', 'Womack, Steve', '', '', 'Republican', 'Arkansas', 'House', 3, 'https://www.congress.gov/img/member/117_rp_ar_3_womack_steve_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001087', 'Crawford, Eric A. "Rick"', '', '', 'Republican', 'Arkansas', 'House', 1, 'https://www.congress.gov/img/member/c001087_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001185', 'Sewell, Terri A.', '', '', 'Democratic', 'Alabama', 'House', 7, 'https://www.congress.gov/img/member/s001185_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001177', 'McClintock, Tom', '', '', 'Republican', 'California', 'House', 5, 'https://www.congress.gov/img/member/m001177_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001163', 'Matsui, Doris O.', '', '', 'Democratic', 'California', 'House', 7, 'https://www.congress.gov/img/member/m001163_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000197', 'Pelosi, Nancy', '', '', 'Democratic', 'California', 'House', 11, 'https://www.congress.gov/img/member/p000197_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000460', 'Thompson, Mike', '', '', 'Democratic', 'California', 'House', 4, 'https://www.congress.gov/img/member/116_rp_ca_5_thompson_mike_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000055', 'Aderholt, Robert B.', '', '', 'Republican', 'Alabama', 'House', 4, 'https://www.congress.gov/img/member/a000055_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000481', 'Figures, Shomari', '', '', 'Democratic', 'Alabama', 'House', 2, 'https://www.congress.gov/img/member/68013eaa4e51529406f18e42_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001323', 'Begich, Nicholas J.', '', '', 'Republican', 'Alaska', 'House', 0, 'https://www.congress.gov/img/member/6774217e0b34857ecc909040_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001212', 'Moore, Barry', '', '', 'Republican', 'Alabama', 'House', 1, 'https://www.congress.gov/img/member/m001212_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000575', 'Rogers, Mike D.', '', '', 'Republican', 'Alabama', 'House', 3, 'https://www.congress.gov/img/member/116_rp_al_3_rogers_mike_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001114', 'Curtis, John R.', '', '', 'Republican', 'Utah', 'Senate', 0, 'https://www.congress.gov/img/member/1b9d1007d6895a37da28a67cd8149803_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001104', 'Husted, Jon', '', '', 'Republican', 'Ohio', 'Senate', 0, 'https://www.congress.gov/img/member/67f0316b1b05a5a598f7fdf3_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001227', 'Schmitt, Eric', '', '', 'Republican', 'Missouri', 'Senate', 0, 'https://www.congress.gov/img/member/b66a0806e77f63e862391b15a0b1f753_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('A000382', 'Alsobrooks, Angela D.', '', '', 'Democratic', 'Maryland', 'Senate', 0, 'https://www.congress.gov/img/member/67acdbbf044eb506e25958f2_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001319', 'Britt, Katie Boyd', '', '', 'Republican', 'Alabama', 'Senate', 0, 'https://www.congress.gov/img/member/b001319_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001305', 'Budd, Ted', '', '', 'Republican', 'North Carolina', 'Senate', 0, 'https://www.congress.gov/img/member/b001305_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001208', 'Slotkin, Elissa', '', '', 'Democratic', 'Michigan', 'Senate', 0, 'https://www.congress.gov/img/member/s001208_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000394', 'Kim, Andy', '', '', 'Democratic', 'New Jersey', 'Senate', 0, 'https://www.congress.gov/img/member/677d84cbfdb6cf36bbb649a1_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001243', 'McCormick, David', '', '', 'Republican', 'Pennsylvania', 'Senate', 0, 'https://www.congress.gov/img/member/677d85e0fdb6cf36bbb649aa_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001299', 'Banks, Jim', '', '', 'Republican', 'Indiana', 'Senate', 0, 'https://www.congress.gov/img/member/677d83cbfdb6cf36bbb64998_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('Y000064', 'Young, Todd', '', '', 'Republican', 'Indiana', 'Senate', 0, 'https://www.congress.gov/img/member/y000064_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000779', 'Wyden, Ron', '', '', 'Democratic', 'Oregon', 'Senate', 0, 'https://www.congress.gov/img/member/w000779_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000790', 'Warnock, Raphael G.', '', '', 'Democratic', 'Georgia', 'Senate', 0, 'https://www.congress.gov/img/member/w000790_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000817', 'Warren, Elizabeth', '', '', 'Democratic', 'Massachusetts', 'Senate', 0, 'https://www.congress.gov/img/member/w000817_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000802', 'Whitehouse, Sheldon', '', '', 'Democratic', 'Rhode Island', 'Senate', 0, 'https://www.congress.gov/img/member/w000802_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000805', 'Warner, Mark R.', '', '', 'Democratic', 'Virginia', 'Senate', 0, 'https://www.congress.gov/img/member/w000805_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('W000437', 'Wicker, Roger F.', '', '', 'Republican', 'Mississippi', 'Senate', 0, 'https://www.congress.gov/img/member/f49ac425119375e9fe6a075762734079_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('V000128', 'Van Hollen, Chris', '', '', 'Democratic', 'Maryland', 'Senate', 0, 'https://www.congress.gov/img/member/v000128_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000278', 'Tuberville, Tommy', '', '', 'Republican', 'Alabama', 'Senate', 0, 'https://www.congress.gov/img/member/t000278_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001203', 'Smith, Tina', '', '', 'Democratic', 'Minnesota', 'Senate', 0, 'https://www.congress.gov/img/member/s001203_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000476', 'Tillis, Thomas', '', '', 'Republican', 'North Carolina', 'Senate', 0, 'https://www.congress.gov/img/member/t000476_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001198', 'Sullivan, Dan', '', '', 'Republican', 'Alaska', 'Senate', 0, 'https://www.congress.gov/img/member/s001198_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('T000250', 'Thune, John', '', '', 'Republican', 'South Dakota', 'Senate', 0, 'https://www.congress.gov/img/member/t000250_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001217', 'Scott, Rick', '', '', 'Republican', 'Florida', 'Senate', 0, 'https://www.congress.gov/img/member/s001217_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001181', 'Shaheen, Jeanne', '', '', 'Democratic', 'New Hampshire', 'Senate', 0, 'https://www.congress.gov/img/member/s001181_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000605', 'Rounds, Mike', '', '', 'Republican', 'South Dakota', 'Senate', 0, 'https://www.congress.gov/img/member/r000605_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001194', 'Schatz, Brian', '', '', 'Democratic', 'Hawaii', 'Senate', 0, 'https://www.congress.gov/img/member/s001194_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001184', 'Scott, Tim', '', '', 'Republican', 'South Carolina', 'Senate', 0, 'https://www.congress.gov/img/member/s001184_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000148', 'Schumer, Charles E.', '', '', 'Democratic', 'New York', 'Senate', 0, 'https://www.congress.gov/img/member/s000148_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S000033', 'Sanders, Bernard', '', '', 'Independent', 'Vermont', 'Senate', 0, 'https://www.congress.gov/img/member/s000033_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('S001150', 'Schiff, Adam B.', '', '', 'Democratic', 'California', 'Senate', 0, 'https://www.congress.gov/img/member/677d870dfdb6cf36bbb649b3_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000618', 'Ricketts, Pete', '', '', 'Republican', 'Nebraska', 'Senate', 0, 'https://www.congress.gov/img/member/r000618_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000608', 'Rosen, Jacky', '', '', 'Democratic', 'Nevada', 'Senate', 0, 'https://www.congress.gov/img/member/r000608_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000595', 'Peters, Gary C.', '', '', 'Democratic', 'Michigan', 'Senate', 0, 'https://www.congress.gov/img/member/p000595_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000584', 'Risch, James E.', '', '', 'Republican', 'Idaho', 'Senate', 0, 'https://www.congress.gov/img/member/r000584_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('R000122', 'Reed, Jack', '', '', 'Democratic', 'Rhode Island', 'Senate', 0, 'https://www.congress.gov/img/member/r000122_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000145', 'Padilla, Alex', '', '', 'Democratic', 'California', 'Senate', 0, 'https://www.congress.gov/img/member/p000145_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('O000174', 'Ossoff, Jon', '', '', 'Democratic', 'Georgia', 'Senate', 0, 'https://www.congress.gov/img/member/o000174_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('P000603', 'Paul, Rand', '', '', 'Republican', 'Kentucky', 'Senate', 0, 'https://www.congress.gov/img/member/p000603_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001111', 'Murray, Patty', '', '', 'Democratic', 'Washington', 'Senate', 0, 'https://www.congress.gov/img/member/1b52ad6d215684d847d1c2bf28b9b262_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001190', 'Mullin, Markwayne', '', '', 'Republican', 'Oklahoma', 'Senate', 0, 'https://www.congress.gov/img/member/m001190_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001169', 'Murphy, Christopher', '', '', 'Democratic', 'Connecticut', 'Senate', 0, 'https://www.congress.gov/img/member/m001169_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000934', 'Moran, Jerry', '', '', 'Republican', 'Kansas', 'Senate', 0, 'https://www.congress.gov/img/member/m000934_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001153', 'Murkowski, Lisa', '', '', 'Republican', 'Alaska', 'Senate', 0, 'https://www.congress.gov/img/member/m001153_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001198', 'Marshall, Roger', '', '', 'Republican', 'Kansas', 'Senate', 0, 'https://www.congress.gov/img/member/m001198_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000571', 'Lummis, Cynthia M.', '', '', 'Republican', 'Wyoming', 'Senate', 0, 'https://www.congress.gov/img/member/l000571_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M001176', 'Merkley, Jeff', '', '', 'Democratic', 'Oregon', 'Senate', 0, 'https://www.congress.gov/img/member/m001176_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000133', 'Markey, Edward J.', '', '', 'Democratic', 'Massachusetts', 'Senate', 0, 'https://www.congress.gov/img/member/m000133_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('M000355', 'McConnell, Mitch', '', '', 'Republican', 'Kentucky', 'Senate', 0, 'https://www.congress.gov/img/member/m000355_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000383', 'King, Angus S., Jr.', '', '', 'Independent', 'Maine', 'Senate', 0, 'https://www.congress.gov/img/member/k000383_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000367', 'Klobuchar, Amy', '', '', 'Democratic', 'Minnesota', 'Senate', 0, 'https://www.congress.gov/img/member/k000367_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000577', 'Lee, Mike', '', '', 'Republican', 'Utah', 'Senate', 0, 'https://www.congress.gov/img/member/l000577_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('L000575', 'Lankford, James', '', '', 'Republican', 'Oklahoma', 'Senate', 0, 'https://www.congress.gov/img/member/l000575_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000377', 'Kelly, Mark', '', '', 'Democratic', 'Arizona', 'Senate', 0, 'https://www.congress.gov/img/member/k000377_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000393', 'Kennedy, John', '', '', 'Republican', 'Louisiana', 'Senate', 0, 'https://www.congress.gov/img/member/k000393_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('K000384', 'Kaine, Tim', '', '', 'Democratic', 'Virginia', 'Senate', 0, 'https://www.congress.gov/img/member/k000384_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000312', 'Justice, James C.', '', '', 'Republican', 'West Virginia', 'Senate', 0, 'https://www.congress.gov/img/member/67c86b5e6159152e59828b1a_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001079', 'Hyde-Smith, Cindy', '', '', 'Republican', 'Mississippi', 'Senate', 0, 'https://www.congress.gov/img/member/h001079_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('J000293', 'Johnson, Ron', '', '', 'Republican', 'Wisconsin', 'Senate', 0, 'https://www.congress.gov/img/member/j000293_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001061', 'Hoeven, John', '', '', 'Republican', 'North Dakota', 'Senate', 0, 'https://www.congress.gov/img/member/h001061_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001042', 'Hirono, Mazie K.', '', '', 'Democratic', 'Hawaii', 'Senate', 0, 'https://www.congress.gov/img/member/h001042_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H000273', 'Hickenlooper, John W.', '', '', 'Democratic', 'Colorado', 'Senate', 0, 'https://www.congress.gov/img/member/h000273_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H000601', 'Hagerty, Bill', '', '', 'Republican', 'Tennessee', 'Senate', 0, 'https://www.congress.gov/img/member/h000601_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001076', 'Hassan, Margaret Wood', '', '', 'Democratic', 'New Hampshire', 'Senate', 0, 'https://www.congress.gov/img/member/h001076_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('H001046', 'Heinrich, Martin', '', '', 'Democratic', 'New Mexico', 'Senate', 0, 'https://www.congress.gov/img/member/h001046_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000386', 'Grassley, Chuck', '', '', 'Republican', 'Iowa', 'Senate', 0, 'https://www.congress.gov/img/member/g000386_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000479', 'Fetterman, John', '', '', 'Democratic', 'Pennsylvania', 'Senate', 0, 'https://www.congress.gov/img/member/f000479_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000574', 'Gallego, Ruben', '', '', 'Democratic', 'Arizona', 'Senate', 0, 'https://www.congress.gov/img/member/c6870f487cf4bc9a568d8afbe61d754b_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('F000463', 'Fischer, Deb', '', '', 'Republican', 'Nebraska', 'Senate', 0, 'https://www.congress.gov/img/member/669ec7925d19788d1f2034a1_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000555', 'Gillibrand, Kirsten E.', '', '', 'Democratic', 'New York', 'Senate', 0, 'https://www.congress.gov/img/member/g000555_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('G000359', 'Graham, Lindsey', '', '', 'Republican', 'South Carolina', 'Senate', 0, 'https://www.congress.gov/img/member/g000359_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('E000295', 'Ernst, Joni', '', '', 'Republican', 'Iowa', 'Senate', 0, 'https://www.congress.gov/img/member/e000295_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001098', 'Cruz, Ted', '', '', 'Republican', 'Texas', 'Senate', 0, 'https://www.congress.gov/img/member/c001098_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000618', 'Daines, Steve', '', '', 'Republican', 'Montana', 'Senate', 0, 'https://www.congress.gov/img/member/d000618_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000622', 'Duckworth, Tammy', '', '', 'Democratic', 'Illinois', 'Senate', 0, 'https://www.congress.gov/img/member/d000622_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('D000563', 'Durbin, Richard J.', '', '', 'Democratic', 'Illinois', 'Senate', 0, 'https://www.congress.gov/img/member/d000563_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C000880', 'Crapo, Mike', '', '', 'Republican', 'Idaho', 'Senate', 0, 'https://www.congress.gov/img/member/c000880_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001113', 'Cortez Masto, Catherine', '', '', 'Democratic', 'Nevada', 'Senate', 0, 'https://www.congress.gov/img/member/c001113_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001096', 'Cramer, Kevin', '', '', 'Republican', 'North Dakota', 'Senate', 0, 'https://www.congress.gov/img/member/c001096_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001095', 'Cotton, Tom', '', '', 'Republican', 'Arkansas', 'Senate', 0, 'https://www.congress.gov/img/member/c001095_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001056', 'Cornyn, John', '', '', 'Republican', 'Texas', 'Senate', 0, 'https://www.congress.gov/img/member/c001056_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001088', 'Coons, Christopher A.', '', '', 'Democratic', 'Delaware', 'Senate', 0, 'https://www.congress.gov/img/member/c001088_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001075', 'Cassidy, Bill', '', '', 'Republican', 'Louisiana', 'Senate', 0, 'https://www.congress.gov/img/member/c001075_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001035', 'Collins, Susan M.', '', '', 'Republican', 'Maine', 'Senate', 0, 'https://www.congress.gov/img/member/c001035_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C001047', 'Capito, Shelley Moore', '', '', 'Republican', 'West Virginia', 'Senate', 0, 'https://www.congress.gov/img/member/c001047_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('C000127', 'Cantwell, Maria', '', '', 'Democratic', 'Washington', 'Senate', 0, 'https://www.congress.gov/img/member/c000127_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001303', 'Blunt Rochester, Lisa', '', '', 'Democratic', 'Delaware', 'Senate', 0, 'https://www.congress.gov/img/member/b001303_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001288', 'Booker, Cory A.', '', '', 'Democratic', 'New Jersey', 'Senate', 0, 'https://www.congress.gov/img/member/b001288_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001277', 'Blumenthal, Richard', '', '', 'Democratic', 'Connecticut', 'Senate', 0, 'https://www.congress.gov/img/member/b001277_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001236', 'Boozman, John', '', '', 'Republican', 'Arkansas', 'Senate', 0, 'https://www.congress.gov/img/member/b001236_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001261', 'Barrasso, John', '', '', 'Republican', 'Wyoming', 'Senate', 0, 'https://www.congress.gov/img/member/b001261_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001267', 'Bennet, Michael F.', '', '', 'Democratic', 'Colorado', 'Senate', 0, 'https://www.congress.gov/img/member/b001267_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001230', 'Baldwin, Tammy', '', '', 'Democratic', 'Wisconsin', 'Senate', 0, 'https://www.congress.gov/img/member/b001230_200.jpg', true);

INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('B001243', 'Blackburn, Marsha', '', '', 'Republican', 'Tennessee', 'Senate', 0, 'https://www.congress.gov/img/member/b001243_200.jpg', true);
