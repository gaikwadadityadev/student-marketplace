import json

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        # Let's search for any string pattern resembling hostnames, e.g. .railway.app or containers-us
        if 'railway.app' in line.lower() or 'containers-us' in line.lower() or 'mysql' in line.lower():
            # Check if this is not the script itself
            if 'extract_dom' in line or 'find_subagent' in line or 'find_all_logs' in line:
                continue
            try:
                data = json.loads(line)
                content = str(data.get('content', ''))
                # Print type, step_index, and match details
                print(f"Step {data.get('step_index')} (type: {data.get('type')}, source: {data.get('source')}):")
                print(f"  Match length: {len(content)}")
                for var in ['railway.app', 'containers-us', 'mysql']:
                    if var in content.lower():
                        pos = content.lower().find(var)
                        print(f"    --> Found '{var}' in content!")
                        print(f"      Context: {content[pos-50:pos+150]}")
                
                tool_calls = str(data.get('tool_calls', ''))
                for var in ['railway.app', 'containers-us', 'mysql']:
                    if var in tool_calls.lower():
                        pos = tool_calls.lower().find(var)
                        print(f"    --> Found '{var}' in tool_calls!")
                        print(f"      Context: {tool_calls[pos-50:pos+150]}")
            except Exception as e:
                pass
