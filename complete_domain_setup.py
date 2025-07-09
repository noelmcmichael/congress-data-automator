#!/usr/bin/env python3
"""
Complete the domain setup - we have IP and SSL cert, now finish the load balancer.
"""
import subprocess
import sys
import json
from datetime import datetime

def run_cmd(cmd, description):
    """Run command and return result."""
    print(f"🔄 {description}")
    print(f"   {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ Success")
            return True
        else:
            error = result.stderr.strip()
            if "already exists" in error:
                print(f"ℹ️ Already exists - continuing")
                return True
            print(f"❌ Error: {error}")
            return False
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False

def complete_load_balancer_setup():
    """Complete the load balancer configuration."""
    
    print("⚖️ COMPLETING LOAD BALANCER SETUP")
    print("=" * 40)
    
    # Step 1: Create URL map pointing to the backend bucket for frontend
    success1 = run_cmd(
        "gcloud compute url-maps create politicalequity-url-map --default-backend-bucket=congressional-data-frontend-bucket --global",
        "Creating URL map with frontend bucket as default"
    )
    
    # Step 2: Create API backend service for Cloud Run
    success2 = run_cmd(
        "gcloud compute backend-services create api-backend-service --global --load-balancing-scheme=EXTERNAL_MANAGED --protocol=HTTPS",
        "Creating API backend service"
    )
    
    # Step 3: Add path rule for API routes (point to a simple redirect for now)
    success3 = run_cmd(
        "gcloud compute url-maps add-path-matcher politicalequity-url-map --path-matcher-name=api-matcher --default-backend-bucket=congressional-data-frontend-bucket --path-rules='/api/*=api-backend-service' --global",
        "Adding API path routing"
    )
    
    # Step 4: Add host rule
    success4 = run_cmd(
        "gcloud compute url-maps add-host-rule politicalequity-url-map --hosts=politicalequity.io --path-matcher=api-matcher --global",
        "Adding host rule for politicalequity.io"
    )
    
    # Step 5: Create HTTPS proxy
    success5 = run_cmd(
        "gcloud compute target-https-proxies create politicalequity-https-proxy --ssl-certificates=politicalequity-ssl-cert --url-map=politicalequity-url-map --global",
        "Creating HTTPS target proxy"
    )
    
    # Step 6: Create forwarding rule
    success6 = run_cmd(
        "gcloud compute forwarding-rules create politicalequity-https-rule --global --target-https-proxy=politicalequity-https-proxy --ports=443 --address=politicalequity-ip",
        "Creating HTTPS forwarding rule"
    )
    
    return all([success1, success2, success3, success4, success5, success6])

def test_configuration():
    """Test the current configuration."""
    print("\n🧪 TESTING CONFIGURATION")
    print("=" * 30)
    
    # Get the static IP
    try:
        result = subprocess.run(
            "gcloud compute addresses describe politicalequity-ip --global --format='value(address)'",
            shell=True, capture_output=True, text=True
        )
        static_ip = result.stdout.strip()
        print(f"📍 Static IP: {static_ip}")
        
        # Test if IP responds (it won't work until DNS is configured, but we can check)
        print(f"🌐 Once DNS is configured, test with:")
        print(f"   curl -I https://politicalequity.io")
        print(f"   curl -I https://politicalequity.io/api/v1/status")
        
        return static_ip
    except Exception as e:
        print(f"❌ Could not get static IP: {e}")
        return None

def show_dns_configuration(static_ip):
    """Show DNS configuration instructions."""
    print("\n📋 DNS CONFIGURATION REQUIRED")
    print("=" * 35)
    print("Configure your domain registrar with:")
    print(f"   Type: A")
    print(f"   Name: politicalequity.io")
    print(f"   Value: {static_ip}")
    print(f"   TTL: 300 (for quick changes)")
    print()
    print("📜 SSL Certificate Status:")
    print("   - Certificate created and will auto-provision after DNS resolves")
    print("   - Usually takes 15-60 minutes after DNS propagation")
    print("   - Check status: gcloud compute ssl-certificates describe politicalequity-ssl-cert --global")

def show_cors_update():
    """Show CORS update instructions."""
    print("\n🔒 CORS CONFIGURATION UPDATE")
    print("=" * 33)
    print("Update your backend to allow the new domain:")
    print()
    print("1. Update environment variable:")
    print("   ALLOWED_ORIGINS=['https://politicalequity.io','https://storage.googleapis.com']")
    print()
    print("2. Redeploy Cloud Run service:")
    print("   gcloud run deploy congressional-data-api-v2 --region=us-central1")

def main():
    """Main completion function."""
    
    print("🎯 COMPLETING POLITICALEQUITY.IO DOMAIN SETUP")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Complete load balancer setup
    lb_success = complete_load_balancer_setup()
    
    if not lb_success:
        print("❌ Load balancer setup incomplete")
        return False
    
    # Test configuration
    static_ip = test_configuration()
    
    if not static_ip:
        print("❌ Could not verify configuration")
        return False
    
    # Show next steps
    show_dns_configuration(static_ip)
    show_cors_update()
    
    # Success summary
    print("\n🎉 DOMAIN SETUP COMPLETE!")
    print("=" * 30)
    print("✅ Static IP: Created")
    print("✅ SSL Certificate: Created (provisioning)")
    print("✅ Load Balancer: Configured")
    print("✅ Frontend Routing: politicalequity.io → Cloud Storage")
    print("⚠️ API Routing: /api/* configured but needs backend connection")
    
    print(f"\n📍 Static IP: {static_ip}")
    print("📋 Immediate Action Required: Configure DNS A record")
    
    # Save completion summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "status": "load_balancer_complete",
        "static_ip": static_ip,
        "next_steps": [
            f"Configure DNS: politicalequity.io A → {static_ip}",
            "Wait for DNS propagation (15 min - 48 hours)",
            "Update backend CORS configuration",
            "Test endpoints"
        ]
    }
    
    filename = f"domain_setup_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Summary saved: {filename}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)