#!/usr/bin/env python3
"""
Assess current GCP setup for domain configuration planning.
"""
import subprocess
import sys
import json
from datetime import datetime

def run_command(cmd, description, check=False):
    """Run a command and return the result safely."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print(f"✅ {description}: {output}")
            else:
                print(f"✅ {description}: (empty result)")
            return output
        else:
            print(f"ℹ️ {description}: Not found or not configured")
            return None
    except subprocess.TimeoutExpired:
        print(f"⏰ {description}: Timeout (10s)")
        return None
    except Exception as e:
        print(f"❌ {description}: Error - {e}")
        return None

def assess_gcp_environment():
    """Assess the current GCP environment."""
    
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "gcp_config": {},
        "existing_resources": {},
        "cloud_run_services": {},
        "storage_buckets": {},
        "recommendations": []
    }
    
    print("🔍 GCP Environment Assessment")
    print("=" * 40)
    
    # Basic GCP configuration
    print("\n📋 Basic Configuration")
    print("-" * 25)
    
    account = run_command("gcloud auth list --format='value(account)' --filter='status=ACTIVE'", "Active account")
    project = run_command("gcloud config get-value project", "Active project")
    region = run_command("gcloud config get-value compute/region", "Default region")
    zone = run_command("gcloud config get-value compute/zone", "Default zone")
    
    assessment["gcp_config"] = {
        "account": account,
        "project": project,
        "region": region,
        "zone": zone
    }
    
    # Check existing compute resources
    print("\n🖥️ Compute Resources")
    print("-" * 20)
    
    # Static IPs
    static_ips = run_command("gcloud compute addresses list --global --format='value(name,address)'", "Global static IPs")
    if static_ips:
        assessment["existing_resources"]["static_ips"] = static_ips.split('\n')
    
    # SSL certificates
    ssl_certs = run_command("gcloud compute ssl-certificates list --format='value(name,domains)'", "SSL certificates")
    if ssl_certs:
        assessment["existing_resources"]["ssl_certificates"] = ssl_certs.split('\n')
    
    # Load balancers
    url_maps = run_command("gcloud compute url-maps list --format='value(name)'", "URL maps")
    if url_maps:
        assessment["existing_resources"]["url_maps"] = url_maps.split('\n')
    
    target_proxies = run_command("gcloud compute target-https-proxies list --format='value(name)'", "HTTPS proxies")
    if target_proxies:
        assessment["existing_resources"]["target_proxies"] = target_proxies.split('\n')
    
    forwarding_rules = run_command("gcloud compute forwarding-rules list --global --format='value(name,IPAddress)'", "Forwarding rules")
    if forwarding_rules:
        assessment["existing_resources"]["forwarding_rules"] = forwarding_rules.split('\n')
    
    backend_services = run_command("gcloud compute backend-services list --format='value(name,backends[].group)'", "Backend services")
    if backend_services:
        assessment["existing_resources"]["backend_services"] = backend_services.split('\n')
    
    # Check Cloud Run services
    print("\n🏃 Cloud Run Services")
    print("-" * 20)
    
    cloud_run_services = run_command("gcloud run services list --format='value(SERVICE,URL,REGION)'", "Cloud Run services")
    if cloud_run_services:
        services = []
        for service_line in cloud_run_services.split('\n'):
            if service_line.strip():
                parts = service_line.split('\t')
                if len(parts) >= 3:
                    services.append({
                        "name": parts[0],
                        "url": parts[1], 
                        "region": parts[2]
                    })
        assessment["cloud_run_services"] = services
    
    # Check Storage buckets
    print("\n🪣 Storage Buckets")
    print("-" * 17)
    
    storage_buckets = run_command("gsutil ls -b", "Storage buckets")
    if storage_buckets:
        buckets = []
        for bucket_line in storage_buckets.split('\n'):
            if bucket_line.strip() and bucket_line.startswith('gs://'):
                bucket_name = bucket_line.replace('gs://', '').rstrip('/')
                buckets.append(bucket_name)
        assessment["storage_buckets"] = buckets
    
    # Check specific resources we care about
    print("\n🎯 Congressional Data Resources")
    print("-" * 32)
    
    # Check for our specific bucket
    bucket_check = run_command("gsutil ls gs://congressional-data-frontend/", "Frontend bucket contents")
    if bucket_check:
        assessment["frontend_bucket_status"] = "active"
        print("✅ Frontend bucket is active and contains files")
    
    # Check for our API service
    api_check = run_command("gcloud run services describe congressional-data-api-v2 --region=us-central1 --format='value(status.url)' 2>/dev/null", "API service status")
    if api_check:
        assessment["api_service_url"] = api_check
        print(f"✅ API service is active: {api_check}")
    
    return assessment

def analyze_assessment(assessment):
    """Analyze the assessment and provide recommendations."""
    
    print("\n📊 Assessment Analysis")
    print("=" * 25)
    
    recommendations = []
    readiness_score = 0
    max_score = 10
    
    # Check project setup
    if assessment["gcp_config"].get("project"):
        print("✅ GCP project configured")
        readiness_score += 2
    else:
        print("❌ No GCP project configured")
        recommendations.append("Set GCP project: gcloud config set project YOUR_PROJECT")
    
    # Check authentication
    if assessment["gcp_config"].get("account"):
        print("✅ GCP authentication active")
        readiness_score += 1
    else:
        print("❌ No active GCP authentication")
        recommendations.append("Authenticate: gcloud auth login")
    
    # Check existing resources
    if assessment["existing_resources"].get("static_ips"):
        print("ℹ️ Existing static IPs found - may need cleanup or reuse")
        recommendations.append("Review existing static IPs before creating new ones")
    else:
        print("✅ No conflicting static IPs")
        readiness_score += 1
    
    if assessment["existing_resources"].get("ssl_certificates"):
        print("ℹ️ Existing SSL certificates found - check for conflicts")
        recommendations.append("Review existing SSL certificates")
    else:
        print("✅ No conflicting SSL certificates")
        readiness_score += 1
    
    # Check application resources
    if assessment.get("frontend_bucket_status") == "active":
        print("✅ Frontend bucket operational")
        readiness_score += 2
    else:
        print("❌ Frontend bucket not accessible")
        recommendations.append("Verify frontend bucket: gs://congressional-data-frontend/")
    
    if assessment.get("api_service_url"):
        print("✅ API service operational")
        readiness_score += 2
    else:
        print("❌ API service not accessible")
        recommendations.append("Verify API service deployment in us-central1")
    
    # Check for region consistency
    cloud_run_regions = [s.get("region") for s in assessment.get("cloud_run_services", [])]
    if "us-central1" in cloud_run_regions:
        print("✅ Services deployed in us-central1")
        readiness_score += 1
    else:
        print("⚠️ Services not in expected region (us-central1)")
        recommendations.append("Ensure services are in us-central1 for optimal routing")
    
    # Overall readiness
    print(f"\n🎯 Readiness Score: {readiness_score}/{max_score}")
    
    if readiness_score >= 8:
        print("🟢 READY for domain implementation")
        implementation_strategy = "direct_implementation"
    elif readiness_score >= 6:
        print("🟡 MOSTLY READY - minor issues to resolve")
        implementation_strategy = "staged_implementation"
    else:
        print("🔴 NOT READY - significant issues to resolve")
        implementation_strategy = "fix_issues_first"
    
    assessment["readiness_score"] = readiness_score
    assessment["implementation_strategy"] = implementation_strategy
    assessment["recommendations"] = recommendations
    
    return assessment

def create_implementation_plan(assessment):
    """Create a tailored implementation plan based on assessment."""
    
    print(f"\n📋 Implementation Plan ({assessment['implementation_strategy']})")
    print("=" * 40)
    
    if assessment["implementation_strategy"] == "direct_implementation":
        print("🚀 Direct Implementation Approach")
        print("1. Create static IP address")
        print("2. Create SSL certificate for politicalequity.io")
        print("3. Create backend services (frontend bucket + API service)")
        print("4. Create URL map with path routing (/api/* → API, /* → frontend)")
        print("5. Create HTTPS load balancer")
        print("6. Update DNS A record")
        print("7. Update CORS configuration")
        print("8. Test and validate")
        
    elif assessment["implementation_strategy"] == "staged_implementation":
        print("🏗️ Staged Implementation Approach")
        print("Phase 1 - Resolve Issues:")
        for rec in assessment["recommendations"]:
            print(f"  - {rec}")
        print("\nPhase 2 - Infrastructure Setup:")
        print("  - Create load balancer components")
        print("  - Test in staging mode")
        print("\nPhase 3 - DNS Cutover:")
        print("  - Update DNS records")
        print("  - Monitor and validate")
        
    else:
        print("🔧 Fix Issues First")
        print("Critical issues must be resolved:")
        for rec in assessment["recommendations"]:
            print(f"  ❗ {rec}")
        print("\nRe-run assessment after fixing issues")
    
    # Estimated timeline
    if assessment["implementation_strategy"] == "direct_implementation":
        print(f"\n⏱️ Estimated Timeline: 2-3 hours")
    elif assessment["implementation_strategy"] == "staged_implementation":
        print(f"\n⏱️ Estimated Timeline: 3-4 hours")
    else:
        print(f"\n⏱️ Estimated Timeline: Fix issues first, then 2-3 hours")

def main():
    """Main assessment function."""
    
    print("🏗️ Congressional Data Automator - GCP Assessment")
    print("🎯 Preparing for politicalequity.io domain implementation")
    print()
    
    # Run assessment
    assessment = assess_gcp_environment()
    
    # Analyze results
    final_assessment = analyze_assessment(assessment)
    
    # Create implementation plan
    create_implementation_plan(final_assessment)
    
    # Save assessment
    filename = f"gcp_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(final_assessment, f, indent=2)
    
    print(f"\n💾 Assessment saved to: {filename}")
    
    return final_assessment

if __name__ == "__main__":
    assessment = main()
    sys.exit(0)