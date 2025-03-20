Step 1: Install Required Libraries
pip3 install requests

📌 Step 4: Run the Script from CLI
Now, run the script with:

python3 race_condition.py -r login.txt -u urls.txt -c 128
Where:

-r login.txt → Specifies the login request file
-u urls.txt → Specifies the file with URLs to test
-c 128 → Specifies the number of concurrent requests
📌 Step 5: Understanding Output
✅ If everything is normal:

arduino

[✅] Logged in successfully. Session maintained.
[🚀] Running Race Condition Test...
[🚀] Testing /api/transfer?amount=100 for Race Conditions...
[✅] Request 5 normal at /api/transfer?amount=100. (0.87s)
[✅] Request 6 normal at /api/transfer?amount=100. (0.90s)
[✅] No Race Condition Detected at /api/transfer?amount=100.
🔥 If a race condition is detected:
[🔥] Race Condition Detected at /api/transfer?amount=100 (1.23s)
[🔥] Balance changed multiple times at /api/transfer?amount=100! (1.20s)
[🔥] Race Condition Confirmed at /api/transfer?amount=100!





