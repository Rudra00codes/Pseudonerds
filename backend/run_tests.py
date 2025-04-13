import subprocess
import time
import os
import sys
import signal
import platform

def is_port_in_use(port):
    """Check if a port is in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_tests():
    """Run the test suite with the Flask server running"""
    # Check if server is already running
    if is_port_in_use(5000):
        print("Warning: Port 5000 is already in use. Make sure no other Flask server is running.")
        return False
    
    # Start the Flask server
    print("Starting Flask server...")
    if platform.system() == 'Windows':
        server_process = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        server_process = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
    
    # Wait for server to start
    print("Waiting for server to start...")
    max_retries = 10
    retries = 0
    while retries < max_retries:
        if is_port_in_use(5000):
            break
        time.sleep(1)
        retries += 1
    
    if retries == max_retries:
        print("Error: Server failed to start within the expected time.")
        server_process.terminate()
        return False
    
    print("Server started successfully.")
    
    try:
        # Run the tests
        print("\nRunning API tests...")
        test_result = subprocess.run(["python", "tests/test_api.py"], check=False)
        success = test_result.returncode == 0
    finally:
        # Terminate the server
        print("\nShutting down server...")
        if platform.system() == 'Windows':
            os.kill(server_process.pid, signal.CTRL_BREAK_EVENT)
        else:
            os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        
        server_process.wait(timeout=5)
        print("Server shutdown complete.")
    
    return success

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = run_tests()
    sys.exit(0 if success else 1)