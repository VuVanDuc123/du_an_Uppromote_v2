#!/usr/bin/env python3
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'app-data-clean.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(os.path.join(script_dir, 'app-logic.js'), 'r', encoding='utf-8') as f:
    logic = f.read()

output = f"let allData = {json.dumps(data)};\n\n{logic}"

with open(os.path.join(script_dir, 'app.js'), 'w', encoding='utf-8') as f:
    f.write(output)

print("Build complete!")