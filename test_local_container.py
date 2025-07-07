#!/usr/bin/env python3
"""
Test local container to diagnose deployment issue
"""

import subprocess
import sys
import time
import requests
import keyring

def get_secrets():
    """Get required secrets"""
    try:
        congress_api_key = keyring.get_password('memex', 'CONGRESS_API_KEY')
        return {
            'CONGRESS_API_KEY': congress_api_key,
            'SECRET_KEY': 'test-secret-key-for-local-testing',
            'DEBUG': 'false'
        }
    except Exception as e:
        print(f"Error getting secrets: {e}")
        return None

def build_container():
    """Build the container locally"""
    print("=== BUILDING CONTAINER LOCALLY ===")
    
    cmd = [
        "docker", "build", 
        "-t", "congress-api:local-test",
        "-f", "backend/Dockerfile",
        "backend/"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Container built successfully")
        return True
    else:
        print("❌ Container build failed")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False

def test_container():
    """Test container locally with environment variables"""
    print("\n=== TESTING CONTAINER LOCALLY ===")
    
    secrets = get_secrets()
    if not secrets:
        print("❌ Failed to get secrets")
        return False
    
    # Test container startup
    env_vars = [
        f"-e", f"DATABASE_URL=postgresql://postgres:test@localhost:5432/test_db",
        f"-e", f"CONGRESS_API_KEY={secrets['CONGRESS_API_KEY']}",
        f"-e", f"SECRET_KEY={secrets['SECRET_KEY']}",
        f"-e", f"DEBUG={secrets['DEBUG']}",
        f"-e", f"PORT=8000"
    ]
    
    cmd = [
        "docker", "run", "--rm", "-d",
        "-p", "8001:8000",
        "--name", "congress-api-test"
    ] + env_vars + ["congress-api:local-test"]
    
    print(f"Running container with environment variables...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Container failed to start")
        print("STDERR:", result.stderr)
        return False
    
    container_id = result.stdout.strip()
    print(f"✅ Container started with ID: {container_id}")
    
    # Wait a moment for startup
    print("Waiting for container startup...")
    time.sleep(10)
    
    # Check if container is still running
    check_cmd = ["docker", "ps", "-q", "-f", f"id={container_id}"]
    check_result = subprocess.run(check_cmd, capture_output=True, text=True)
    
    if not check_result.stdout.strip():
        print("❌ Container stopped unexpectedly")
        # Get logs
        logs_cmd = ["docker", "logs", container_id]
        logs_result = subprocess.run(logs_cmd, capture_output=True, text=True)
        print("Container logs:")
        print(logs_result.stdout)
        print(logs_result.stderr)
        return False
    
    # Test HTTP endpoint
    try:
        print("Testing HTTP endpoint...")
        response = requests.get("http://localhost:8001/health", timeout=10)
        if response.status_code == 200:
            print("✅ Container HTTP endpoint working")
            print(f"Response: {response.json()}")
            
            # Test API endpoint
            try:
                api_response = requests.get("http://localhost:8001/api/v1/committees?limit=1", timeout=10)
                if api_response.status_code == 200:
                    data = api_response.json()
                    print("✅ API endpoint working")
                    if data:
                        committee = data[0]
                        # Check for URL fields
                        url_fields = ['hearings_url', 'members_url', 'official_website_url']
                        has_url_fields = any(field in committee for field in url_fields)
                        if has_url_fields:
                            print("✅ Enhanced schema with URL fields working!")
                        else:
                            print("⚠️ URL fields not found in response")
                        print(f"Sample committee: {committee.get('name')}")
                        print(f"Fields: {list(committee.keys())}")
                else:
                    print(f"⚠️ API endpoint returned: {api_response.status_code}")
                    print(f"Response text: {api_response.text}")
            except Exception as e:
                print(f"⚠️ API endpoint test failed: {e}")
            
            return True
        else:
            print(f"❌ HTTP endpoint returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP endpoint test failed: {e}")
        return False
    finally:
        # Get container logs before stopping
        logs_cmd = ["docker", "logs", container_id]
        logs_result = subprocess.run(logs_cmd, capture_output=True, text=True)
        if logs_result.stdout or logs_result.stderr:
            print("\n=== CONTAINER LOGS ===")
            if logs_result.stdout:
                print("STDOUT:", logs_result.stdout[-1000:])  # Last 1000 chars
            if logs_result.stderr:
                print("STDERR:", logs_result.stderr[-1000:])  # Last 1000 chars
        
        # Stop container
        stop_cmd = ["docker", "stop", container_id]
        subprocess.run(stop_cmd, capture_output=True)
        print("Container stopped")

def main():
    """Main test function"""
    print("Local Container Testing for Congressional Data API")
    print("Testing enhanced schema deployment issue...\n")
    
    if build_container():
        if test_container():
            print("\n✅ LOCAL CONTAINER TEST PASSED")
            print("The enhanced schema should work in production")
            return True
        else:
            print("\n❌ LOCAL CONTAINER TEST FAILED")
            print("Issue with container startup or API functionality")
            return False
    else:
        print("\n❌ CONTAINER BUILD FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)