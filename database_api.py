import sqlite3
import os

USER_DATABASE = os.path.dirname(os.path.realpath(__file__)) + "/datasets/users.db"
TWEETS_DATABASE = os.path.dirname(os.path.realpath(__file__)) + "/datasets/tweets.db"

def get_all_tweets_by_username(user_name):
    conn = sqlite3.connect(TWEETS_DATABASE)
    cursor = conn.cursor()
    t = (user_name, )
    tweets = []
    for row in cursor.execute('SELECT * FROM tweets WHERE screen_name=?', t):
        tweets.append(row)
    conn.close()
    return tweets


def get_all_followers_by_username(user_name):
    conn = sqlite3.connect(USER_DATABASE)
    cursor = conn.cursor()
    id = (username_to_id(user_name), )
    followers = []
    for row in cursor.execute('SELECT follower_id FROM followers WHERE id=?', id):
        followers.append(row[0])
    conn.close()
    return followers


def username_to_id(user_name):
    conn = sqlite3.connect(USER_DATABASE)
    cursor = conn.cursor()
    t = (user_name, )
    for row in cursor.execute('SELECT id FROM users WHERE username =?', t):
        id = row[0]
    conn.close()
    return id
