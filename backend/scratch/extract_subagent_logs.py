import json
import re

p = r"C:\Users\adity\.gemini\antigravity-ide\brain\661ed935-406a-436f-b46d-3279ca299127\.system_generated\logs\transcript.jsonl"

with open(p, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        # Let's search this line for any output of browser_get_dom
        # The tool response from the subagent has the DOM or text content
        if 'browser_get_dom' in line or 'DOM' in line or 'MYSQL' in line:
            try:
                data = json.loads(line)
                content = str(data.get('content', ''))
                # Print type, step_index, and match details
                print(f"Step {data.get('step_index')} (type: {data.get('type')}, source: {data.get('source')}):")
                print(f"  Content length: {len(content)}")
                
                # Check for railway values or connection string
                # We can print any lines of the content that contain input, value, or the key strings
                for l in content.splitlines():
                    if any(x in l.lower() for x in ['mysql', 'railway.app', 'containers', 'port', 'password', 'user', 'host', 'db']):
                        print(f"    --> {l.strip()[:140]}")
            except Exception as e:
                pass
