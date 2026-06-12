import os
import time

brain_dir = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87"
now = time.time()
recent_files = []

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        full_path = os.path.join(root, f)
        try:
            mtime = os.path.getmtime(full_path)
            # Files modified in the last 30 minutes
            if now - mtime < 1800:
                recent_files.append((full_path, mtime))
        except Exception:
            pass

print(f"Found {len(recent_files)} recent files:")
for path, mtime in sorted(recent_files, key=lambda x: x[1]):
    print(f"  {path} (Modified {int(now - mtime)}s ago)")
    
    # Search content if it is a text file
    if path.endswith(('.txt', '.log', '.json', '.md', '.jsonl')):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as file_content:
                text = file_content.read()
                # Check for railway variables or hosts
                for term in ['MYSQLHOST', 'railway.app', 'MYSQL_HOST']:
                    if term in text:
                        print(f"    --> Found '{term}' in this file!")
                        # Print occurrences
                        for line in text.splitlines():
                            if any(t in line for t in ['MYSQLHOST', 'MYSQLPASSWORD', 'MYSQLUSER', 'MYSQLDATABASE', 'MYSQLPORT', 'railway.app']):
                                print(f"      Line: {line.strip()[:120]}")
        except Exception as e:
            print(f"    Error reading file: {e}")
