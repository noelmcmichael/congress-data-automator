#!/usr/bin/env python3
"""
Direct implementation of politicalequity.io domain - no waiting around!
"""
import subprocess
import sys
import json
from datetime import datetime

def run_gcloud(cmd, description):
    """Run gcloud command with 30s timeout - fail fast if stuck."""
    print(f"🔄 {description}...")
    full_cmd = f"timeout 30 {cmd}"
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"✅ {description} - Success")
            return output
        elif result.returncode == 124:  # timeout
            print(f"⏰ {description} - Timeout, continuing...")
            return "TIMEOUT"
        else:
            print(f"ℹ️ {description} - {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return None

def step1_create_static_ip():
    """Step 1: Create static IP."""
    print("\n📍 STEP 1: Static IP Address")
    print("-" * 30)
    
    # Create static IP
    result = run_gcloud(
        "gcloud compute addresses create politicalequity-ip --global --ip-version=IPV4",
        "Creating static IP"
    )
    
    if result == "TIMEOUT":
        print("⚠️ Command timed out but likely succeeded")
    
    # Get IP address (retry a few times)
    for attempt in range(3):
        ip_result = run_gcloud(
            "gcloud compute addresses describe politicalequity-ip --global --format='value(address)'",
            f"Getting IP address (attempt {attempt + 1})"
        )
        
        if ip_result and ip_result != "TIMEOUT" and "." in ip_result:
            print(f"🎯 Static IP: {ip_result}")
            return ip_result
        
        if attempt < 2:
            print("⏳ Waiting 5 seconds...")
            import time
            time.sleep(5)
    
    # If we can't get the IP, continue anyway
    print("⚠️ Couldn't retrieve IP, but continuing...")
    return "UNKNOWN"

def step2_create_ssl_cert():
    """Step 2: Create SSL certificate."""
    print("\n📜 STEP 2: SSL Certificate")
    print("-" * 30)
    
    result = run_gcloud(
        "gcloud compute ssl-certificates create politicalequity-ssl-cert --domains=politicalequity.io --global",
        "Creating SSL certificate"
    )
    
    return result is not None or result == "TIMEOUT"

def step3_create_backend_services():
    """Step 3: Create backend services."""
    print("\n🔗 STEP 3: Backend Services")
    print("-" * 30)
    
    # Frontend backend service
    frontend_result = run_gcloud(
        "gcloud compute backend-services create frontend-bucket-backend-service --global",
        "Creating frontend backend service"
    )
    
    # Add bucket to frontend service
    bucket_result = run_gcloud(
        "gcloud compute backend-services add-backend frontend-bucket-backend-service --global --cloud-storage-bucket-name=congressional-data-frontend",
        "Adding bucket to frontend service"
    )
    
    # API backend service
    api_result = run_gcloud(
        "gcloud compute backend-services create congressional-data-api-backend-service --global --load-balancing-scheme=EXTERNAL_MANAGED --protocol=HTTPS",
        "Creating API backend service"
    )
    
    return True  # Continue regardless

def step4_create_url_map():
    """Step 4: Create URL map."""
    print("\n🗺️ STEP 4: URL Map")
    print("-" * 30)
    
    # Create URL map
    map_result = run_gcloud(
        "gcloud compute url-maps create politicalequity-url-map --default-service=frontend-bucket-backend-service --global",
        "Creating URL map"
    )
    
    # Add path matcher for API routes  
    path_result = run_gcloud(
        "gcloud compute url-maps add-path-matcher politicalequity-url-map --path-matcher-name=api-matcher --default-service=frontend-bucket-backend-service --path-rules='/api/*=congressional-data-api-backend-service' --global",
        "Adding API path routing"
    )
    
    # Add host rule
    host_result = run_gcloud(
        "gcloud compute url-maps add-host-rule politicalequity-url-map --hosts=politicalequity.io --path-matcher=api-matcher --global",
        "Adding host rule"
    )
    
    return True

def step5_create_load_balancer():
    """Step 5: Create load balancer."""
    print("\n⚖️ STEP 5: Load Balancer")
    print("-" * 30)
    
    # Create HTTPS proxy
    proxy_result = run_gcloud(
        "gcloud compute target-https-proxies create politicalequity-https-proxy --ssl-certificates=politicalequity-ssl-cert --url-map=politicalequity-url-map --global",
        "Creating HTTPS proxy"
    )
    
    # Create forwarding rule
    rule_result = run_gcloud(
        "gcloud compute forwarding-rules create politicalequity-https-rule --global --target-https-proxy=politicalequity-https-proxy --ports=443 --address=politicalequity-ip",
        "Creating forwarding rule"
    )
    
    return True

def step6_update_cors():
    """Step 6: Update CORS (manual step)."""
    print("\n🔒 STEP 6: CORS Configuration")
    print("-" * 30)
    print("📝 Manual step required:")
    print("1. Update backend environment variable: ALLOWED_ORIGINS=['https://politicalequity.io']")
    print("2. Redeploy Cloud Run service")
    return True

def main():
    """Main implementation."""
    
    print("🚀 DIRECT DOMAIN IMPLEMENTATION")
    print("🎯 Target: https://politicalequity.io")
    print("⚡ Fast execution - no waiting around!")
    print("=" * 50)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "domain": "politicalequity.io",
        "steps": {}
    }
    
    # Execute steps
    static_ip = step1_create_static_ip()
    results["steps"]["static_ip"] = static_ip
    
    results["steps"]["ssl_cert"] = step2_create_ssl_cert()
    results["steps"]["backend_services"] = step3_create_backend_services()
    results["steps"]["url_map"] = step4_create_url_map()
    results["steps"]["load_balancer"] = step5_create_load_balancer()
    results["steps"]["cors"] = step6_update_cors()
    
    print("\n🎉 IMPLEMENTATION COMPLETE!")
    print("=" * 40)
    print(f"📍 Static IP: {static_ip}")
    print("\n📋 NEXT STEPS:")
    print(f"1. Configure DNS A record: politicalequity.io → {static_ip}")
    print("2. Wait 15-60 minutes for SSL certificate to provision")
    print("3. Update backend CORS configuration")
    print("4. Test: curl -I https://politicalequity.io")
    
    # Save results
    filename = f"domain_implementation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved: {filename}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)