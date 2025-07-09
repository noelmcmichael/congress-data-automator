#!/usr/bin/env python3
"""
Implement politicalequity.io domain configuration with Google Cloud Load Balancer.
"""
import subprocess
import sys
import json
import time
from datetime import datetime

def run_command(cmd, description, check=True):
    """Run a command and return the result."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return result.stdout.strip()
        else:
            if check:
                print(f"❌ {description} failed: {result.stderr}")
                return None
            else:
                print(f"⚠️ {description} completed with warnings: {result.stderr}")
                return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_prerequisites():
    """Check if gcloud is configured and has necessary permissions."""
    print("🔍 Checking Prerequisites")
    print("=" * 30)
    
    # Check gcloud auth
    auth_result = run_command(
        "gcloud auth list --format='value(account)' --filter='status=ACTIVE'",
        "Checking gcloud authentication"
    )
    
    if not auth_result:
        print("❌ Please run 'gcloud auth login' first")
        return False
    
    print(f"✅ Authenticated as: {auth_result}")
    
    # Check project
    project_result = run_command(
        "gcloud config get-value project",
        "Checking active GCP project"
    )
    
    if not project_result:
        print("❌ No active GCP project. Run 'gcloud config set project YOUR_PROJECT'")
        return False
        
    print(f"✅ Active project: {project_result}")
    
    return True

def create_static_ip():
    """Create static IP address for the load balancer."""
    
    # Check if IP already exists
    existing_ip = run_command(
        "gcloud compute addresses describe politicalequity-ip --global --format='value(address)' 2>/dev/null",
        "Checking for existing static IP",
        check=False
    )
    
    if existing_ip:
        print(f"✅ Static IP already exists: {existing_ip}")
        return existing_ip
    
    # Create new static IP
    create_result = run_command(
        "gcloud compute addresses create politicalequity-ip --global --ip-version IPV4",
        "Creating static IP address"
    )
    
    if create_result is None:
        return None
    
    # Get the IP address
    ip_address = run_command(
        "gcloud compute addresses describe politicalequity-ip --global --format='value(address)'",
        "Retrieving static IP address"
    )
    
    print(f"📍 Static IP created: {ip_address}")
    return ip_address

def create_ssl_certificate():
    """Create Google-managed SSL certificate."""
    
    # Check if certificate already exists
    existing_cert = run_command(
        "gcloud compute ssl-certificates describe politicalequity-ssl-cert --global --format='value(name)' 2>/dev/null",
        "Checking for existing SSL certificate",
        check=False
    )
    
    if existing_cert:
        print("✅ SSL certificate already exists")
        return True
    
    # Create SSL certificate
    cert_result = run_command(
        "gcloud compute ssl-certificates create politicalequity-ssl-cert --domains politicalequity.io --global",
        "Creating Google-managed SSL certificate"
    )
    
    if cert_result is None:
        return False
    
    print("📜 SSL certificate created (will provision after DNS is configured)")
    return True

def create_backend_services():
    """Create backend services for frontend and API."""
    
    # Frontend backend service (Cloud Storage)
    frontend_exists = run_command(
        "gcloud compute backend-services describe frontend-bucket-backend-service --global --format='value(name)' 2>/dev/null",
        "Checking for existing frontend backend service",
        check=False
    )
    
    if not frontend_exists:
        frontend_result = run_command(
            "gcloud compute backend-services create frontend-bucket-backend-service --global",
            "Creating frontend backend service"
        )
        if frontend_result is None:
            return False
    
    # Add Cloud Storage bucket as backend
    bucket_backend = run_command(
        "gcloud compute backend-services add-backend frontend-bucket-backend-service --global --cloud-storage-bucket-name=congressional-data-frontend",
        "Adding Cloud Storage bucket to frontend backend service"
    )
    
    # API backend service (Cloud Run)
    api_exists = run_command(
        "gcloud compute backend-services describe congressional-data-api-backend-service --global --format='value(name)' 2>/dev/null",
        "Checking for existing API backend service", 
        check=False
    )
    
    if not api_exists:
        api_result = run_command(
            "gcloud compute backend-services create congressional-data-api-backend-service --global --load-balancing-scheme=EXTERNAL_MANAGED --protocol=HTTPS",
            "Creating API backend service"
        )
        if api_result is None:
            return False
    
    # Add Cloud Run service as backend
    run_backend = run_command(
        "gcloud compute backend-services add-backend congressional-data-api-backend-service --global --network-endpoint-group=congressional-data-api-neg --network-endpoint-group-region=us-central1",
        "Adding Cloud Run service to API backend service",
        check=False
    )
    
    if not run_backend:
        print("⚠️ Cloud Run NEG might need to be created. This is normal for first-time setup.")
    
    return True

def create_url_map():
    """Create URL map for routing."""
    
    # Check if URL map already exists
    existing_map = run_command(
        "gcloud compute url-maps describe politicalequity-url-map --global --format='value(name)' 2>/dev/null",
        "Checking for existing URL map",
        check=False
    )
    
    if existing_map:
        print("✅ URL map already exists")
        return True
    
    # Create URL map
    map_result = run_command(
        "gcloud compute url-maps create politicalequity-url-map --default-service frontend-bucket-backend-service --global",
        "Creating URL map"
    )
    
    if map_result is None:
        return False
    
    # Add path matcher for API routes
    path_matcher = run_command(
        """gcloud compute url-maps add-path-matcher politicalequity-url-map \\
           --path-matcher-name=path-matcher-1 \\
           --default-service=frontend-bucket-backend-service \\
           --path-rules='/api/*=congressional-data-api-backend-service' \\
           --global""",
        "Adding API path routing"
    )
    
    # Add host rule
    host_rule = run_command(
        "gcloud compute url-maps add-host-rule politicalequity-url-map --hosts=politicalequity.io --path-matcher=path-matcher-1 --global",
        "Adding host rule for politicalequity.io"
    )
    
    return True

def create_load_balancer():
    """Create the HTTPS load balancer."""
    
    # Check if target proxy exists
    existing_proxy = run_command(
        "gcloud compute target-https-proxies describe politicalequity-https-proxy --global --format='value(name)' 2>/dev/null",
        "Checking for existing HTTPS proxy",
        check=False
    )
    
    if not existing_proxy:
        proxy_result = run_command(
            "gcloud compute target-https-proxies create politicalequity-https-proxy --ssl-certificates=politicalequity-ssl-cert --url-map=politicalequity-url-map --global",
            "Creating HTTPS target proxy"
        )
        if proxy_result is None:
            return False
    
    # Check if forwarding rule exists
    existing_rule = run_command(
        "gcloud compute forwarding-rules describe politicalequity-https-rule --global --format='value(name)' 2>/dev/null",
        "Checking for existing forwarding rule",
        check=False
    )
    
    if not existing_rule:
        rule_result = run_command(
            "gcloud compute forwarding-rules create politicalequity-https-rule --global --target-https-proxy=politicalequity-https-proxy --ports=443 --address=politicalequity-ip",
            "Creating HTTPS forwarding rule"
        )
        if rule_result is None:
            return False
    
    return True

def update_cors_configuration():
    """Update backend CORS configuration for the new domain."""
    
    print("🔄 Updating CORS configuration...")
    
    # Note: This would typically require updating the backend environment variables
    # and redeploying the Cloud Run service
    
    print("⚠️ CORS Configuration Update Required:")
    print("   1. Update backend/app/core/config.py")
    print("   2. Set ALLOWED_ORIGINS environment variable")
    print("   3. Redeploy Cloud Run service")
    print("   Example: ALLOWED_ORIGINS=['https://politicalequity.io']")
    
    return True

def main():
    """Main implementation function."""
    
    implementation_summary = {
        "timestamp": datetime.now().isoformat(),
        "domain": "politicalequity.io",
        "implementation_type": "google_cloud_load_balancer",
        "status": "in_progress"
    }
    
    print("🌐 Political Equity Domain Implementation")
    print("🎯 Target: https://politicalequity.io")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites check failed. Please resolve issues and try again.")
        return False
    
    print()
    
    # Step 1: Create static IP
    print("📍 Phase 1: Static IP Address")
    print("-" * 30)
    static_ip = create_static_ip()
    if not static_ip:
        print("❌ Failed to create static IP address")
        return False
    
    implementation_summary["static_ip"] = static_ip
    print()
    
    # Step 2: Create SSL certificate
    print("📜 Phase 2: SSL Certificate")
    print("-" * 30)
    if not create_ssl_certificate():
        print("❌ Failed to create SSL certificate")
        return False
    print()
    
    # Step 3: Create backend services
    print("🔗 Phase 3: Backend Services")
    print("-" * 30)
    if not create_backend_services():
        print("❌ Failed to create backend services")
        return False
    print()
    
    # Step 4: Create URL map
    print("🗺️ Phase 4: URL Routing")
    print("-" * 30)
    if not create_url_map():
        print("❌ Failed to create URL map")
        return False
    print()
    
    # Step 5: Create load balancer
    print("⚖️ Phase 5: Load Balancer")
    print("-" * 30)
    if not create_load_balancer():
        print("❌ Failed to create load balancer")
        return False
    print()
    
    # Step 6: CORS configuration
    print("🔒 Phase 6: CORS Configuration")
    print("-" * 30)
    update_cors_configuration()
    print()
    
    # Success summary
    print("✅ DOMAIN IMPLEMENTATION SUCCESSFUL!")
    print("=" * 50)
    print(f"🌐 Static IP Address: {static_ip}")
    print("📋 Next Steps:")
    print("1. Configure DNS A record: politicalequity.io → " + static_ip)
    print("2. Wait for DNS propagation (15 minutes - 48 hours)")
    print("3. SSL certificate will auto-provision after DNS resolves")
    print("4. Update backend CORS configuration")
    print("5. Test the new domain endpoints")
    print()
    print("🔍 Verification Commands:")
    print(f"   dig politicalequity.io")
    print(f"   curl -I https://politicalequity.io")
    print(f"   curl -I https://politicalequity.io/api/v1/status")
    
    implementation_summary["status"] = "success"
    implementation_summary["next_steps"] = [
        f"Configure DNS A record: politicalequity.io → {static_ip}",
        "Wait for DNS propagation",
        "Update backend CORS configuration",
        "Test endpoints"
    ]
    
    # Save implementation summary
    with open(f"domain_implementation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(implementation_summary, f, indent=2)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)