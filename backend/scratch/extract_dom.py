import json
import re

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

# We will search the JSON objects in transcript.jsonl for any strings resembling the variables
# e.g., MYSQLHOST, MYSQLPASSWORD, etc.

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if '8D5F9F015912B736D033CA1B4A36AAB6' in line:
            # Let's search this line for potential connection parameters
            # e.g. hostnames ending in railway.app or password characters
            # Let's extract any words containing .railway.app or similar patterns
            matches = re.findall(r'[a-zA-Z0-9_\-\.]+\.railway\.app[a-zA-Z0-9_\-\./\?]*', line)
            if matches:
                print(f"Line {idx} matches railway.app: {matches}")
            
            # Let's search for values of variables like MYSQLUSER, MYSQLPASSWORD, etc.
            # Usually they are in the DOM, so let's look for tags or values
            # e.g. "value":"..."
            for var in ['MYSQLHOST', 'MYSQLPASSWORD', 'MYSQLUSER', 'MYSQLDATABASE', 'MYSQLPORT']:
                if var in line:
                    print(f"Line {idx} contains {var}")
                    # Print context around it
                    pos = line.find(var)
                    start = max(0, pos - 100)
                    end = min(len(line), pos + 300)
                    print(f"  Context: {line[start:end]}")
                    print("-" * 50)
