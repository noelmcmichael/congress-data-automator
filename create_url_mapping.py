#!/usr/bin/env python3

"""
Step 3: URL Mapping System
Create comprehensive mapping of provided URLs to database committees
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import re

def connect_to_database():
    """Connect to Cloud SQL database via proxy"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def get_current_committees():
    """Get all current committees from database"""
    conn = connect_to_database()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, chamber, committee_type, is_subcommittee
            FROM committees
            WHERE is_subcommittee = FALSE OR is_subcommittee IS NULL
            ORDER BY chamber, name;
        """)
        
        committees = cursor.fetchall()
        return [dict(committee) for committee in committees]
        
    except Exception as e:
        print(f"Error fetching committees: {e}")
        return []
    
    finally:
        conn.close()

def create_official_url_data():
    """Create structured data from the provided research URLs"""
    
    # Senate Committees with URLs
    senate_committees = {
        "Agriculture, Nutrition, and Forestry": {
            "hearings_url": "https://www.agriculture.senate.gov/hearings",
            "members_url": "https://www.agriculture.senate.gov/about/membership"
        },
        "Appropriations": {
            "hearings_url": "https://www.appropriations.senate.gov/hearings",
            "members_url": "https://www.appropriations.senate.gov/about/members"
        },
        "Armed Services": {
            "hearings_url": "https://www.armed-services.senate.gov/hearings",
            "members_url": "https://www.armed-services.senate.gov/about"
        },
        "Banking, Housing, and Urban Affairs": {
            "hearings_url": "https://www.banking.senate.gov/hearings",
            "members_url": "https://www.banking.senate.gov/about/members"
        },
        "Budget": {
            "hearings_url": "https://www.budget.senate.gov/hearings",
            "members_url": "https://www.budget.senate.gov/about/committee-members"
        },
        "Commerce, Science, and Transportation": {
            "hearings_url": "https://www.commerce.senate.gov/2025/hearings",
            "members_url": "https://www.commerce.senate.gov/members"
        },
        "Energy and Natural Resources": {
            "hearings_url": "https://www.energy.senate.gov/hearings",
            "members_url": "https://www.energy.senate.gov/about-committees"
        },
        "Environment and Public Works": {
            "hearings_url": "https://www.epw.senate.gov/public/index.cfm/hearings",
            "members_url": "https://www.epw.senate.gov/public/index.cfm/members"
        },
        "Finance": {
            "hearings_url": "https://www.finance.senate.gov/hearings",
            "members_url": "https://www.finance.senate.gov/about/membership"
        },
        "Foreign Relations": {
            "hearings_url": "https://www.foreign.senate.gov/hearings",
            "members_url": "https://www.foreign.senate.gov/about/committee-membership"
        },
        "Health, Education, Labor, and Pensions": {
            "hearings_url": "https://www.help.senate.gov/hearings",
            "members_url": "https://www.help.senate.gov/about/members"
        },
        "Homeland Security and Governmental Affairs": {
            "hearings_url": "https://www.hsgac.senate.gov/hearings",
            "members_url": "https://www.hsgac.senate.gov/about/committee-membership"
        },
        "Judiciary": {
            "hearings_url": "https://www.judiciary.senate.gov/meetings",
            "members_url": "https://www.judiciary.senate.gov/about/members"
        },
        "Rules and Administration": {
            "hearings_url": "https://www.rules.senate.gov/hearings",
            "members_url": "https://www.rules.senate.gov/about/members"
        },
        "Small Business and Entrepreneurship": {
            "hearings_url": "https://www.sbc.senate.gov/public/index.cfm/hearings",
            "members_url": "https://www.sbc.senate.gov/public/index.cfm/members"
        },
        "Veterans' Affairs": {
            "hearings_url": "https://www.veterans.senate.gov/hearings",
            "members_url": "https://www.veterans.senate.gov/about/membership"
        },
        # Select Committees
        "Select Committee on Intelligence": {
            "hearings_url": "https://www.intelligence.senate.gov/hearings",
            "members_url": "https://www.intelligence.senate.gov/about"
        },
        "Special Committee on Aging": {
            "hearings_url": "https://www.aging.senate.gov/hearings",
            "members_url": "https://www.aging.senate.gov/about"
        }
    }
    
    # House Committees with URLs
    house_committees = {
        "Agriculture": {
            "hearings_url": "https://agriculture.house.gov/calendar/?EventTypeID=214",
            "members_url": "https://agriculture.house.gov/about/committee-members.htm"
        },
        "Appropriations": {
            "hearings_url": "https://appropriations.house.gov/calendar",
            "members_url": "https://appropriations.house.gov/about/members"
        },
        "Armed Services": {
            "hearings_url": "https://armedservices.house.gov/meetings",
            "members_url": "https://armedservices.house.gov/members"
        },
        "Budget": {
            "hearings_url": "https://budget.house.gov/legislation/hearings",
            "members_url": "https://budget.house.gov/about/members"
        },
        "Education and the Workforce": {
            "hearings_url": "https://edworkforce.house.gov/schedule",
            "members_url": "https://edworkforce.house.gov/about/members.htm"
        },
        "Energy and Commerce": {
            "hearings_url": "https://energycommerce.house.gov/committee-activity/hearings",
            "members_url": "https://energycommerce.house.gov/about-ec/committee-members"
        },
        "Ethics": {
            "hearings_url": "https://ethics.house.gov/events",
            "members_url": "https://ethics.house.gov/committee-members"
        },
        "Financial Services": {
            "hearings_url": "https://financialservices.house.gov/calendar",
            "members_url": "https://financialservices.house.gov/about/membership.htm"
        },
        "Foreign Affairs": {
            "hearings_url": "https://foreignaffairs.house.gov/hearings",
            "members_url": "https://foreignaffairs.house.gov/members"
        },
        "Homeland Security": {
            "hearings_url": "https://homeland.house.gov/activities/hearings",
            "members_url": "https://homeland.house.gov/about/membership"
        },
        "House Administration": {
            "hearings_url": "https://cha.house.gov/committee-activity/hearings",
            "members_url": "https://cha.house.gov/about/members"
        },
        "Judiciary": {
            "hearings_url": "https://judiciary.house.gov/committee-activity/hearings",
            "members_url": "https://judiciary.house.gov/about/members"
        },
        "Natural Resources": {
            "hearings_url": "https://naturalresources.house.gov/calendar",
            "members_url": "https://naturalresources.house.gov/about/members.htm"
        },
        "Oversight and Accountability": {
            "hearings_url": "https://oversight.house.gov/hearing",
            "members_url": "https://oversight.house.gov/full-committee-members"
        },
        "Rules": {
            "hearings_url": "https://rules.house.gov/hearings",
            "members_url": "https://rules.house.gov/about/members"
        },
        "Science, Space, and Technology": {
            "hearings_url": "https://science.house.gov/hearings",
            "members_url": "https://science.house.gov/about/membership"
        },
        "Small Business": {
            "hearings_url": "https://smallbusiness.house.gov/legislation/hearings.htm",
            "members_url": "https://smallbusiness.house.gov/about/members.htm"
        },
        "Transportation and Infrastructure": {
            "hearings_url": "https://transportation.house.gov/committee-activity/hearings",
            "members_url": "https://transportation.house.gov/about/members.htm"
        },
        "Veterans' Affairs": {
            "hearings_url": "https://veterans.house.gov/events/hearings",
            "members_url": "https://veterans.house.gov/about/membership"
        },
        "Ways and Means": {
            "hearings_url": "https://waysandmeans.house.gov/hearings",
            "members_url": "https://waysandmeans.house.gov/about/members.htm"
        },
        # Select Committees
        "Permanent Select Committee on Intelligence": {
            "hearings_url": "https://intelligence.house.gov/calendar/?EventTypeID=215",
            "members_url": "https://intelligence.house.gov/about/hpsci-members.htm"
        },
        "Select Committee on the Strategic Competition Between the U.S. and the CCP": {
            "hearings_url": "https://selectcommitteeontheccp.house.gov/committee-activity/hearings",
            "members_url": "https://selectcommitteeontheccp.house.gov/members"
        }
    }
    
    return senate_committees, house_committees

def normalize_committee_name(name):
    """Normalize committee names for matching"""
    # Remove "Committee on" prefix
    normalized = re.sub(r'^Committee on\s+', '', name, flags=re.IGNORECASE)
    # Remove "the" articles
    normalized = re.sub(r'\bthe\s+', ' ', normalized, flags=re.IGNORECASE)
    # Remove extra spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized.lower()

def create_committee_mapping():
    """Create mapping between database committees and official URLs"""
    
    # Get current committees from database
    db_committees = get_current_committees()
    
    # Get official URL data
    senate_urls, house_urls = create_official_url_data()
    
    # Create mapping
    mapping = {
        "timestamp": datetime.now().isoformat(),
        "source": "Official Congressional Committee URLs Research",
        "mapping_stats": {
            "total_db_committees": len(db_committees),
            "total_senate_urls": len(senate_urls),
            "total_house_urls": len(house_urls)
        },
        "mappings": [],
        "unmapped_committees": [],
        "unmapped_urls": []
    }
    
    print("🔗 CREATING COMMITTEE URL MAPPING")
    print("=" * 60)
    
    mapped_urls = set()
    
    for committee in db_committees:
        db_name = committee['name']
        db_chamber = committee['chamber']
        normalized_db_name = normalize_committee_name(db_name)
        
        # Choose the appropriate URL source
        url_source = senate_urls if db_chamber == 'Senate' else house_urls
        
        # Try to find a match
        match_found = False
        for url_name, urls in url_source.items():
            normalized_url_name = normalize_committee_name(url_name)
            
            # Check for exact match or partial match
            if (normalized_db_name == normalized_url_name or 
                normalized_db_name in normalized_url_name or
                normalized_url_name in normalized_db_name):
                
                committee_mapping = {
                    "committee_id": committee['id'],
                    "database_name": db_name,
                    "official_name": url_name,
                    "chamber": db_chamber,
                    "hearings_url": urls['hearings_url'],
                    "members_url": urls['members_url'],
                    "match_type": "exact" if normalized_db_name == normalized_url_name else "partial",
                    "confidence": 1.0 if normalized_db_name == normalized_url_name else 0.8
                }
                
                mapping['mappings'].append(committee_mapping)
                mapped_urls.add(url_name)
                match_found = True
                
                print(f"✅ {db_chamber:<6} {db_name[:50]:<50} -> {url_name[:30]}")
                break
        
        if not match_found:
            mapping['unmapped_committees'].append({
                "committee_id": committee['id'],
                "name": db_name,
                "chamber": db_chamber,
                "reason": "No matching URL found"
            })
            print(f"❌ {db_chamber:<6} {db_name[:50]:<50} -> NO MATCH")
    
    # Find unmapped URLs
    all_urls = {**senate_urls, **house_urls}
    for url_name in all_urls.keys():
        if url_name not in mapped_urls:
            mapping['unmapped_urls'].append({
                "name": url_name,
                "chamber": "Senate" if url_name in senate_urls else "House",
                "reason": "No matching committee in database"
            })
    
    # Update stats
    mapping['mapping_stats'].update({
        "successful_mappings": len(mapping['mappings']),
        "unmapped_committees": len(mapping['unmapped_committees']),
        "unmapped_urls": len(mapping['unmapped_urls']),
        "mapping_rate": len(mapping['mappings']) / len(db_committees) * 100
    })
    
    print("\n📊 MAPPING STATISTICS:")
    print("=" * 60)
    print(f"  Total Database Committees: {mapping['mapping_stats']['total_db_committees']}")
    print(f"  Successful Mappings: {mapping['mapping_stats']['successful_mappings']}")
    print(f"  Unmapped Committees: {mapping['mapping_stats']['unmapped_committees']}")
    print(f"  Unmapped URLs: {mapping['mapping_stats']['unmapped_urls']}")
    print(f"  Mapping Rate: {mapping['mapping_stats']['mapping_rate']:.1f}%")
    
    # Save mapping to file
    with open('committee_url_mapping.json', 'w') as f:
        json.dump(mapping, f, indent=2, default=str)
    
    print(f"\n✅ MAPPING COMPLETE")
    print(f"📁 Report saved to: committee_url_mapping.json")
    
    return mapping

def main():
    """Main execution function"""
    print("🚀 STARTING URL MAPPING SYSTEM")
    print("=" * 60)
    
    mapping = create_committee_mapping()
    
    print("\n🎯 MAPPING READY FOR STEP 4: DATABASE POPULATION")
    print("=" * 60)
    print(f"✅ {len(mapping['mappings'])} committees ready for URL updates")
    print(f"⚠️  {len(mapping['unmapped_committees'])} committees need manual review")
    print(f"📋 Next: Execute database population with mapped URLs")

if __name__ == "__main__":
    main()