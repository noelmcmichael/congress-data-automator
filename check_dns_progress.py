#!/usr/bin/env python3
"""
Monitor DNS propagation and SSL certificate provisioning for politicalequity.io
"""
import subprocess
import time
import sys
from datetime import datetime

def run_cmd(cmd, timeout=10):
    """Run command with timeout."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return None, "Timeout", 124
    except Exception as e:
        return None, str(e), 1

def check_dns_propagation():
    """Check if DNS A record is propagated."""
    print("🔍 Checking DNS propagation...")
    
    # Check with dig
    stdout, stderr, code = run_cmd("dig +short politicalequity.io A")
    
    if code == 0 and stdout:
        ips = [ip.strip() for ip in stdout.split('\n') if ip.strip()]
        if '34.8.118.40' in ips:
            print("✅ DNS A record found: 34.8.118.40")
            return True
        else:
            print(f"⚠️ DNS A record found but wrong IP: {ips}")
            return False
    else:
        print("❌ No DNS A record found yet")
        return False

def check_dns_multiple_servers():
    """Check DNS from multiple servers."""
    print("\n🌐 Checking DNS from multiple servers...")
    
    dns_servers = [
        ("Google DNS", "8.8.8.8"),
        ("Cloudflare DNS", "1.1.1.1"),
        ("Quad9 DNS", "9.9.9.9")
    ]
    
    propagated_count = 0
    
    for name, server in dns_servers:
        stdout, stderr, code = run_cmd(f"dig @{server} +short politicalequity.io A")
        
        if code == 0 and stdout and '34.8.118.40' in stdout:
            print(f"✅ {name} ({server}): Propagated")
            propagated_count += 1
        else:
            print(f"❌ {name} ({server}): Not yet propagated")
    
    return propagated_count, len(dns_servers)

def check_ssl_certificate():
    """Check SSL certificate status."""
    print("\n📜 Checking SSL certificate status...")
    
    stdout, stderr, code = run_cmd("gcloud compute ssl-certificates describe politicalequity-ssl-cert --global --format='value(managed.status,managed.domainStatus.politicalequity.io)'")
    
    if code == 0 and stdout:
        parts = stdout.split('\t')
        overall_status = parts[0] if len(parts) > 0 else "UNKNOWN"
        domain_status = parts[1] if len(parts) > 1 else "UNKNOWN"
        
        print(f"📋 Overall Status: {overall_status}")
        print(f"🌐 Domain Status: {domain_status}")
        
        if overall_status == "ACTIVE" and domain_status == "ACTIVE":
            print("✅ SSL certificate is ACTIVE and ready!")
            return True
        elif "PROVISIONING" in overall_status or "PROVISIONING" in domain_status:
            print("⏳ SSL certificate is provisioning...")
            return False
        else:
            print("⚠️ SSL certificate status unclear")
            return False
    else:
        print("❌ Could not check SSL certificate status")
        return False

def test_domain_response():
    """Test if the domain responds."""
    print("\n🌐 Testing domain response...")
    
    # Test HTTP first (should redirect to HTTPS)
    stdout, stderr, code = run_cmd("curl -I -s --connect-timeout 10 http://politicalequity.io")
    
    if code == 0:
        print("✅ HTTP response received")
        if "301" in stdout or "302" in stdout:
            print("🔀 HTTP redirects to HTTPS (good)")
    else:
        print("❌ No HTTP response yet")
    
    # Test HTTPS
    stdout, stderr, code = run_cmd("curl -I -s --connect-timeout 10 https://politicalequity.io")
    
    if code == 0:
        print("✅ HTTPS response received!")
        if "200" in stdout:
            print("🎉 Domain is fully functional!")
            return True
        else:
            print(f"⚠️ HTTPS responds but status unclear: {stdout[:100]}")
    else:
        print("❌ No HTTPS response yet (SSL may still be provisioning)")
    
    return False

def show_progress_summary(dns_ok, ssl_ok, domain_ok, propagated_count, total_servers):
    """Show progress summary."""
    print("\n📊 PROGRESS SUMMARY")
    print("=" * 25)
    
    dns_status = "✅" if dns_ok else "⏳"
    ssl_status = "✅" if ssl_ok else "⏳"
    domain_status = "✅" if domain_ok else "⏳"
    
    print(f"{dns_status} DNS Propagation: {propagated_count}/{total_servers} servers")
    print(f"{ssl_status} SSL Certificate: {'Ready' if ssl_ok else 'Provisioning'}")
    print(f"{domain_status} Domain Response: {'Working' if domain_ok else 'Not yet'}")
    
    if domain_ok:
        print("\n🎉 DOMAIN IS FULLY ACTIVE!")
        print("🌐 https://politicalequity.io is live!")
    elif ssl_ok and dns_ok:
        print("\n⏳ DNS and SSL ready - testing domain response...")
    elif dns_ok:
        print("\n⏳ DNS propagated - waiting for SSL certificate...")
    else:
        print("\n⏳ Waiting for DNS propagation...")

def main():
    """Main monitoring function."""
    
    print("🎯 POLITICALEQUITY.IO DNS & SSL MONITOR")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Target IP: 34.8.118.40")
    print("=" * 50)
    
    while True:
        print(f"\n🕐 Check at: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 30)
        
        # Check DNS propagation
        dns_ok = check_dns_propagation()
        propagated_count, total_servers = check_dns_multiple_servers()
        
        # Check SSL certificate
        ssl_ok = check_ssl_certificate()
        
        # Test domain response
        domain_ok = test_domain_response()
        
        # Show summary
        show_progress_summary(dns_ok, ssl_ok, domain_ok, propagated_count, total_servers)
        
        # If everything is working, we're done!
        if domain_ok:
            print("\n🎉 MONITORING COMPLETE - DOMAIN IS LIVE!")
            break
        
        # Wait before next check
        print(f"\n⏳ Next check in 2 minutes... (Ctrl+C to stop)")
        try:
            time.sleep(120)  # 2 minutes
        except KeyboardInterrupt:
            print(f"\n\n⏹️ Monitoring stopped by user")
            print("💡 Run this script again anytime to check progress")
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")
        sys.exit(1)