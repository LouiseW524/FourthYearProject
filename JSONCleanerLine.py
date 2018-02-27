import json
import os
import glob

for filename in glob.iglob('**/*.json', recursive=True):
     print(filename)
     with open(filename, encoding="utf8") as json_file:
        data = str(json.load(json_file))
        year = year + 1
        for line in data.split():
            line.replace(".", " ")
     f = open("C:/Program Files (x86)/Jenkins/workspace/data/MongoFiles" + filename , "w")
     f.write(data)