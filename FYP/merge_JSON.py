import json

def merge(a, b):
    "merges b into a"
    for key in b:
        if key in a:# if key is in both a and b
            if isinstance(a[key], dict) and isinstance(b[key], dict): # if the key is dict Object
                merge(a[key], b[key])
            else:
              a[key] =a[key]+ b[key]
        else: # if the key is not in dict a , add it to dict a
            a.update({key:b[key]})
    return a

with open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season15-16/season_stats.json') as fp1:
    with open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_stats.json') as fp2:
        jsondata1=json.load(fp1)
        jsondata2=json.load(fp2)
        with open('./JsonMergeTestData/data.json', 'w') as f:
          json.dump(merge(jsondata1,jsondata2),f,sort_keys=True,indent=4)

with open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season15-16/season_match_stats.json') as fp1:
    with open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_match_stats.json') as fp2:
        jsondata1=json.load(fp1)
        jsondata2=json.load(fp2)
        with open('./JsonMergeTestData/matches.json', 'w') as f:
          json.dump(merge(jsondata1,jsondata2),f,sort_keys=True,indent=4)

