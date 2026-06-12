# Parse the temp DOM files to find the database connection details
for name in ["temp_dom_336.txt", "temp_dom_351.txt"]:
    print(f"\n==================== Analyzing {name} ====================")
    try:
        with open(name, "r", encoding="utf-8") as f:
            content = f.read()
            # Let's search for input values or labels
            # Let's look for standard patterns like value="..." or strings close to MYSQL_HOST
            # Also let's print lines containing 'railway.app' or similar
            for line in content.splitlines():
                if any(k in line for k in ['MYSQL', 'railway', 'root', 'port', 'password', 'database', 'host']):
                    print(line.strip())
    except Exception as e:
        print(f"Error reading {name}: {e}")
