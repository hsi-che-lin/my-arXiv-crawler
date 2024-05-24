import json
import os
import re

keywords = r"astronomy"
allFind = []

for result in sorted(os.listdir("results")):
    with open(os.path.join("results", result), "r") as f:
        info = json.load(f)
    
    for x in info:
        find = re.findall(keywords, x["title"], flags = re.IGNORECASE) + re.findall(keywords, x["abstract"], flags = re.IGNORECASE)
        if ((len(find) > 0) and (float(x["rating"]) > -1)):
            allFind.append(x)
            print(f"date = {result.split('.')[0]}")
            print(f"url = {x['abstract url']}")
            print(f"rating = {x['rating']}")
            print(f"title = {x['title']}")
            print(f"abstract = {x['abstract']}")
            print("-" * 80)

print(f"total findings = {len(allFind)}")
