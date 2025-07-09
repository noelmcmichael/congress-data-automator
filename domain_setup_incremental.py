#!/usr/bin/env python3
"""
Incremental domain setup with proper error handling and API enablement.
"""
import subprocess
import sys
import time
from datetime import datetime

def run_cmd(cmd, description, required=True):
    """Run command with better error handling."""
    print(f"🔄 {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"✅ Success: {output[:100]}{'...' if len(output) > 100 else ''}")
            return output
        else:
            error = result.stderr.strip()
            print(f"❌ Failed: {error[:200]}{'...' if len(error) > 200 else ''}")
            if required:
                return None
            return "FAILED_BUT_CONTINUING"
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout after 60 seconds")
        if required:
            return None
        return "TIMEOUT"
    except Exception as e:
        print(f"💥 Exception: {e}")
        return None

def check_current_status():
    """Check what's already configured."""
    print("🔍 CHECKING CURRENT STATUS")
    print("=" * 40)
    
    # Check project
    project = run_cmd("gcloud config get-value project", "Getting current project", required=False)
    
    # Check enabled APIs
    apis = run_cmd("gcloud services list --enabled --format='value(name)' | grep -E '(compute|dns|certificatemanager)'", "Checking enabled APIs", required=False)
    
    return {
        "project": project,
        "apis": apis.split('\n') if apis else []
    }

def enable_required_apis():
    """Enable required Google Cloud APIs."""
    print("\n🔧 ENABLING REQUIRED APIs")
    print("=" * 30)
    
    apis_to_enable = [
        "compute.googleapis.com",
        "dns.googleapis.com", 
        "certificatemanager.googleapis.com"
    ]
    
    for api in apis_to_enable:
        result = run_cmd(
            f"gcloud services enable {api} --quiet",
            f"Enabling {api}",
            required=False
        )
        
        if result:
            print(f"✅ {api} enabled")
        else:
            print(f"⚠️ {api} may already be enabled or failed")
    
    # Wait for APIs to propagate
    print("⏳ Waiting 30 seconds for APIs to propagate...")
    time.sleep(30)

def create_static_ip():
    """Create static IP address."""
    print("\n📍 CREATING STATIC IP")
    print("=" * 25)
    
    # Check if already exists
    existing = run_cmd(
        "gcloud compute addresses describe politicalequity-ip --global --format='value(address)' 2>/dev/null",
        "Checking existing IP",
        required=False
    )
    
    if existing and existing != "FAILED_BUT_CONTINUING":
        print(f"✅ Static IP already exists: {existing}")
        return existing
    
    # Create new IP
    create_result = run_cmd(
        "gcloud compute addresses create politicalequity-ip --global --ip-version=IPV4 --quiet",
        "Creating static IP"
    )
    
    if not create_result:
        return None
    
    # Get the IP
    ip_address = run_cmd(
        "gcloud compute addresses describe politicalequity-ip --global --format='value(address)'",
        "Getting IP address"
    )
    
    return ip_address

def create_ssl_certificate():
    """Create SSL certificate."""
    print("\n📜 CREATING SSL CERTIFICATE")
    print("=" * 30)
    
    # Check if already exists
    existing = run_cmd(
        "gcloud compute ssl-certificates describe politicalequity-ssl-cert --global --format='value(name)' 2>/dev/null",
        "Checking existing certificate",
        required=False
    )
    
    if existing and existing != "FAILED_BUT_CONTINUING":
        print("✅ SSL certificate already exists")
        return True
    
    # Create certificate
    cert_result = run_cmd(
        "gcloud compute ssl-certificates create politicalequity-ssl-cert --domains=politicalequity.io --global --quiet",
        "Creating SSL certificate"
    )
    
    return cert_result is not None

def test_basic_commands():
    """Test basic gcloud commands work."""
    print("\n🧪 TESTING BASIC COMMANDS")
    print("=" * 30)
    
    # Test compute API
    test1 = run_cmd(
        "gcloud compute regions list --limit=1 --format='value(name)'",
        "Testing Compute API",
        required=False
    )
    
    # Test current resources
    test2 = run_cmd(
        "gcloud compute addresses list --global --format='value(name)' --limit=5",
        "Listing current IPs",
        required=False
    )
    
    return test1 is not None and test2 is not None

def main():
    """Main incremental setup."""
    
    print("🚀 INCREMENTAL DOMAIN SETUP")
    print("🎯 Target: politicalequity.io")
    print("📅 Started:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "steps_completed": [],
        "static_ip": None,
        "ssl_cert": False
    }
    
    # Step 1: Check current status
    status = check_current_status()
    results["initial_status"] = status
    
    if not status["project"]:
        print("❌ No GCP project configured. Run: gcloud config set project YOUR_PROJECT")
        return False
    
    print(f"✅ Working with project: {status['project']}")
    
    # Step 2: Enable APIs
    enable_required_apis()
    results["steps_completed"].append("apis_enabled")
    
    # Step 3: Test basic commands
    if not test_basic_commands():
        print("❌ Basic API tests failed. Check API enablement.")
        return False
    
    results["steps_completed"].append("api_tests_passed")
    
    # Step 4: Create static IP
    static_ip = create_static_ip()
    if static_ip:
        results["static_ip"] = static_ip
        results["steps_completed"].append("static_ip_created")
        print(f"🎯 Static IP: {static_ip}")
    else:
        print("❌ Failed to create static IP")
        return False
    
    # Step 5: Create SSL certificate
    ssl_success = create_ssl_certificate()
    if ssl_success:
        results["ssl_cert"] = True
        results["steps_completed"].append("ssl_cert_created")
    else:
        print("❌ Failed to create SSL certificate")
        return False
    
    # Success summary
    print("\n✅ INCREMENTAL SETUP COMPLETE!")
    print("=" * 40)
    print(f"📍 Static IP: {static_ip}")
    print("📜 SSL Certificate: Created (will provision after DNS)")
    print("\n📋 NEXT IMMEDIATE STEPS:")
    print(f"1. Configure DNS: politicalequity.io A record → {static_ip}")
    print("2. Continue with backend services and load balancer")
    print("3. Update CORS configuration")
    
    # Save results
    filename = f"incremental_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        import json
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results: {filename}")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Ready for next phase!")
    else:
        print("\n❌ Setup incomplete - check errors above")
    sys.exit(0 if success else 1)