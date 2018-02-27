echo on
title MongoSetup
::Importing mongodb match JSON files into respective collections
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection matchStats --file season_match_stats14-15.json
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection matchStats --file season_match_stats15-16.json
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection matchStats --file season_match_stats16-17.json
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection matchStats --file season_match_stats17-18.json	
::Importing mongodb player JSON files into respective collections
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection playerStats --file season_stats14-15.json
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection playerStats --file season_stats15-16.json
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection playerStats --file season_stats16-17.json
C:/"Program Files (x86)"/Jenkins/tools/org.jenkinsci.plugins.mongodb.MongoDBInstallation/mongodb/bin/mongoimport --db soccerStats --collection playerStats --file season_stats17-18.json

		
		
	
