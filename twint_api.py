import twint
USER_DATABASE = "datasets/users.db"
TWEETS_DATABASE = "datasets/tweets.db"

def get_followers(userName, limit):
    c = twint.Config()
    c.Username = userName
    c.Database = USER_DATABASE
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