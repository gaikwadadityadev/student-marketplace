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
            # Files modified in the last 15 minutes (900 seconds)
            if now - mtime < 900:
                recent_files.append((full_path, mtime, os.path.getsize(full_path)))
        except Exception:
            pass

print(f"Found {len(recent_files)} recent files:")
for path, mtime, size in sorted(recent_files, key=lambda x: x[1], reverse=True):
    print(f"  {path} (Size: {size} bytes, Modified {int(now - mtime)}s ago)")
