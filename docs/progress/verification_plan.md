# Congressional Data Verification Plan

## Problem Statement
Current database claims 100% accuracy but lacks verification against authoritative sources. Need automated benchmarking system.

## Authoritative Sources for 119th Congress

### Primary Sources
1. **congress.gov** - Official congressional information
2. **house.gov/committees** - House committee listings  
3. **senate.gov/committees** - Senate committee listings
4. **clerk.house.gov** - House official records
5. **senate.gov/general/committee_membership** - Senate membership

### Secondary Sources
6. **govtrack.us** - Structured congressional data
7. **propublica.org/congress** - Congress API
8. **ballotpedia.org** - Committee information

## Current Database Analysis Needed

### Committee Structure Verification
- [ ] Compare committee names against official sources
- [ ] Verify chamber assignments (House/Senate/Joint)
- [ ] Check committee types (Standing/Select/Joint)
- [ ] Validate parent-child relationships for subcommittees

### Member Assignment Verification  
- [ ] Cross-reference member-committee assignments
- [ ] Verify leadership positions (Chair/Ranking Member)
- [ ] Check party affiliations
- [ ] Validate assignment limits per chamber

### Leadership Accuracy
- [ ] Confirm current chairs (Republican majority)
- [ ] Verify ranking members (Democratic minority)
- [ ] Check for multiple leadership conflicts
- [ ] Validate party-position alignment

## Implementation Strategy

### Phase 1: Source Integration
Build scrapers/API clients for authoritative sources

### Phase 2: Comparison Engine
Create diff system to identify discrepancies

### Phase 3: Self-Correction
Implement automated fixes with human approval

### Phase 4: Monitoring
Continuous validation with alerts

## Success Metrics
- Accuracy score vs authoritative sources
- Time to detect discrepancies
- Automated correction rate
- False positive/negative rates