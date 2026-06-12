import json
import sys

# Set output encoding to UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

terms = ['railway.app', 'up.railway.app', 'mysql.railway', 'mysql.railway.internal', 'railway.internal']
found = []

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            content = str(data.get('content', ''))
            matched = False
            for term in terms:
                if term in content.lower():
                    matched = True
                    break
            if not matched:
                tool_calls = str(data.get('tool_calls', ''))
                for term in terms:
                    if term in tool_calls.lower():
                        matched = True
                        break
            if matched:
                found.append({
                    'step': data.get('step_index'),
                    'type': data.get('type'),
                    'content': content,
                    'tool_calls': str(data.get('tool_calls'))
                })
        except Exception as e:
            pass

print(f"Total matched steps: {len(found)}")
for item in found:
    print(f"Step {item['step']} ({item['type']}):")
    # Escape characters that might cause printing issues
    clean_content = item['content'].encode('ascii', errors='replace').decode('ascii')
    clean_tools = item['tool_calls'].encode('ascii', errors='replace').decode('ascii')
    print(f"  Content: {clean_content[:1500]}")
    print(f"  Tools: {clean_tools[:1500]}")
    print("=" * 80)
