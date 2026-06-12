import json

log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if '8D5F9F015912B736D033CA1B4A36AAB6' in line:
            try:
                data = json.loads(line)
                # Print type, step_index, and some content
                print(f"Step {data.get('step_index')} (type: {data.get('type')}, source: {data.get('source')}):")
                content = str(data.get('content', ''))
                print(f"  Content length: {len(content)}")
                # If there are tool calls:
                if 'tool_calls' in data:
                    print(f"  Tool calls: {data['tool_calls']}")
                
                # Let's check if the content contains the variables
                for var in ['MYSQLHOST', 'MYSQLPASSWORD', 'MYSQLUSER', 'MYSQLDATABASE', 'MYSQLPORT', 'railway.app']:
                    if var in content:
                        print(f"    --> Found '{var}' in content!")
                        # print context
                        pos = content.find(var)
                        print(f"      Context: {content[pos-50:pos+150]}")
            except Exception as e:
                print(f"  Error parsing line {idx}: {e}")
