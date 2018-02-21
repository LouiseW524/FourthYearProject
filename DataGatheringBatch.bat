echo on
title DataGathering
:: Accessing API and Downloading dataset
cd C:/Users/louis/AppData/Local/Programs/Python/Python36-32/Scripts && kaggle config path -p C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1" && kaggle datasets download -d shubhmamp/english-premier-league-match-data
:: Unzipping the dataset
cd C:/"Program Files (x86)"/Jenkins/workspace/"Fourth Year Project V1.1"/datasets/shubhmamp/english-premier-league-match-data && dir &&  C:/"Program Files"/7-Zip/7z x datafile.zip