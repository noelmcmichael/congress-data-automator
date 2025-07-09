"""
Reconciles data from congress.gov API and Wikipedia.
"""
import json
import re
from typing import Dict, List, Optional, Tuple
import structlog
from sqlalchemy.orm import Session
from ..models.member import Member
from ..models.committee import Committee, CommitteeMembership

logger = structlog.get_logger()

class DataReconciler:
    """
    Compares and merges data from congress.gov and Wikipedia.
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.wikipedia_data = self.load_wikipedia_data()
        self.reconciliation_results = {
            "member_matches": [],
            "committee_matches": [],
            "leadership_updates": [],
            "errors": []
        }

    def load_wikipedia_data(self) -> Optional[Dict]:
        """
        Loads the scraped Wikipedia data from the JSON file.
        """
        try:
            with open("wikipedia_data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("wikipedia_data.json not found. Please run the scraper first.")
            return None
        except json.JSONDecodeError:
            logger.error("Error decoding wikipedia_data.json.")
            return None

    def parse_member_info(self, member_text: str) -> Dict:
        """
        Parse member name and party/state from Wikipedia format.
        Example: "Chuck Grassley (R-IA)" -> {"name": "Chuck Grassley", "party": "R", "state": "IA"}
        """
        # Extract name and party/state info
        match = re.match(r"^(.+?)\s*\(([RDI])-([A-Z]{2})\)$", member_text.strip())
        if match:
            name = match.group(1).strip()
            party = match.group(2)
            state = match.group(3)
            
            # Split name into first and last
            name_parts = name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = " ".join(name_parts[1:])
            else:
                first_name = name
                last_name = ""
            
            return {
                "full_name": name,
                "first_name": first_name,
                "last_name": last_name,
                "party": "Republican" if party == "R" else "Democratic" if party == "D" else "Independent",
                "state": state
            }
        return {"full_name": member_text, "first_name": "", "last_name": "", "party": "", "state": ""}

    def find_member_by_name(self, member_info: Dict) -> Optional[Member]:
        """
        Find a member in the database by name, with fuzzy matching.
        """
        # Try exact match first
        member = self.db.query(Member).filter(
            Member.first_name.ilike(f"%{member_info['first_name']}%"),
            Member.last_name.ilike(f"%{member_info['last_name']}%")
        ).first()
        
        if member:
            return member
        
        # Try last name only match
        if member_info['last_name']:
            member = self.db.query(Member).filter(
                Member.last_name.ilike(f"%{member_info['last_name']}%")
            ).first()
            
        return member

    def find_committee_by_name(self, committee_name: str, chamber: str) -> Optional[Committee]:
        """
        Find a committee in the database by name and chamber.
        """
        # Try exact match first
        committee = self.db.query(Committee).filter(
            Committee.name.ilike(f"%{committee_name}%"),
            Committee.chamber == chamber
        ).first()
        
        if committee:
            return committee
        
        # Try partial match on key words
        key_words = committee_name.split()
        for word in key_words:
            if len(word) > 3:  # Skip small words
                committee = self.db.query(Committee).filter(
                    Committee.name.ilike(f"%{word}%"),
                    Committee.chamber == chamber
                ).first()
                if committee:
                    return committee
        
        return None

    def reconcile_leadership(self) -> Dict:
        """
        Reconciles committee leadership roles using Wikipedia data.
        """
        if not self.wikipedia_data:
            self.reconciliation_results["errors"].append("No Wikipedia data available")
            return self.reconciliation_results

        logger.info("Starting committee leadership reconciliation...")
        
        # Check current database state
        member_count = self.db.query(Member).count()
        committee_count = self.db.query(Committee).count()
        
        logger.info(f"Database state: {member_count} members, {committee_count} committees")
        
        if member_count == 0:
            self.reconciliation_results["errors"].append("No members in database. Please populate members first.")
            return self.reconciliation_results
        
        if committee_count == 0:
            self.reconciliation_results["errors"].append("No committees in database. Please populate committees first.")
            return self.reconciliation_results
        
        # Process each committee from Wikipedia
        for wiki_committee in self.wikipedia_data.get("committees", []):
            try:
                self._reconcile_single_committee(wiki_committee)
            except Exception as e:
                error_msg = f"Error processing committee {wiki_committee.get('name', 'Unknown')}: {str(e)}"
                logger.error(error_msg)
                self.reconciliation_results["errors"].append(error_msg)
        
        # Summary
        logger.info(f"Reconciliation complete: {len(self.reconciliation_results['leadership_updates'])} updates, {len(self.reconciliation_results['errors'])} errors")
        
        return self.reconciliation_results

    def _reconcile_single_committee(self, wiki_committee: Dict):
        """
        Reconcile leadership for a single committee.
        """
        committee_name = wiki_committee["name"]
        chamber = wiki_committee["chamber"]
        
        logger.info(f"Processing {chamber} committee: {committee_name}")
        
        # Find matching committee in database
        db_committee = self.find_committee_by_name(committee_name, chamber)
        if not db_committee:
            self.reconciliation_results["errors"].append(f"Committee not found in database: {committee_name} ({chamber})")
            return
        
        self.reconciliation_results["committee_matches"].append({
            "wikipedia_name": committee_name,
            "database_name": db_committee.name,
            "chamber": chamber,
            "database_id": db_committee.id
        })
        
        # Process chair
        if wiki_committee.get("chair"):
            chair_info = self.parse_member_info(wiki_committee["chair"])
            chair_member = self.find_member_by_name(chair_info)
            
            if chair_member:
                self.reconciliation_results["member_matches"].append({
                    "wikipedia_name": chair_info["full_name"],
                    "database_name": f"{chair_member.first_name} {chair_member.last_name}",
                    "role": "Chair",
                    "committee": committee_name,
                    "member_id": chair_member.id
                })
                
                # Update chair if different
                if db_committee.chair_member_id != chair_member.id:
                    self.reconciliation_results["leadership_updates"].append({
                        "committee_id": db_committee.id,
                        "committee_name": db_committee.name,
                        "position": "chair",
                        "old_member_id": db_committee.chair_member_id,
                        "new_member_id": chair_member.id,
                        "new_member_name": chair_info["full_name"]
                    })
            else:
                self.reconciliation_results["errors"].append(f"Chair not found: {chair_info['full_name']} for {committee_name}")
        
        # Process ranking member
        if wiki_committee.get("ranking_member"):
            ranking_info = self.parse_member_info(wiki_committee["ranking_member"])
            ranking_member = self.find_member_by_name(ranking_info)
            
            if ranking_member:
                self.reconciliation_results["member_matches"].append({
                    "wikipedia_name": ranking_info["full_name"],
                    "database_name": f"{ranking_member.first_name} {ranking_member.last_name}",
                    "role": "Ranking Member",
                    "committee": committee_name,
                    "member_id": ranking_member.id
                })
                
                # Update ranking member if different
                if db_committee.ranking_member_id != ranking_member.id:
                    self.reconciliation_results["leadership_updates"].append({
                        "committee_id": db_committee.id,
                        "committee_name": db_committee.name,
                        "position": "ranking_member",
                        "old_member_id": db_committee.ranking_member_id,
                        "new_member_id": ranking_member.id,
                        "new_member_name": ranking_info["full_name"]
                    })
            else:
                self.reconciliation_results["errors"].append(f"Ranking member not found: {ranking_info['full_name']} for {committee_name}")

    def generate_update_sql(self) -> List[str]:
        """
        Generate SQL UPDATE statements for leadership changes.
        """
        sql_statements = []
        
        for update in self.reconciliation_results["leadership_updates"]:
            if update["position"] == "chair":
                sql = f"UPDATE committees SET chair_member_id = {update['new_member_id']} WHERE id = {update['committee_id']};"
            elif update["position"] == "ranking_member":
                sql = f"UPDATE committees SET ranking_member_id = {update['new_member_id']} WHERE id = {update['committee_id']};"
            else:
                continue
            
            sql_statements.append(sql)
        
        return sql_statements

    def save_results(self, filename: str = "reconciliation_results.json"):
        """
        Save reconciliation results to a JSON file.
        """
        with open(filename, "w") as f:
            json.dump(self.reconciliation_results, f, indent=2)
        
        logger.info(f"Reconciliation results saved to {filename}")


if __name__ == "__main__":
    from ..core.db import get_db
    
    db_session = next(get_db())
    reconciler = DataReconciler(db_session)
    results = reconciler.reconcile_leadership()
    reconciler.save_results()
    
    print("Reconciliation Results:")
    print(f"- Member matches: {len(results['member_matches'])}")
    print(f"- Committee matches: {len(results['committee_matches'])}")
    print(f"- Leadership updates: {len(results['leadership_updates'])}")
    print(f"- Errors: {len(results['errors'])}")
    
    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    # Generate SQL statements
    sql_statements = reconciler.generate_update_sql()
    if sql_statements:
        print(f"\nGenerated {len(sql_statements)} SQL update statements")
        with open("leadership_updates.sql", "w") as f:
            for sql in sql_statements:
                f.write(sql + "\n")
        print("SQL statements saved to leadership_updates.sql")
