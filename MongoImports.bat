echo on
title MongoSetup
::Importing mongodb match JSON files into respective collections
STR="C:/Program Files (x86)/Jenkins/workspace/Fourth Year Project V1.1/datasets"
cd C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin
mongoimport --db soccerStats --collection matchStats --file $STR/season_match_stats14-15.json
mongoimport --db soccerStats --collection matchStats --file $STR/season_match_stats15-16.json
mongoimport --db soccerStats --collection matchStats --file $STR/season_match_stats16-17.json
mongoimport --db soccerStats --collection matchStats --file $STR/season_match_stats17-18.json	
::Importing mongodb player JSON files into respective collections
mongoimport --db soccerStats --collection playerStats --file $STR/season_stats14-15.json
mongoimport --db soccerStats --collection playerStats --file $STR/season_stats15-16.json
mongoimport --db soccerStats --collection playerStats --file $STR/season_stats16-17.json
mongoimport --db soccerStats --collection playerStats --file $STR/season_stats17-18.json

		
		
	
