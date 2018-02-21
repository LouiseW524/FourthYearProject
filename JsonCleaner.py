import json
import string

filename = 'C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_stats.json'
translator = str.maketrans('', '', string.punctuation)

def remove_dot_key(obj):
    replacement_keys = {}
    for key in obj.keys():
        for subkey in obj[key]:
            for underkey in obj[key][subkey]:
                if underkey == "Player_stats":
                    for basekey in obj[key][subkey][underkey].keys():
                        new_key = basekey.translate(translator)
                        print(new_key)
                        replacement_keys[basekey] = new_key

                for old_key, value in replacement_keys.items():
                    obj[key][subkey][underkey][value] = obj[key][subkey][underkey][old_key]
                    del obj[key][subkey][underkey][old_key]

    return obj

obj = None
with open(filename, 'r') as f:
    obj = json.load(f)
    ans =  remove_dot_key(obj)


f = open("C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/myfile.txt", "w")
f.write(str(ans))