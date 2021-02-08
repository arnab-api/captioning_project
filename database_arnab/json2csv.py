import json

with open("database_arnab/report.json") as f:
    obj = json.load(f)

print(obj[0])
print(type(obj[0]))

txt = "hi\nhi\n"
print(txt)