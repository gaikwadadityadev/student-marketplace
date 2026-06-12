import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

found = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '8D5F9F015912B736D033CA1B4A36AAB6' in line or 'get_railway_db' in line:
            found.append(line)

print(f"Found {len(found)} lines matching the subagent run.")
for f_line in found[-5:]: # Print last 5 lines
    data = json.loads(f_line)
    content = str(data.get('content', ''))
    clean_content = content.encode('ascii', errors='replace').decode('ascii')
    print(f"Step {data.get('step_index')}: {clean_content[:1500]}")
    print("-" * 80)
