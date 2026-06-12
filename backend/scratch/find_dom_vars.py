import json

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

# We will read transcript.jsonl, find all lines that contain "browser_get_dom",
# and print any content in those tool outputs.
with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'browser_get_dom' in line:
            # Parse line as json
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content:
                    print(f"--- MATCH AT LINE {idx} (Content length: {len(content)}) ---")
                    # Look for values inside the content (e.g. railway.app, root, etc.)
                    # Let's write the content to a temp file to inspect
                    with open(f"temp_dom_{idx}.txt", "w", encoding="utf-8") as temp_f:
                        temp_f.write(content)
                    print(f"Saved DOM to temp_dom_{idx}.txt")
            except Exception as e:
                print(f"Error at line {idx}: {e}")
