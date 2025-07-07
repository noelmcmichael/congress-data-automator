#!/usr/bin/env python3
"""
Phase 3A - Reliable Sources Analysis
Analyze current URLs, identify unreliable sources, and create coverage gap report.
"""
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd

class ReliableSourcesAnalyzer:
    def __init__(self):
        self.api_base = "https://congressional-data-api-v3-1066017671167.us-central1.run.app"
        self.timeout = 10
        self.user_agent = "Congressional Data Quality Analyzer 1.0"
        self.reliable_sources = []
        self.unreliable_sources = []
        self.coverage_gaps = []
        
    def get_committee_data(self) -> List[Dict]:
        """Get current committee data from API."""
        try:
            response = requests.get(f"{self.api_base}/api/v1/committees", timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get committee data: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting committee data: {e}")
            return []
    
    def test_url_reliability(self, url: str) -> Dict:
        """Test URL reliability with detailed analysis."""
        if not url:
            return {
                "url": url,
                "status": "empty",
                "reliable": False,
                "error": "Empty URL",
                "response_time": 0,
                "content_length": 0
            }
        
        try:
            start_time = time.time()
            response = requests.get(
                url, 
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent},
                allow_redirects=True
            )
            response_time = time.time() - start_time
            
            # Analyze response
            analysis = {
                "url": url,
                "status_code": response.status_code,
                "response_time": round(response_time, 2),
                "content_length": len(response.content),
                "final_url": response.url,
                "redirected": response.url != url,
                "reliable": False,
                "error": None
            }
            
            # Determine reliability
            if response.status_code == 200:
                if response_time < 5.0 and len(response.content) > 1000:
                    analysis["reliable"] = True
                    analysis["status"] = "reliable"
                elif response_time >= 5.0:
                    analysis["reliable"] = False
                    analysis["status"] = "slow"
                    analysis["error"] = f"Slow response: {response_time}s"
                elif len(response.content) <= 1000:
                    analysis["reliable"] = False
                    analysis["status"] = "minimal_content"
                    analysis["error"] = f"Minimal content: {len(response.content)} bytes"
            elif response.status_code in [301, 302, 303, 307, 308]:
                analysis["reliable"] = False
                analysis["status"] = "redirect"
                analysis["error"] = f"Redirect to {response.url}"
            elif response.status_code == 404:
                analysis["reliable"] = False
                analysis["status"] = "not_found"
                analysis["error"] = "Page not found"
            elif response.status_code >= 500:
                analysis["reliable"] = False
                analysis["status"] = "server_error"
                analysis["error"] = f"Server error: {response.status_code}"
            else:
                analysis["reliable"] = False
                analysis["status"] = "client_error"
                analysis["error"] = f"Client error: {response.status_code}"
                
            return analysis
            
        except requests.exceptions.Timeout:
            return {
                "url": url,
                "status": "timeout",
                "reliable": False,
                "error": "Request timeout",
                "response_time": self.timeout,
                "content_length": 0
            }
        except requests.exceptions.ConnectionError:
            return {
                "url": url,
                "status": "connection_error",
                "reliable": False,
                "error": "Connection failed",
                "response_time": 0,
                "content_length": 0
            }
        except Exception as e:
            return {
                "url": url,
                "status": "error",
                "reliable": False,
                "error": str(e),
                "response_time": 0,
                "content_length": 0
            }
    
    def analyze_committee_urls(self, committees: List[Dict]) -> Dict:
        """Analyze all committee URLs for reliability."""
        print("🔍 Analyzing committee URL reliability...")
        
        url_analysis = {
            "reliable": [],
            "unreliable": [],
            "coverage_by_committee": {},
            "coverage_by_chamber": {"House": {"total": 0, "reliable": 0}, "Senate": {"total": 0, "reliable": 0}},
            "url_type_analysis": {
                "hearings_url": {"total": 0, "reliable": 0},
                "members_url": {"total": 0, "reliable": 0},
                "official_website_url": {"total": 0, "reliable": 0}
            }
        }
        
        for committee in committees:
            committee_name = committee.get("name", "Unknown")
            chamber = committee.get("chamber", "Unknown")
            
            # Initialize committee coverage
            committee_coverage = {
                "name": committee_name,
                "chamber": chamber,
                "urls": {},
                "reliable_count": 0,
                "total_count": 0,
                "coverage_score": 0
            }
            
            # Count chamber totals
            if chamber in url_analysis["coverage_by_chamber"]:
                url_analysis["coverage_by_chamber"][chamber]["total"] += 1
            
            # Test each URL type
            url_types = ["hearings_url", "members_url", "official_website_url"]
            for url_type in url_types:
                url = committee.get(url_type)
                if url:
                    print(f"   Testing {committee_name} - {url_type}: {url}")
                    
                    # Test URL reliability
                    result = self.test_url_reliability(url)
                    result["committee"] = committee_name
                    result["chamber"] = chamber
                    result["url_type"] = url_type
                    
                    # Track URL type statistics
                    url_analysis["url_type_analysis"][url_type]["total"] += 1
                    if result["reliable"]:
                        url_analysis["url_type_analysis"][url_type]["reliable"] += 1
                    
                    # Add to appropriate list
                    if result["reliable"]:
                        url_analysis["reliable"].append(result)
                        committee_coverage["reliable_count"] += 1
                    else:
                        url_analysis["unreliable"].append(result)
                    
                    committee_coverage["urls"][url_type] = result
                    committee_coverage["total_count"] += 1
                    
                    # Small delay to be respectful
                    time.sleep(0.5)
            
            # Calculate coverage score
            if committee_coverage["total_count"] > 0:
                committee_coverage["coverage_score"] = round(
                    (committee_coverage["reliable_count"] / committee_coverage["total_count"]) * 100, 1
                )
            
            # Track chamber reliability
            if committee_coverage["reliable_count"] > 0:
                if chamber in url_analysis["coverage_by_chamber"]:
                    url_analysis["coverage_by_chamber"][chamber]["reliable"] += 1
            
            url_analysis["coverage_by_committee"][committee_name] = committee_coverage
        
        return url_analysis
    
    def generate_coverage_report(self, analysis: Dict) -> str:
        """Generate comprehensive coverage gap report."""
        report = []
        report.append("# 📊 Committee URL Coverage and Reliability Report")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        total_urls = len(analysis["reliable"]) + len(analysis["unreliable"])
        reliable_count = len(analysis["reliable"])
        reliability_rate = (reliable_count / total_urls * 100) if total_urls > 0 else 0
        
        report.append("## 📈 Executive Summary")
        report.append(f"- **Total URLs Tested**: {total_urls}")
        report.append(f"- **Reliable URLs**: {reliable_count} ({reliability_rate:.1f}%)")
        report.append(f"- **Unreliable URLs**: {len(analysis['unreliable'])} ({100-reliability_rate:.1f}%)")
        report.append("")
        
        # Chamber Coverage
        report.append("## 🏛️ Coverage by Chamber")
        for chamber, stats in analysis["coverage_by_chamber"].items():
            if stats["total"] > 0:
                chamber_rate = (stats["reliable"] / stats["total"] * 100)
                report.append(f"- **{chamber}**: {stats['reliable']}/{stats['total']} committees ({chamber_rate:.1f}% reliable)")
        report.append("")
        
        # URL Type Analysis
        report.append("## 🔗 URL Type Reliability")
        for url_type, stats in analysis["url_type_analysis"].items():
            if stats["total"] > 0:
                type_rate = (stats["reliable"] / stats["total"] * 100)
                report.append(f"- **{url_type}**: {stats['reliable']}/{stats['total']} ({type_rate:.1f}% reliable)")
        report.append("")
        
        # Committee Coverage Details
        report.append("## 📋 Committee Coverage Details")
        report.append("")
        
        # Sort committees by coverage score
        committees_sorted = sorted(
            analysis["coverage_by_committee"].items(),
            key=lambda x: x[1]["coverage_score"],
            reverse=True
        )
        
        for committee_name, coverage in committees_sorted:
            score = coverage["coverage_score"]
            reliable = coverage["reliable_count"]
            total = coverage["total_count"]
            chamber = coverage["chamber"]
            
            if score >= 75:
                status = "✅ EXCELLENT"
            elif score >= 50:
                status = "⚠️ GOOD"
            elif score > 0:
                status = "❌ POOR"
            else:
                status = "🚫 NO COVERAGE"
            
            report.append(f"### {committee_name} ({chamber})")
            report.append(f"**Status**: {status} - {reliable}/{total} URLs reliable ({score}%)")
            report.append("")
            
            # URL details
            for url_type, url_result in coverage["urls"].items():
                if url_result["reliable"]:
                    report.append(f"- ✅ **{url_type}**: {url_result['url']}")
                else:
                    report.append(f"- ❌ **{url_type}**: {url_result['url']} ({url_result['error']})")
            report.append("")
        
        # Unreliable Sources to Remove
        report.append("## 🚫 Unreliable Sources to Remove from Operations")
        report.append("")
        
        # Group by error type
        error_groups = {}
        for url_result in analysis["unreliable"]:
            error_type = url_result.get("status", "unknown")
            if error_type not in error_groups:
                error_groups[error_type] = []
            error_groups[error_type].append(url_result)
        
        for error_type, urls in error_groups.items():
            report.append(f"### {error_type.upper()} ({len(urls)} URLs)")
            for url_result in urls:
                report.append(f"- {url_result['committee']} ({url_result['chamber']}) - {url_result['url_type']}")
                report.append(f"  URL: {url_result['url']}")
                report.append(f"  Error: {url_result['error']}")
            report.append("")
        
        # Recommendations
        report.append("## 🎯 Operational Recommendations")
        report.append("")
        report.append("### Immediate Actions")
        report.append("1. **Remove Unreliable Sources**: Decommission the URLs listed above from operational crawling")
        report.append("2. **Focus on Reliable Sources**: Prioritize monitoring and enhancement of reliable URLs")
        report.append("3. **Committee Prioritization**: Focus resources on committees with >50% coverage")
        report.append("")
        
        report.append("### Committee Classification")
        excellent = sum(1 for _, c in committees_sorted if c["coverage_score"] >= 75)
        good = sum(1 for _, c in committees_sorted if 50 <= c["coverage_score"] < 75)
        poor = sum(1 for _, c in committees_sorted if 0 < c["coverage_score"] < 50)
        no_coverage = sum(1 for _, c in committees_sorted if c["coverage_score"] == 0)
        
        report.append(f"- **Excellent Coverage** ({excellent} committees): Continue operational monitoring")
        report.append(f"- **Good Coverage** ({good} committees): Attempt to find alternative sources")
        report.append(f"- **Poor Coverage** ({poor} committees): Deprioritize or find alternative sources")
        report.append(f"- **No Coverage** ({no_coverage} committees): May not have public hearings or resources")
        report.append("")
        
        return "\n".join(report)
    
    def create_operational_source_list(self, analysis: Dict) -> List[Dict]:
        """Create clean list of operational sources."""
        operational_sources = []
        
        for url_result in analysis["reliable"]:
            operational_sources.append({
                "committee": url_result["committee"],
                "chamber": url_result["chamber"],
                "url_type": url_result["url_type"],
                "url": url_result["url"],
                "response_time": url_result["response_time"],
                "content_length": url_result["content_length"],
                "last_validated": datetime.now().isoformat()
            })
        
        return operational_sources
    
    def save_results(self, analysis: Dict, report: str, operational_sources: List[Dict]):
        """Save analysis results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full analysis
        with open(f"url_reliability_analysis_{timestamp}.json", "w") as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Save coverage report
        with open(f"committee_coverage_report_{timestamp}.md", "w") as f:
            f.write(report)
        
        # Save operational sources
        with open(f"operational_sources_{timestamp}.json", "w") as f:
            json.dump(operational_sources, f, indent=2, default=str)
        
        print(f"📊 Results saved:")
        print(f"   - url_reliability_analysis_{timestamp}.json")
        print(f"   - committee_coverage_report_{timestamp}.md")
        print(f"   - operational_sources_{timestamp}.json")
    
    def run_analysis(self):
        """Run complete reliability analysis."""
        print("🚀 Phase 3A - Reliable Sources Analysis")
        print("=" * 50)
        
        # Get committee data
        committees = self.get_committee_data()
        if not committees:
            print("❌ No committee data available")
            return
        
        print(f"📋 Found {len(committees)} committees to analyze")
        
        # Analyze URL reliability
        analysis = self.analyze_committee_urls(committees)
        
        # Generate coverage report
        report = self.generate_coverage_report(analysis)
        
        # Create operational source list
        operational_sources = self.create_operational_source_list(analysis)
        
        # Save results
        self.save_results(analysis, report, operational_sources)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 ANALYSIS COMPLETE")
        print("=" * 50)
        
        total_urls = len(analysis["reliable"]) + len(analysis["unreliable"])
        reliable_count = len(analysis["reliable"])
        reliability_rate = (reliable_count / total_urls * 100) if total_urls > 0 else 0
        
        print(f"✅ Reliable URLs: {reliable_count} ({reliability_rate:.1f}%)")
        print(f"❌ Unreliable URLs: {len(analysis['unreliable'])} ({100-reliability_rate:.1f}%)")
        print(f"🎯 Operational Sources: {len(operational_sources)} URLs ready for monitoring")
        
        # Show top unreliable sources
        print("\n🚫 Top Unreliable Source Categories:")
        error_counts = {}
        for url_result in analysis["unreliable"]:
            error_type = url_result.get("status", "unknown")
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {error_type}: {count} URLs")
        
        print(f"\n📋 Detailed coverage report: committee_coverage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        print("🎯 Ready to implement operational monitoring for reliable sources")


def main():
    """Main execution function."""
    analyzer = ReliableSourcesAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()