import os

base_dir = r"C:\Users\adity\.gemini\antigravity-ide\brain"
terms = ['containers-us', 'railway.app', 'mysql']

# List all subfolders in the brain directory
try:
    subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
except Exception as e:
    print(f"Error listing base: {e}")
    subfolders = []

print(f"Subfolders found: {subfolders}")

for folder in subfolders:
    folder_path = os.path.join(base_dir, folder)
    print(f"\nScanning folder: {folder_path}")
    
    # Recursively search files in this folder
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.endswith(('.jsonl', '.json', '.txt', '.log')):
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as file_content:
                        text = file_content.read()
                        # Clean script mentions
                        if any(s in p for s in ['search_all_transcripts', 'find_credentials', 'find_dom_vars', 'analyze_dom', 'search_subagent_logs_full', 'extract_subagent_logs']):
                            continue
                        
                        found_terms = [t for t in terms if t in text.lower()]
                        if found_terms:
                            print(f"  File: {p}")
                            print(f"    Found terms: {found_terms}")
                            # Let's print some lines containing them
                            for line in text.splitlines():
                                if any(t in line.lower() for t in terms):
                                    # clean script names
                                    if any(s in line for s in ['search_all_transcripts', 'find_credentials', 'find_dom_vars', 'analyze_dom', 'search_subagent_logs_full', 'extract_subagent_logs']):
                                        continue
                                    clean_line = line.strip().encode('ascii', errors='replace').decode('ascii')
                                    print(f"      Line: {clean_line[:150]}")
                except Exception as e:
                    pass
