import os
import time

base_dir = r"C:\Users\adity\.gemini\antigravity-ide\brain"
folders = []

try:
    for f in os.listdir(base_dir):
        p = os.path.join(base_dir, f)
        if os.path.isdir(p):
            folders.append((f, os.path.getmtime(p)))
except Exception as e:
    print(f"Error: {e}")

print("Folders sorted by modification time (newest first):")
for f, mtime in sorted(folders, key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {f} (Modified {int(time.time() - mtime)}s ago)")
