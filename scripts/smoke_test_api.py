"""
Smoke test for API deployment verification.

This script:
1. Sends a single prediction request to the API
2. Verifies the service returns 200 OK
3. Validates the response format

This is the critical "Deployment Test" that proves the application
works from a user's perspective.
"""
import sys
import requests
import time
from typing import Dict, Any


API_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{API_URL}/health"
PREDICT_ENDPOINT = f"{API_URL}/predict"


def check_health(max_retries: int = 5, retry_delay: int = 2) -> bool:
    """
    Check if the API health endpoint is responding.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    
    Returns:
        True if health check passes, False otherwise
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=5)
            if response.status_code == 200:
                print(f"✅ Health check passed: {response.json()}")
                return True
            else:
                print(f"⚠️  Health check returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"⏳ Health check attempt {attempt + 1}/{max_retries} failed, retrying...")
                time.sleep(retry_delay)
            else:
                print(f"❌ Health check failed after {max_retries} attempts: {e}")
                return False
    
    return False


def send_prediction_request(features: Dict[str, Any]) -> requests.Response:
    """
    Send a prediction request to the API.
    
    Args:
        features: Feature dictionary to send
    
    Returns:
        Response object
    """
    payload = {"features": features}
    response = requests.post(PREDICT_ENDPOINT, json=payload, timeout=10)
    return response


def validate_response(response: requests.Response) -> bool:
    """
    Validate that the response is correct.
    
    Args:
        response: Response object to validate
    
    Returns:
        True if validation passes, False otherwise
    """
    if response.status_code != 200:
        print(f"❌ Request failed with status code: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    try:
        data = response.json()
        
        # Check required fields
        if 'click_probability' not in data:
            print("❌ Missing 'click_probability' in response")
            return False
        
        if 'click_prediction' not in data:
            print("❌ Missing 'click_prediction' in response")
            return False
        
        # Validate types and ranges
        proba = data['click_probability']
        if not isinstance(proba, (int, float)):
            print(f"❌ Invalid type for 'click_probability': {type(proba)}")
            return False
        
        if not 0.0 <= proba <= 1.0:
            print(f"❌ 'click_probability' out of range [0, 1]: {proba}")
            return False
        
        pred = data['click_prediction']
        if pred not in [0, 1]:
            print(f"❌ Invalid 'click_prediction' value: {pred} (must be 0 or 1)")
            return False
        
        print(f"✅ Response validation passed:")
        print(f"   click_probability: {proba}")
        print(f"   click_prediction: {pred}")
        return True
        
    except ValueError as e:
        print(f"❌ Invalid JSON response: {e}")
        return False


def main():
    """Main smoke test function."""
    print("🔥 Starting smoke test for Avazu CTR API...")
    print(f"   API URL: {API_URL}")
    
    # Step 1: Health check
    print("\n📡 Step 1: Health check...")
    if not check_health():
        print("\n❌ Smoke test FAILED: Health check did not pass")
        sys.exit(1)
    
    # Step 2: Send prediction request
    print("\n📤 Step 2: Sending prediction request...")
    test_features = {
        "site_id": "test_site_123",
        "app_id": "test_app_456",
        "site_domain": "test_domain.com",
        "app_domain": "test_app.com",
        "device_type": "1",
        "device_conn_type": "0",
    }
    
    try:
        response = send_prediction_request(test_features)
        print(f"   Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)
    
    # Step 3: Validate response
    print("\n✅ Step 3: Validating response...")
    if not validate_response(response):
        print("\n❌ Smoke test FAILED: Response validation failed")
        sys.exit(1)
    
    print("\n🎉 Smoke test PASSED: Service is up and responding correctly!")
    sys.exit(0)


if __name__ == "__main__":
    main()

