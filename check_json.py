import json
import os

path = 'data/medical.json'
if not os.path.exists(path):
    print("File not found")
else:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            # medical.json seems to be a list of JSON objects, not a single JSON array?
            # Or maybe it's one JSON object per line?
            # Let's check the first char.
            first_char = f.read(1)
            f.seek(0)
            if first_char == '[':
                data = json.load(f)
                print(f"Loaded JSON array with {len(data)} items")
            elif first_char == '{':
                # Maybe one object per line?
                count = 0
                for line in f:
                    try:
                        json.loads(line)
                        count += 1
                    except:
                        pass
                print(f"Loaded {count} JSON lines")
            else:
                print(f"Unknown format, starts with {first_char}")
    except Exception as e:
        print(f"Error reading utf-8: {e}")
        # Try GBK
        try:
            with open(path, 'r', encoding='gbk') as f:
                 # ... same logic ...
                 pass
        except Exception as e2:
            print(f"Error reading gbk: {e2}")
