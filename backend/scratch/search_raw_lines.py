log_path = r"C:\Users\adity\.gemini\antigravity-ide\brain\e53b5913-11f9-42e6-baed-fdb594d3ce87\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        # We want to find the exact database variables.
        # Let's search for MYSQLHOST or containers-us or mysql.railway
        # or railway.app.
        # Clean script matching
        if any(s in line for s in ['search_raw_lines', 'extract_dom', 'find_subagent', 'find_all_logs']):
            continue
        
        # Check if line contains railway.app or containers-us
        if 'railway.app' in line.lower() or 'containers-us' in line.lower():
            print(f"Line {idx}:")
            # print surrounding characters
            pos = line.lower().find('railway.app')
            if pos == -1:
                pos = line.lower().find('containers-us')
            context = line[max(0, pos-150):pos+150]
            clean_context = context.encode('ascii', errors='replace').decode('ascii')
            print(f"  Context: {clean_context}")
            print("-" * 80)
