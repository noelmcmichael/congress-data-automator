# Phase 2: Data Reconciliation - Step-by-Step Plan

## 🎯 Objective
Reconcile Wikipedia committee leadership data with existing database to correct inaccuracies in committee chairs and ranking members for the 119th Congress.

## 📊 Current Status Assessment
- **Wikipedia Data**: ✅ 47 committees successfully scraped with chair/ranking member information
- **Database State**: ❌ Contains 118th Congress Democratic leadership (needs correction)
- **Reconciliation Logic**: ❌ Not implemented (skeleton exists)
- **Target**: Update database with accurate 119th Congress Republican leadership

## 🔧 Phase 2 Implementation Plan

### Step 2.1: Database Connection & Schema Analysis (20 minutes)
**Goal**: Establish database connection and understand current schema for reconciliation

**Tasks**:
1. **Database Connection Setup**
   - Test database connectivity to Cloud SQL PostgreSQL
   - Verify table structure for members, committees, and committee_memberships
   - Identify chair_member_id and ranking_member_id fields in committees table

2. **Current Leadership Analysis**
   - Query existing committee leadership positions in database
   - Identify discrepancies with Wikipedia data (e.g., Democratic vs Republican chairs)
   - Document current leadership structure for comparison

3. **Schema Validation**
   - Confirm committee name matching strategy (exact vs fuzzy matching)
   - Verify member name resolution approach (first_name + last_name vs full name)
   - Plan update strategy for chair_member_id and ranking_member_id fields

**Expected Outputs**:
- Database connection confirmed
- Current leadership positions documented
- Schema update strategy defined

### Step 2.2: Member Name Matching Implementation (30 minutes)
**Goal**: Implement logic to match Wikipedia leader names with database member IDs

**Tasks**:
1. **Name Parsing Logic**
   - Extract first name, last name, party, and state from Wikipedia format
   - Handle various name formats (e.g., "Chuck Grassley (R-IA)", "Dick Durbin (D-IL)")
   - Parse party affiliation and state information

2. **Member ID Resolution**
   - Query database members table to find matching member IDs
   - Implement fuzzy matching for name variations
   - Handle edge cases (nicknames, middle names, prefixes)

3. **Validation Logic**
   - Verify party affiliation matches between Wikipedia and database
   - Cross-check state information for accuracy
   - Log unmatched names for manual review

**Expected Outputs**:
- Name parsing functions implemented
- Member ID resolution working
- Validation logic in place

### Step 2.3: Committee Matching Implementation (30 minutes)
**Goal**: Match Wikipedia committee names with database committee records

**Tasks**:
1. **Committee Name Normalization**
   - Handle variations in committee names (e.g., "Judiciary" vs "Committee on Judiciary")
   - Implement chamber-specific matching logic
   - Create committee name mapping dictionary

2. **Committee ID Resolution**
   - Query database committees table for matching records
   - Handle subcommittee vs full committee distinctions
   - Implement fuzzy matching for committee name variations

3. **Validation and Logging**
   - Verify chamber matches between Wikipedia and database
   - Log unmatched committees for manual review
   - Create committee mapping report

**Expected Outputs**:
- Committee matching functions implemented
- Committee ID resolution working
- Mapping validation complete

### Step 2.4: Leadership Position Reconciliation (40 minutes)
**Goal**: Implement core reconciliation logic to identify and prepare leadership updates

**Tasks**:
1. **Leadership Comparison Logic**
   - Compare current database leadership with Wikipedia data
   - Identify discrepancies requiring updates
   - Generate update recommendations with confidence scores

2. **Update Statement Generation**
   - Create SQL UPDATE statements for chair_member_id changes
   - Generate SQL UPDATE statements for ranking_member_id changes
   - Include validation checks in update statements

3. **Reconciliation Report**
   - Generate comprehensive report of proposed changes
   - Include current vs proposed leadership for each committee
   - Provide confidence scores and validation status

**Expected Outputs**:
- Leadership comparison complete
- SQL update statements generated
- Reconciliation report created

### Step 2.5: Data Validation & Testing (30 minutes)
**Goal**: Validate reconciliation results and test update logic

**Tasks**:
1. **Validation Testing**
   - Test name matching accuracy with known examples
   - Verify committee matching logic with sample data
   - Validate SQL statement generation

2. **Dry Run Execution**
   - Execute reconciliation in test mode (no database changes)
   - Review proposed changes for accuracy
   - Verify all Wikipedia committees are processed

3. **Error Handling**
   - Implement comprehensive error handling
   - Create rollback procedures for failed updates
   - Add logging for audit trail

**Expected Outputs**:
- Validation tests passing
- Dry run successful
- Error handling implemented

## 📈 Success Criteria
1. **Database Connection**: ✅ Successfully connected to production database
2. **Name Matching**: ✅ 95%+ accuracy in member name to ID resolution
3. **Committee Matching**: ✅ 90%+ accuracy in committee name to ID resolution  
4. **Leadership Updates**: ✅ SQL statements generated for all matched committees
5. **Validation**: ✅ All updates validated with confidence scores

## 🚀 Expected Outcomes
- **47 Committees Processed**: All Wikipedia committees analyzed for leadership updates
- **Republican Leadership**: Database updated to reflect 119th Congress Republican chairs
- **Democratic Ranking Members**: Accurate ranking member assignments
- **Audit Trail**: Complete log of all changes made
- **Confidence Scoring**: Quality assessment of all updates

## ⏱️ Time Estimate
- **Total Time**: 2.5 hours
- **Phase 2 Complete**: Ready for Phase 3 (Database Updates)
- **Next Phase**: Execute validated updates in production database

## 📋 Implementation Notes
- Focus on major committees first (Judiciary, Finance, Armed Services, etc.)
- Use Wikipedia as authoritative source for 119th Congress leadership
- Maintain comprehensive logging for audit and debugging
- Implement validation checks to prevent incorrect updates
- Create rollback procedures for safety

**Ready to begin Phase 2 implementation upon user approval.**