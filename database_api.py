import sqlite3
import os

USER_DATABASE = os.path.dirname(os.path.realpath(__file__)) + "/datasets/users.db"
TWEETS_DATABASE = os.path.dirname(os.path.realpath(__file__)) + "/datasets/tweets.db"
TWITTER_DATABASE = os.path.dirname(os.path.realpath(__file__)) + "/datasets/twitter.db"
SETS_DATABASE = os.path.dirname(os.path.realpath(__file__)) + "/datasets/sets.db"

def insert_datamuse_set(context, strong_set, weak_set):
    conn = sqlite3.connect(SETS_DATABASE)
    cursor = conn.cursor()
    new_strong_set = ";".join([x for x in strong_set])
    new_weak_set = ";".join([x for x in weak_set])
    params = (context, new_weak_set, new_strong_set, )
    sql = 'REPLACE INTO sets(context,weak_set,strong_set) VALUES("{}","{}","{}")'.format(*params)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_datamuse_set(context, strength):
    conn = sqlite3.connect(SETS_DATABASE)
    cursor = conn.cursor()
    params = (strength, context,)
    set = []
    sql = 'SELECT "{}" FROM sets where context = "{}"'.format(*params)
    for row in cursor.execute(sql):
        set.append(row)
    conn.close()
    if set == (['']):
        return []
    return set[0][0]


def get_all_tweets_by_username(user_name):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    t = (user_name, )
    tweets = []
    for row in cursor.execute('SELECT * FROM tweets WHERE screen_name=?', t):
        tweets.append(row)
    conn.close()
    return tweets


# TODO : Join from both followers and following tables
def get_all_followers_ids(user_id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    id = (user_id, )
    followers = []
    for row in cursor.execute('SELECT follower_id FROM followers WHERE id=?', id):
        followers.append(row[0])
    conn.close()
    return followers

# TODO : Join from both followers and following tables
def get_all_following(user_id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    id = (user_id, )
    following = []
    for row in cursor.execute('SELECT following_id FROM following WHERE id=?', id):
        following.append(row[0])
    conn.close()
    return following

def username_to_id(user_name):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    t = (user_name, )
    id = None
    for row in cursor.execute('SELECT id FROM users WHERE username =?', t):
        id = row[0]
    conn.close()
    return id

def id_to_username(id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    t = (id, )
    username = None
    for row in cursor.execute('SELECT username FROM users WHERE id =?', t):
        username = row[0]
    conn.close()
    return username

def get_profile(username):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    t = (username, )
    profile = None
    for row in cursor.execute('SELECT * FROM users WHERE username = ?', t):
        profile = row
    conn.close()
    return profile

def get_profile_by_id(user_id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    t = (user_id, )
    profile = None
    for row in cursor.execute('SELECT * FROM users WHERE id = ?', t):
        profile = row
    conn.close()
    return profile

def get_all_tweets_by_context(context):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    tweets = []
    added_ids = []
    for term in context.split(" "):
        t = ('%' + term + '%',)
        for row in cursor.execute('SELECT * FROM tweets WHERE tweet LIKE ?', t):
            if row[0] not in added_ids:
                added_ids.append(row[0])
                tweets.append(row)
    conn.close()
    return tweets

def get_all_users_by_context(context):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    screen_names = []
    for term in context.split(" "):
        t = ('%' + term + '%',)
        for row in cursor.execute('SELECT * FROM tweets WHERE tweet LIKE ?', t):
            if row[14] not in screen_names:
                screen_names.append(row[14])
    conn.close()
    return screen_names

def get_filtered_favorites(user_id, candidate_id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    filtered_favorites = []
    params = (candidate_id, user_id,)
    sql = 'SELECT * FROM tweets WHERE user_id = "{}" AND id in \
          (SELECT tweet_id FROM favorites WHERE user_id = "{}")'.format(*params)
    for row in cursor.execute(sql):
        filtered_favorites.append(row)

    conn.close()
    return filtered_favorites

def get_favorites_by_context(user_id, keyword):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    favorites_by_context = []
    params = (user_id, '%' + keyword + '%')
    sql = 'SELECT * FROM tweets WHERE user_id = "{}" AND tweet LIKE "{}" AND id in \
          (SELECT tweet_id FROM favorites)'.format(*params)

    for row in cursor.execute(sql):
        favorites_by_context.append(row)

    conn.close()
    return favorites_by_context

def get_favorites(user_id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    favorites = []
    params = (user_id,)
    sql = 'SELECT tweet_id FROM favorites WHERE user_id = "{}"'.format(*params)

    for row in cursor.execute(sql):
        favorites.append(row)

    conn.close()
    return favorites

def get_common_favorites(user_id, candidate_id):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    favorites = []
    params = (user_id, candidate_id)
    sql = 'SELECT f1.tweet_id FROM favorites f1, favorites f2 WHERE f1.user_id = "{}" AND f2.user_id = "{}" AND f1.tweet_id = f2.tweet_id'.format(*params)

    for row in cursor.execute(sql):
        favorites.append(row)

    conn.close()
    return favorites

def get_user_tweets_by_context(user_id, keyword):
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    params = (user_id, '%' + keyword + '%')
    user_tweets_by_context = []
    sql = 'SELECT * FROM tweets WHERE user_id = "{}" AND tweet LIKE "{}"'.format(*params)
    for row in cursor.execute(sql):
        user_tweets_by_context.append(row)

    conn.close()
    return user_tweets_by_context

def get_all_connections():
    conn = sqlite3.connect(TWITTER_DATABASE)
    cursor = conn.cursor()
    following = []
    for row in cursor.execute('SELECT * FROM following',):
        following.append((row[0], row[1]))
    for row in cursor.execute('SELECT * FROM followers', ):
            following.append((row[0], row[1]))
    conn.close()
    return following