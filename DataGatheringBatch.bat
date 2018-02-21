echo on
title DataGathering
:: Accessing API and Downloading dataset
cd C:/Users/louis/AppData/Local/Programs/Python/Python36-32/Scripts && kaggle config path -p C:/"Program Files (x86)"/Jenkins/workspace/Test2 && kaggle datasets download -d shubhmamp/english-premier-league-match-data
:: Unzipping the dataset
cd C:/"Program Files (x86)"/Jenkins/workspace/Test2/datasets/shubhmamp/english-premier-league-match-data && dir &&  C:/"Program Files"/7-Zip/7z x datafile.zip
:: Moving unzipped files to correct workspace
cd datasets\shubhmamp/english-premier-league-match-data/season14-15 && move *.json C:/"Program Files (x86)"/Jenkins/workspace/Test2 


