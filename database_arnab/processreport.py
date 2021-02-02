import json

with open("database_arnab/report.json") as f:
    report = json.load(f)

print(report)

json_formatted_str = json.dumps(report, indent=2)
print(json_formatted_str)