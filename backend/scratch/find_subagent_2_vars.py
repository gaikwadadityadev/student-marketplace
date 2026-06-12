import json

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"
target_id = "62F29B9F19C63F15FF64DFDF45C65F6D"

# Find any line that contains target_id and check its content.
# Specifically, we want the response of browser_get_dom tool calls!
with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if target_id in line:
            try:
                data = json.loads(line)
                content = str(data.get('content', ''))
                # Write matching DOM tool responses to files so we can read/analyze them
                if 'CORTEX_STEP_STATUS_DONE' in content or 'DOM' in line or len(content) > 1000:
                    with open(f"subagent_dom_{idx}.txt", "w", encoding="utf-8") as out_f:
                        out_f.write(content)
                    print(f"Saved match to subagent_dom_{idx}.txt (Len: {len(content)}, Source: {data.get('source')}, Type: {data.get('type')})")
            except Exception as e:
                print(f"Error parsing line {idx}: {e}")
