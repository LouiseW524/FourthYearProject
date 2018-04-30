import psycopg2.extras
from sklearn.naive_bayes import GaussianNB

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute("""SELECT DISTINCT playerid FROM training_teamlist""")
all_player_ids = cur.fetchall()
list_of_stats = []
features_list = []
target_list = []
for player_id in all_player_ids:
    cur.execute("""SELECT * FROM training_player_match_stats WHERE playerid = %s""", (player_id[0],))
    all_stats = cur.fetchall()
    for stat in all_stats:
        match_id = stat['matchid']
        print(match_id)
        list_of_stats = ( int(stat['redcard']),int(stat['yellowcard']), int(stat['goalassists']), int(stat['goalassists']), float(stat['playerrating']), int(stat['goalsscored']), int(stat['goalsconceded']), int(stat['cleansheet']), int(stat['penaltymissed']), int(stat['owngoals']), int(stat['saves']), int(stat['penaltysaves']))
        features_list.append(list_of_stats)
        target_list.append(int(stat['above_average_points']))

    half_features = int(len(features_list) / 2)
    half_targets =  int(len(target_list)/2)

    if half_features > 0:
        train_half_features, test_half_features= features_list[:half_features], features_list[half_features:]
        train_half_targets, test_half_targets = target_list[:half_targets], target_list[half_targets:]

        clf = GaussianNB()
        clf.fit(train_half_features,train_half_targets)

        from sklearn.tree import DecisionTreeClassifier

        for item in test_half_features:
            print(clf.predict([item]))
        print(test_half_targets)

        print('Accuracy of GNB classifier on test set: {:.2f}'
              .format(clf.score(test_half_features,test_half_targets)))

       # clf = DecisionTreeClassifier().fit(train_half_features, train_half_targets)
        #print('Accuracy of Decision Tree classifier on test set: {:.2f}'
         #     .format(clf.score(test_half_features, test_half_targets)))

        features_list.clear()
        target_list.clear()
