echo on
title MongoSetup
::Importing mongodb match JSON files into respective collections
cd C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin
mongoimport --db soccerStats --collection matchStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_match_stats14-15.json
mongoimport --db soccerStats --collection matchStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_match_stats15-16.json
mongoimport --db soccerStats --collection matchStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_match_stats16-17.json
mongoimport --db soccerStats --collection matchStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_match_stats17-18.json	
::Importing mongodb player JSON files into respective collections
mongoimport --db soccerStats --collection playerStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_stats14-15.json
mongoimport --db soccerStats --collection playerStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_stats15-16.json
mongoimport --db soccerStats --collection playerStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_stats16-17.json
mongoimport --db soccerStats --collection playerStats --file C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/season_stats17-18.json

		
		
	
