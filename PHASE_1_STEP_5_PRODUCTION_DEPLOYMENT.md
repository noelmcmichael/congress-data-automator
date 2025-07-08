# Phase 1 Step 1.5: Production API Deployment

## 🎯 OBJECTIVE
Deploy enhanced API to Cloud Run with Congressional session support and update production database with 119th Congress data.

## 📋 STEP-BY-STEP PLAN (45 minutes)

### **STEP 1.5.1: PRODUCTION DATABASE PREPARATION (10 minutes)**

#### Actions:
1. Connect to production Cloud SQL database
2. Backup existing database state  
3. Add congress_session columns to Member and Committee tables
4. Create congressional_sessions table
5. Verify schema updates

#### Files:
- Create `phase1_production_database_update.sql`
- Update `backend/app/models/` with production schema

#### Success Criteria:
- Production database has congressional session tracking
- No data loss during schema updates
- All existing relationships preserved

### **STEP 1.5.2: 119TH CONGRESS DATA MIGRATION (10 minutes)**

#### Actions:
1. Load 119th Congress data from `congress_119th.db`
2. Transform to production API schema format
3. Insert/update production database with 119th Congress records
4. Verify leadership mappings and relationships

#### Files:
- Use existing `phase1_migration_data_20250708_131923.json`
- Create `migrate_119th_to_production.py`

#### Success Criteria:
- 32 119th Congress members in production
- 16 119th Congress committees with current chairs
- All Republican leadership properly mapped

### **STEP 1.5.3: API ENHANCEMENT DEPLOYMENT (15 minutes)**

#### Actions:
1. Build Docker image with Congressional session support
2. Deploy enhanced API to Cloud Run
3. Verify all Congressional session endpoints
4. Test session filtering and data access

#### Files:
- Enhanced `backend/app/main.py` with congress routes
- Updated SQLAlchemy models with congress_session fields
- Enhanced Pydantic schemas

#### Success Criteria:
- `/api/v1/congress/current` returns 119th Congress data
- All 8 Congressional session endpoints operational
- Session filtering works correctly

### **STEP 1.5.4: PRODUCTION VALIDATION (10 minutes)**

#### Actions:
1. Test all API endpoints with 119th Congress context
2. Verify current leadership (Grassley, Cruz, Crapo, Wicker)
3. Validate Republican unified control metadata
4. Confirm session tracking accuracy

#### Files:
- Create `phase1_production_validation.py`
- Generate validation report

#### Success Criteria:
- 5/5 endpoint tests pass
- Current Congress properly identified as 119th
- Leadership data accurate and accessible
- Production system operational

## 🔧 TECHNICAL REQUIREMENTS

### Database Schema Updates:
```sql
-- Add congress_session to existing tables
ALTER TABLE members ADD COLUMN congress_session INTEGER DEFAULT 119;
ALTER TABLE committees ADD COLUMN congress_session INTEGER DEFAULT 119;

-- Create congressional_sessions table
CREATE TABLE congressional_sessions (
    session_id SERIAL PRIMARY KEY,
    congress_number INTEGER UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    party_control_house VARCHAR(20),
    party_control_senate VARCHAR(20)
);
```

### API Endpoints Ready:
- `/api/v1/congress/current` - Current Congressional session info
- `/api/v1/congress/{congress_number}` - Specific Congress data
- `/api/v1/congress/history` - Congressional session history
- `/api/v1/congress/transitions` - Party control transitions
- Plus 4 additional Congressional context endpoints

### Data Migration Ready:
- 32 119th Congress members with enhanced schema
- 16 committees with current Republican chairs
- Congressional session metadata (2025-2027)
- Leadership mapping (names → member IDs)

## ⚠️ RISK MITIGATION

### Potential Issues:
1. **Database Schema Lock**: Production database locked during update
2. **API Deployment Timeout**: Cloud Run container startup issues
3. **Data Consistency**: Migration conflicts with existing data
4. **Congressional Session Logic**: Session tracking not working correctly

### Mitigation Strategies:
1. **Quick Schema Updates**: Minimal downtime approach with rolling updates
2. **Container Testing**: Pre-test container locally before deployment
3. **Backup and Rollback**: Full database backup before any changes
4. **Step-by-step Validation**: Test each component before proceeding

## 📊 SUCCESS METRICS

### Completion Criteria:
- [ ] Production database has 119th Congress data
- [ ] API returns current Congressional session as 119th
- [ ] Republican leadership accessible via API
- [ ] All 8 Congressional session endpoints operational
- [ ] Session filtering works correctly
- [ ] No production system downtime

### Expected Outcomes:
- **API Enhanced**: Congressional session tracking throughout
- **Data Current**: 119th Congress (2025-2027) instead of 118th
- **Leadership Accurate**: Current Republican chairs and ranking members
- **Foundation Ready**: Prepared for Phase 2 frontend integration

## 🚀 READY TO PROCEED

**Status**: All preparation complete, tools ready, local testing passed  
**Estimated Time**: 45 minutes  
**Dependencies**: Cloud SQL access, Cloud Run deployment permissions  
**Rollback Plan**: Database backup restoration available  

**Ready to begin production deployment on user confirmation.**