import json
import re

paths = [
    r"C:\Users\adity\.gemini\antigravity-ide\brain\11589b57-803b-45d9-a4a3-9f1707dd7365\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\661ed935-406a-436f-b46d-3279ca299127\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\794c0a86-8028-4066-9b58-d30ca0defd0e\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\97a6564a-a29a-4f70-9dc3-92a7d9d68592\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"
]

for p in paths:
    print(f"\nScanning: {p}")
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            for idx, line in enumerate(f):
                if 'railway.app' in line.lower() or 'containers-us' in line.lower():
                    # clean script mentions
                    if any(s in line for s in ['search_all_transcripts', 'find_credentials', 'find_dom_vars', 'analyze_dom']):
                        continue
                    
                    matches = re.findall(r'[a-zA-Z0-9_\-\.]+\.railway\.app[a-zA-Z0-9_\-\./\?]*', line)
                    if matches:
                        print(f"  Line {idx} matches railway.app: {matches}")
                    
                    pos = line.lower().find('railway.app')
                    if pos == -1:
                        pos = line.lower().find('containers-us')
                    
                    context = line[max(0, pos-100):pos+250]
                    clean_context = context.encode('ascii', errors='replace').decode('ascii')
                    print(f"  Context: {clean_context}")
                    print("-" * 50)
    except Exception as e:
        print(f"  Error: {e}")
