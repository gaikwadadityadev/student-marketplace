import json
import re
import os

paths = [
    r"C:\Users\adity\.gemini\antigravity-ide\brain\11589b57-803b-45d9-a4a3-9f1707dd7365\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\661ed935-406a-436f-b46d-3279ca299127\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\794c0a86-8028-4066-9b58-d30ca0defd0e\.system_generated\logs\transcript.jsonl",
    r"C:\Users\adity\.gemini\antigravity-ide\brain\97a6564a-a29a-4f70-9dc3-92a7d9d68592\.system_generated\logs\transcript.jsonl"
]

for p in paths:
    print(f"\n==================== Scanning: {p} ====================")
    if not os.path.exists(p):
        print("File does not exist")
        continue
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            for idx, line in enumerate(f):
                if 'browser_get_dom' in line:
                    data = json.loads(line)
                    # Print the content or look for values
                    content = str(data.get('content', ''))
                    print(f"  Line {idx} has browser_get_dom! Content length: {len(content)}")
                    
                    # Search for variables
                    for var in ['MYSQLHOST', 'MYSQLPASSWORD', 'MYSQLUSER', 'MYSQLDATABASE', 'MYSQLPORT', 'railway.app']:
                        if var in content:
                            pos = content.find(var)
                            print(f"    Found {var}!")
                            print(f"    Context: {content[pos-10:pos+120]}")
                            
                            # Let's extract values
                            # The DOM might contain patterns like:
                            # input value="value" or text nodes
                    
                    # Save DOM content to file
                    with open(f"extracted_dom_{idx}.txt", "w", encoding="utf-8") as out_f:
                        out_f.write(content)
                    print(f"  Saved DOM to extracted_dom_{idx}.txt")
    except Exception as e:
        print(f"  Error: {e}")
