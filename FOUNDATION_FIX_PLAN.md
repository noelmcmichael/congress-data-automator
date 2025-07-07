# Congressional Data Foundation Fix Plan

## Current Issues Identified
1. **Senate**: 55/100 senators (missing 45 senators)
2. **House**: 483 members (should be 441: 435 voting + 5 delegates + 1 commissioner)
3. **Adam Schiff**: Listed as House member, should be Senator from CA
4. **CA Senate**: Only 1 senator (missing Schiff as 2nd senator)

## Target Counts
- **Senate**: 100 senators (2 per state)
- **House**: 441 members (435 voting + 5 delegates + 1 commissioner)
- **Total**: 541 members

## Step-by-Step Execution Plan

### Step 1: Data Analysis & Validation
- [ ] Analyze current member counts by chamber
- [ ] Identify Adam Schiff's current record
- [ ] Check California senator count
- [ ] Identify missing senators by state
- [ ] Document current vs. target counts

### Step 2: Fix Adam Schiff Record
- [ ] Update chamber from 'house' to 'senate'
- [ ] Update state to 'CA' (if not already)
- [ ] Clear House committee assignments
- [ ] Add Senate committee assignments per user specification:
  - Judiciary Committee
  - Agriculture, Nutrition, and Forestry Committee
  - Environment and Public Works Committee
  - Small Business and Entrepreneurship Committee
  - Subcommittee assignments and leadership roles

### Step 3: Complete Senate Representation
- [ ] Identify states with only 1 senator
- [ ] Use Congress.gov API to fetch missing senators
- [ ] Ensure all 50 states have 2 senators each
- [ ] Add committee assignments for new senators

### Step 4: Correct House Count
- [ ] Identify excess House members (483 - 441 = 42 excess)
- [ ] Verify delegate and commissioner representation
- [ ] Remove duplicate or incorrect House records
- [ ] Ensure proper distribution across districts

### Step 5: Final Validation
- [ ] Verify total counts: 100 Senate + 441 House = 541
- [ ] Check committee assignment integrity
- [ ] Validate state representation (2 senators per state)
- [ ] Test API endpoints with corrected data

### Step 6: Documentation & Commit
- [ ] Update README.md with foundation fix results
- [ ] Commit changes with descriptive message
- [ ] Update validation scripts

## Expected Results
- **Senate**: 100 senators (2 per state)
- **House**: 441 members (proper composition)
- **Adam Schiff**: Correctly categorized as CA Senator
- **Committee Assignments**: Accurate for all corrected records
- **API**: All endpoints working with corrected foundation data