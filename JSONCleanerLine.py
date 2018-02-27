import json
import os
import glob

for filename in glob.iglob('**/*.json', recursive=True):
     print(filename)
     with open(filename, encoding="utf8") as json_file:
        data = str(json.load(json_file))
        for line in data.split():
            line.replace(".", " ")
     f = open(filename , "w")
     f.write(data)