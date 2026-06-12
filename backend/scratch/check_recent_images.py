import os
import time

dir_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.tempmediaStorage"
now = time.time()
recent = []

for f in os.listdir(dir_path):
    p = os.path.join(dir_path, f)
    mtime = os.path.getmtime(p)
    if now - mtime < 600: # Last 10 minutes
        recent.append((f, mtime))

print(f"Found {len(recent)} recent files:")
for f, mtime in sorted(recent, key=lambda x: x[1]):
    print(f"  {f} (Modified {int(now - mtime)}s ago)")
