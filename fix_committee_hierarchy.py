#!/usr/bin/env python3
"""
Fix committee hierarchy by linking subcommittees to their parent standing committees.
Priority: Senate first, then House.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_committee_hierarchy():
    """Fix committee hierarchy by linking subcommittees to parent committees."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    # Committee hierarchy mapping (based on real congressional structure)
    committee_hierarchy = {
        # Senate Standing Committees and their subcommittees
        "Committee on Agriculture, Nutrition, and Forestry": [
            "Commodities, Risk Management, and Trade Subcommittee",
            "Conservation, Forestry and Natural Resources Subcommittee", 
            "Food and Nutrition, Specialty Crops, Organics, and Research Subcommittee",
            "Livestock, Dairy, Poultry, Local Food Systems, and Food Safety and Security Subcommittee"
        ],
        "Committee on Appropriations": [
            "Agriculture, Rural Development, Food and Drug Administration, and Related Agencies Subcommittee",
            "Commerce, Justice, Science, and Related Agencies Subcommittee",
            "Defense Subcommittee",
            "Energy and Water Development Subcommittee",
            "Financial Services and General Government Subcommittee",
            "Homeland Security Subcommittee",
            "Interior, Environment, and Related Agencies Subcommittee",
            "Labor, Health and Human Services, Education, and Related Agencies Subcommittee",
            "Legislative Branch Subcommittee",
            "Military Construction, Veterans Affairs, and Related Agencies Subcommittee",
            "State, Foreign Operations, and Related Programs Subcommittee",
            "Transportation, Housing and Urban Development, and Related Agencies Subcommittee"
        ],
        "Committee on Armed Services": [
            "Airland Subcommittee",
            "Cybersecurity Subcommittee", 
            "Emerging Threats and Capabilities Subcommittee",
            "Personnel Subcommittee",
            "Readiness and Management Support Subcommittee",
            "Seapower Subcommittee",
            "Strategic Forces Subcommittee"
        ],
        "Committee on Banking, Housing, and Urban Affairs": [
            "Economic Policy Subcommittee",
            "Financial Institutions and Consumer Protection Subcommittee",
            "Housing, Transportation, and Community Development Subcommittee",
            "National Security and International Trade and Finance Subcommittee"
        ],
        "Committee on Commerce, Science, and Transportation": [
            "Aviation Safety, Operations, and Innovation Subcommittee",
            "Communications, Media, and Broadband Subcommittee",
            "Consumer Protection, Product Safety, and Data Security Subcommittee",
            "Oceans, Fisheries, Climate Change, and Manufacturing Subcommittee",
            "Space and Science Subcommittee",
            "Surface Transportation, Maritime, Freight, and Ports Subcommittee",
            "Tourism, Trade, and Export Promotion Subcommittee"
        ],
        "Committee on Energy and Natural Resources": [
            "Energy Subcommittee",
            "National Parks Subcommittee",
            "Public Lands, Forests, and Mining Subcommittee",
            "Water and Power Subcommittee"
        ],
        "Committee on Environment and Public Works": [
            "Chemical Safety, Waste Management, Environmental Justice, and Regulatory Oversight Subcommittee",
            "Clean Air, Climate, and Nuclear Safety Subcommittee",
            "Fisheries, Water, and Wildlife Subcommittee",
            "Transportation and Infrastructure Subcommittee"
        ],
        "Committee on Finance": [
            "Energy, Natural Resources, and Infrastructure Subcommittee",
            "Fiscal Responsibility and Economic Growth Subcommittee",
            "Health Care Subcommittee",
            "International Trade, Customs, and Global Competitiveness Subcommittee",
            "Social Security, Pensions, and Family Policy Subcommittee",
            "Taxation and IRS Oversight Subcommittee"
        ],
        "Committee on Foreign Relations": [
            "Africa and Global Health Policy Subcommittee",
            "East Asia, The Pacific, and International Cybersecurity Policy Subcommittee",
            "Europe and Regional Security Cooperation Subcommittee",
            "International Development and Multilateral Institutions Subcommittee",
            "Near East, South Asia, Central Asia, and Counterterrorism Subcommittee",
            "State Department and USAID Management, International Operations, and Bilateral International Development Subcommittee",
            "Western Hemisphere, Transnational Crime, Civilian Security, Democracy, Human Rights, and Global Women's Issues Subcommittee"
        ],
        "Committee on Health, Education, Labor and Pensions": [
            "Children and Families Subcommittee",
            "Employment and Workplace Safety Subcommittee",
            "Primary Health and Retirement Security Subcommittee"
        ],
        "Committee on Homeland Security and Governmental Affairs": [
            "Emerging Threats and Spending Oversight Subcommittee",
            "Government Operations and Border Management Subcommittee",
            "Investigations Subcommittee"
        ],
        "Committee on the Judiciary": [
            "Competition Policy, Antitrust, and Consumer Rights Subcommittee",
            "Criminal Justice and Counterterrorism Subcommittee",
            "Federal Courts, Oversight, Agency Action, and Federal Rights Subcommittee",
            "Immigration, Citizenship, and Border Safety Subcommittee",
            "Privacy, Technology, and the Law Subcommittee"
        ],
        
        # House Standing Committees and their subcommittees  
        "Committee on Agriculture": [
            "Biotechnology, Horticulture, and Research Subcommittee",
            "Commodity Exchanges, Energy, and Credit Subcommittee",
            "Conservation and Forestry Subcommittee",
            "General Farm Commodities, Risk Management, and Credit Subcommittee",
            "Livestock and Foreign Agriculture Subcommittee"
        ],
        "Committee on Appropriations": [
            "Agriculture, Rural Development, Food and Drug Administration, and Related Agencies Subcommittee",
            "Commerce, Justice, Science, and Related Agencies Subcommittee", 
            "Defense Subcommittee",
            "Energy and Water Development, and Related Agencies Subcommittee",
            "Financial Services and General Government Subcommittee",
            "Homeland Security Subcommittee",
            "Interior, Environment, and Related Agencies Subcommittee",
            "Labor, Health and Human Services, Education, and Related Agencies Subcommittee",
            "Legislative Branch Subcommittee",
            "Military Construction, Veterans Affairs, and Related Agencies Subcommittee",
            "State, Foreign Operations, and Related Programs Subcommittee",
            "Transportation, Housing and Urban Development, and Related Agencies Subcommittee"
        ],
        "Committee on Armed Services": [
            "Cyber, Innovative Technologies, and Information Systems Subcommittee",
            "Intelligence and Special Operations Subcommittee",
            "Military Personnel Subcommittee",
            "Readiness Subcommittee",
            "Seapower and Projection Forces Subcommittee",
            "Strategic Forces Subcommittee",
            "Tactical Air and Land Forces Subcommittee"
        ],
        "Committee on Energy and Commerce": [
            "Communications and Technology Subcommittee",
            "Energy, Climate and Grid Security Subcommittee",
            "Environment, Manufacturing, and Critical Materials Subcommittee",
            "Health Subcommittee",
            "Innovation, Data, and Commerce Subcommittee",
            "Oversight and Investigations Subcommittee"
        ],
        "Committee on Financial Services": [
            "Capital Markets Subcommittee",
            "Digital Assets, Financial Technology and Inclusion Subcommittee",
            "Financial Institutions and Monetary Policy Subcommittee",
            "Housing and Insurance Subcommittee",
            "National Security, Illicit Finance, and International Financial Institutions Subcommittee",
            "Oversight and Investigations Subcommittee"
        ],
        "Committee on Foreign Affairs": [
            "Africa Subcommittee",
            "Asia and the Pacific Subcommittee", 
            "Europe Subcommittee",
            "Global Health, Global Human Rights, and International Organizations Subcommittee",
            "International Development, International Organizations, and Corporate Social Impact Subcommittee",
            "Middle East, North Africa and Central Asia Subcommittee",
            "Oversight and Accountability Subcommittee",
            "South and Central Asia Subcommittee",
            "Western Hemisphere Subcommittee"
        ],
        "Committee on the Judiciary": [
            "Administrative State, Regulatory Reform, and Antitrust Subcommittee",
            "Constitution and Limited Government Subcommittee",
            "Courts, Intellectual Property, and the Internet Subcommittee",
            "Crime and Federal Government Surveillance Subcommittee",
            "Immigration Integrity, Security, and Enforcement Subcommittee",
            "Responsiveness and Accountability to Oversight Subcommittee"
        ],
        "Committee on Natural Resources": [
            "Energy and Mineral Resources Subcommittee",
            "Federal Lands Subcommittee",
            "Indian and Insular Affairs Subcommittee",
            "Oversight and Investigations Subcommittee",
            "Water, Wildlife and Fisheries Subcommittee"
        ],
        "Committee on Oversight and Accountability": [
            "Cybersecurity, Information Technology, and Government Innovation Subcommittee",
            "Economic Growth, Energy Policy, and Regulatory Affairs Subcommittee",
            "Government Operations and the Federal Workforce Subcommittee",
            "Health Care and Financial Services Subcommittee",
            "National Security, the Border, and Foreign Affairs Subcommittee"
        ],
        "Committee on Science, Space, and Technology": [
            "Energy Subcommittee",
            "Environment Subcommittee", 
            "Investigations and Oversight Subcommittee",
            "Research and Technology Subcommittee",
            "Space and Aeronautics Subcommittee"
        ],
        "Committee on Transportation and Infrastructure": [
            "Aviation Subcommittee",
            "Coast Guard and Maritime Transportation Subcommittee",
            "Economic Development, Public Buildings, and Emergency Management Subcommittee",
            "Highways and Transit Subcommittee",
            "Railroads, Pipelines, and Hazardous Materials Subcommittee",
            "Water Resources and Environment Subcommittee"
        ],
        "Committee on Veterans' Affairs": [
            "Disability Assistance and Memorial Affairs Subcommittee",
            "Economic Opportunity Subcommittee",
            "Health Subcommittee",
            "Oversight and Investigations Subcommittee",
            "Technology Modernization Subcommittee"
        ],
        "Committee on Ways and Means": [
            "Health Subcommittee",
            "Oversight Subcommittee",
            "Select Revenue Measures Subcommittee",
            "Social Security Subcommittee",
            "Tax Subcommittee",
            "Trade Subcommittee"
        ]
    }
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("🔧 FIXING COMMITTEE HIERARCHY")
            logger.info("="*60)
            
            # Begin transaction
            trans = conn.begin()
            
            try:
                updates_made = 0
                
                for parent_name, subcommittee_names in committee_hierarchy.items():
                    # Find the parent committee
                    result = conn.execute(text("""
                        SELECT id, name, chamber FROM committees 
                        WHERE name = :parent_name AND is_subcommittee = false
                    """), {"parent_name": parent_name})
                    
                    parent = result.fetchone()
                    
                    if parent:
                        parent_id, parent_full_name, chamber = parent
                        logger.info(f"\n📋 {parent_full_name} ({chamber})")
                        
                        subcommittees_linked = 0
                        
                        for subcommittee_name in subcommittee_names:
                            # Find the subcommittee (try exact match first, then partial)
                            result = conn.execute(text("""
                                SELECT id, name FROM committees 
                                WHERE (name = :sub_name OR name LIKE :sub_pattern)
                                AND chamber = :chamber
                                AND is_subcommittee = true
                                AND parent_committee_id IS NULL
                            """), {
                                "sub_name": subcommittee_name,
                                "sub_pattern": f"%{subcommittee_name.replace(' Subcommittee', '')}%",
                                "chamber": chamber
                            })
                            
                            subcommittee = result.fetchone()
                            
                            if subcommittee:
                                sub_id, sub_name = subcommittee
                                
                                # Update the subcommittee to link to parent
                                conn.execute(text("""
                                    UPDATE committees 
                                    SET parent_committee_id = :parent_id 
                                    WHERE id = :sub_id
                                """), {"parent_id": parent_id, "sub_id": sub_id})
                                
                                logger.info(f"  ✅ {sub_name}")
                                subcommittees_linked += 1
                                updates_made += 1
                            else:
                                logger.warning(f"  ❌ {subcommittee_name} (not found)")
                        
                        logger.info(f"  📊 Linked {subcommittees_linked}/{len(subcommittee_names)} subcommittees")
                    else:
                        logger.warning(f"❌ Parent committee not found: {parent_name}")
                
                # Commit transaction
                trans.commit()
                
                logger.info(f"\n✅ HIERARCHY FIX COMPLETE")
                logger.info(f"Total updates made: {updates_made}")
                
                # Verify the fix
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM committees 
                    WHERE is_subcommittee = true AND parent_committee_id IS NOT NULL
                """))
                
                linked_count = result.scalar()
                
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM committees WHERE is_subcommittee = true
                """))
                
                total_subcommittees = result.scalar()
                
                logger.info(f"📊 Verification:")
                logger.info(f"   Subcommittees with parent links: {linked_count}")
                logger.info(f"   Total subcommittees: {total_subcommittees}")
                logger.info(f"   Coverage: {linked_count/total_subcommittees*100:.1f}%")
                
                return True
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ Error fixing hierarchy: {e}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    fix_committee_hierarchy()