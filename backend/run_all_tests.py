import subprocess
import sys
import os

def run_model_tests():
    """Run the model tests"""
    print("=" * 50)
    print("RUNNING MODEL TESTS")
    print("=" * 50)
    result = subprocess.run(["python", "tests/test_model.py"], check=False)
    return result.returncode == 0

def run_api_tests():
    """Run the API tests with server"""
    print("\n" + "=" * 50)
    print("RUNNING API TESTS")
    print("=" * 50)
    result = subprocess.run(["python", "run_tests.py"], check=False)
    return result.returncode == 0

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    model_success = run_model_tests()
    api_success = run_api_tests()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Model tests: {'PASSED' if model_success else 'FAILED'}")
    print(f"API tests: {'PASSED' if api_success else 'FAILED'}")
    print(f"Overall: {'PASSED' if model_success and api_success else 'FAILED'}")
    
    sys.exit(0 if model_success and api_success else 1)