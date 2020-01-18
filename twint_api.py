import twint
USERS_DATABASE = "datasets/users.db"
TWEETS_DATABASE = "datasets/tweets.db"

def get_followers(userName, limit):
    c = twint.Config()
    c.Username = userName
    c.Database = USERS_DATABASE
    c.Limit = limit
    c.User_full = True
    followers = twint.run.Followers(c)
    return followers

def get_tweets(subject, limit):
    c = twint.Config()
    c.Search = subject
    c.Limit = limit
    c.Database = TWEETS_DATABASE
    tweets = twint.run.Search(c)
    return tweets

def get_tweets_by_username(userName, limit):
    c = twint.Config()
    c.Username = userName
    c.Limit = limit
    c.Database = TWEETS_DATABASE
    tweets = twint.run.Search(c)
    return tweets

def get_profile_by_username(user_name):
    c = twint.Config()
    c.Username = user_name
    c.Database = USERS_DATABASE
    profile = twint.run.Lookup(c)
    return profile

def get_favorites_by_username(user_name):
    c = twint.Config()
    c.Username = user_name
    c.Database = TWEETS_DATABASE
    favorites = twint.run.Favorites(c)
    return favorites
