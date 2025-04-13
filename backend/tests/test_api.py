import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000/api"
MAX_RETRIES = 3
RETRY_DELAY = 2

def retry_request(func):
    """Decorator to retry requests with exponential backoff"""
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError as e:
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Connection failed. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Connection failed after {MAX_RETRIES} attempts.")
                    raise
    return wrapper

@retry_request
def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("✓ Health endpoint test passed")
    return True

@retry_request
def test_diagnose_endpoint():
    """Test the diagnose endpoint"""
    print("Testing diagnose endpoint...")
    payload = {
        "symptoms": ["fever", "cough", "headache"],
        "language": "en"
    }
    
    response = requests.post(f"{BASE_URL}/diagnose/test", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Check that we got a diagnosis
    if isinstance(data, list):
        assert len(data) > 0
        assert "diagnosis" in data[0]
        assert "confidence" in data[0]
        assert "severity" in data[0]
        print(f"Diagnosis: {data[0]['diagnosis']} (confidence: {data[0]['confidence']:.2f}, severity: {data[0]['severity']})")
    else:
        assert "diagnosis" in data
        assert "confidence" in data
        assert "severity" in data
        print(f"Diagnosis: {data['diagnosis']} (confidence: {data['confidence']:.2f}, severity: {data['severity']})")
    
    print("✓ Diagnose endpoint test passed")
    return True

@retry_request
def test_multilingual_diagnosis():
    """Test diagnosis with non-English symptoms"""
    print("Testing multilingual diagnosis...")
    # Hindi symptoms for fever, cough, headache
    payload = {
        "symptoms": ["बुखार", "खांसी", "सिरदर्द"],
        "language": "hi"
    }
    
    response = requests.post(f"{BASE_URL}/diagnose/test", json=payload)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            print(f"Hindi symptoms diagnosis: {data[0]['diagnosis']} (confidence: {data[0]['confidence']:.2f})")
        else:
            print(f"Hindi symptoms diagnosis: {data['diagnosis']} (confidence: {data['confidence']:.2f})")
        print("✓ Multilingual diagnosis test passed")
        return True
    else:
        print(f"× Multilingual test failed: {response.text}")
        return False

def run_all_tests():
    """Run all tests and return overall success status"""
    tests_passed = 0
    tests_failed = 0
    
    try:
        if test_health_endpoint():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"Health endpoint test failed: {e}")
        tests_failed += 1
    
    try:
        if test_diagnose_endpoint():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"Diagnose endpoint test failed: {e}")
        tests_failed += 1
    
    # Only run multilingual test if translation service is available
    try:
        if test_multilingual_diagnosis():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"Multilingual test skipped: {e}")
        # Don't count this as a failure if it's a connection issue
        if not isinstance(e, requests.exceptions.ConnectionError):
            tests_failed += 1
    
    print(f"\nTest summary: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0

if __name__ == "__main__":
    print("Running API tests...")
    success = run_all_tests()
    print("API tests completed!")
    sys.exit(0 if success else 1)