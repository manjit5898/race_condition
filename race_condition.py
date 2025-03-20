import requests
import threading
import time
import re
import argparse

# Set default values
RACE_COUNT = 128
BASE_URL = "https://example.com"
session = requests.Session()

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Automated Race Condition Tester")
parser.add_argument("-r", "--request", required=True, help="File containing login request (e.g., login.txt)")
parser.add_argument("-u", "--urls", required=True, help="File containing URLs to test (e.g., urls.txt)")
parser.add_argument("-c", "--count", type=int, default=RACE_COUNT, help="Number of concurrent requests per URL")
args = parser.parse_args()

RACE_COUNT = args.count

# Read login request from file
def load_login_request(filename):
    with open(filename, "r") as f:
        raw_request = f.read()

    lines = raw_request.split("\n")
    method, path, _ = lines[0].split(" ")
    headers = {}
    body = None

    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
        elif line.strip():  
            body = line.strip()
    
    return method, path, headers, body

# Perform login and maintain session
def login():
    method, path, headers, body = load_login_request(args.request)
    login_url = f"{BASE_URL}{path}"

    if "Content-Type" in headers and "json" in headers["Content-Type"]:
        data = body
    else:
        data = None

    if method == "POST":
        response = session.post(login_url, headers=headers, data=data)
    else:
        response = session.get(login_url, headers=headers)

    if response.status_code == 200:
        print("[✅] Logged in successfully. Session maintained.")
        return True
    else:
        print(f"[❌] Login failed! Status: {response.status_code}")
        return False

# Read test URLs from file
def load_test_urls(filename):
    with open(filename, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    return urls

# Send race condition requests
def test_race_condition(url, results, index):
    full_url = f"{BASE_URL}{url}"
    start_time = time.time()
    response = session.get(full_url)
    response_time = time.time() - start_time
    body = response.text

    if response.status_code != 200:
        print(f"[❌] Request {index} failed! Status: {response.status_code}")
        results[index] = False
        return

    if "Transaction processed successfully more than once" in body:
        print(f"[🔥] Race Condition Detected at {url} ({response_time:.2f}s)")
        results[index] = True
        return

    balance_matches = re.findall(r"New Balance: \$([0-9]+)", body)
    if len(balance_matches) > 1:
        print(f"[🔥] Balance changed multiple times at {url}! ({response_time:.2f}s)")
        results[index] = True
        return

    if "Duplicate order detected" in body or "Coupon applied multiple times" in body:
        print(f"[🔥] Multiple orders/coupons applied at {url}! ({response_time:.2f}s)")
        results[index] = True
        return

    if response_time > 2.0:
        print(f"[⚠️] Potential slowdown detected at {url}. ({response_time:.2f}s)")
        results[index] = True
        return

    print(f"[✅] Request {index} normal at {url}. ({response_time:.2f}s)")
    results[index] = False

# Run race condition tests
def run_race_condition_test():
    test_urls = load_test_urls(args.urls)
    
    for url in test_urls:
        print(f"\n[🚀] Testing {url} for Race Conditions...")
        threads = []
        results = [False] * RACE_COUNT

        for i in range(RACE_COUNT):
            t = threading.Thread(target=test_race_condition, args=(url, results, i))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if any(results):
            print(f"\n[🔥] Race Condition Confirmed at {url}!")
        else:
            print(f"\n[✅] No Race Condition Detected at {url}.")

# Execute the attack
if login():
    print("[🚀] Running Race Condition Test...")
    run_race_condition_test()
else:
    print("[❌] Exiting: Login failed.")
