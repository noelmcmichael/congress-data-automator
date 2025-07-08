# Priority Data Fix Plan - Congressional Relationships

## 🚨 **CRITICAL FINDINGS**
Based on audit results, we have a **complete relationship data gap**:
- **0% committee memberships assigned** (0 out of 100 members)
- **0% hearing-committee relationships** (0 out of 100 hearings)
- All entities exist but relationships are missing

## 🎯 **IMMEDIATE PRIORITY APPROACH**

### **Phase 1: Quick Database Schema Investigation (30 minutes)**
**Goal**: Understand why relationships are missing before collecting new data

#### **Step 1.1: Database Schema Analysis**
- [ ] Connect to production database directly
- [ ] Examine relationship table structures (`member_committees`, `hearing_committees`, etc.)
- [ ] Check if relationship data exists but API isn't exposing it
- [ ] Verify foreign key constraints and data integrity

#### **Step 1.2: API Endpoint Analysis**  
- [ ] Test all relationship endpoints (`/members/{id}/committees`, `/committees/{id}/members`)
- [ ] Check if relationship data is in database but not returned by API
- [ ] Verify if this is a data issue vs. API implementation issue

### **Phase 2: Fastest Data Collection Strategy (2-3 hours)**
**Goal**: Get basic relationships working with minimal effort

#### **Step 2.1: House.gov Committee Scraping** *(Most Reliable)*
- [ ] Scrape current House committee rosters from house.gov
- [ ] Format: `https://www.house.gov/committees/[committee-name]`
- [ ] Extract member names and match to existing member records
- [ ] Create committee membership records

#### **Step 2.2: Senate.gov Committee Scraping** *(Most Reliable)*
- [ ] Scrape current Senate committee rosters from senate.gov  
- [ ] Format: `https://www.senate.gov/committees/[committee-name].htm`
- [ ] Extract member names and match to existing member records
- [ ] Create committee membership records

#### **Step 2.3: Hearing Committee Pattern Matching** *(Quick Win)*
- [ ] Parse hearing titles for committee name patterns
- [ ] Match keywords like "Judiciary", "Armed Services", "Appropriations"
- [ ] Create hearing-committee linkages based on title analysis
- [ ] Validate matches against known committee names

### **Phase 3: Implementation & Testing (1-2 hours)**

#### **Step 3.1: Database Updates**
- [ ] Create relationship insert scripts
- [ ] Batch update committee memberships
- [ ] Batch update hearing-committee relationships
- [ ] Verify data integrity after updates

#### **Step 3.2: API Validation** 
- [ ] Test relationship endpoints with new data
- [ ] Verify member committee queries work
- [ ] Test committee member listings
- [ ] Validate hearing committee filters

## 🛠️ **Technical Implementation Tools**

### **Web Scraping Stack**
```python
# Required packages
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.3
pandas>=2.0.0
```

### **Database Connection**
```python
# Use existing Cloud SQL connection
from google.cloud.sql.connector import Connector
import sqlalchemy
```

### **Quick Win Scraping Targets**
1. **House Committees**: `https://www.house.gov/committees`
2. **Senate Committees**: `https://www.senate.gov/committees/committee_home.htm`
3. **Committee Rosters**: Individual committee pages with member listings

## 📋 **Expected Quick Results**

### **After Phase 1** *(30 minutes)*
- [ ] Clear understanding of database relationship structure
- [ ] Identification of root cause (missing data vs. API issues)
- [ ] Informed decision on data collection approach

### **After Phase 2** *(3 hours total)*
- [ ] 80%+ House committee memberships populated
- [ ] 80%+ Senate committee memberships populated  
- [ ] 60%+ hearing-committee relationships established
- [ ] Functional relationship queries in API

### **After Phase 3** *(4 hours total)*
- [ ] Production API serving accurate relationship data
- [ ] Committee membership queries working
- [ ] Hearing committee filters operational
- [ ] Data quality improved from 0% to 70%+

## 🚀 **Immediate Next Steps**

### **Step 1: Database Schema Investigation** *(START HERE)*
```bash
# Connect to production database and examine structure
python investigate_relationship_schema.py
```

### **Step 2: Choose Data Collection Approach**
Based on Step 1 findings:
- **If relationships exist in DB**: Fix API implementation
- **If relationships missing**: Proceed with web scraping
- **If schema issues**: Fix database structure first

### **Step 3: Implement Fastest Solution**
- **House.gov scraping** (most reliable, current data)
- **Title pattern matching** for hearings (immediate partial solution)
- **Batch database updates** (fastest deployment)

## ⚡ **Quick Win Metrics**
- **Target**: 70%+ relationship accuracy within 4 hours
- **Critical Path**: Database investigation → House/Senate scraping → Batch updates
- **Success Criteria**: Member committee queries return results, hearing filters work

## 🔧 **Risk Mitigation**
- **Database Backup**: Before any relationship updates
- **Staged Testing**: Test relationship updates in staging first
- **Rollback Script**: Quick revert if issues occur
- **Incremental Updates**: Add relationships gradually, not all at once

---

**DECISION POINT**: Should we proceed with Phase 1 database investigation first to understand the root cause?