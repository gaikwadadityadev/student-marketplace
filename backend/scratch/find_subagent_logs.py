import os

base_dir = r"C:\Users\adity\.gemini\antigravity-ide"
found = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f == "transcript.jsonl":
            found.append(os.path.join(root, f))

print(f"Found {len(found)} transcript files:")
for path in found:
    print(f"  {path} (Size: {os.path.getsize(path)} bytes)")
