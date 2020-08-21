import twint
USERS_DATABASE = "datasets/users.db"
TWEETS_DATABASE = "datasets/tweets.db"

TWITTER_DATABASE = "datasets/twitter.db"


def get_followers(user_id, limit):
    c = twint.Config()
    c.User_id = user_id
    c.Store_object = True
    c.Database = TWITTER_DATABASE
    c.Limit = limit
    c.User_full = True
    c.Hide_output = False
    twint.run.Followers(c)
    return twint.output.users_list

def get_following(user_id, limit):
    c = twint.Config()
    c.User_id = user_id
    c.Store_object = True
    c.Location = True
    c.Database = TWITTER_DATABASE
    c.Limit = limit
    c.User_full = True
    c.Hide_output = False
    twint.run.Following(c)
    return twint.output.users_list

def get_tweets(context, limit):
    c = twint.Config()
    c.Search = context
    c.Location = True
    c.Limit = limit
    c.User_full = True
    c.Database = TWITTER_DATABASE
    c.Hide_output = False
    tweets = twint.run.Search(c)
    return tweets

def get_tweets_by_username(userName, limit):
    c = twint.Config()
    c.Username = userName
    c.Location = True
    c.Replies = False
    c.Limit = limit
    c.Database = TWITTER_DATABASE
    c.Hide_output = False
    tweets = twint.run.Search(c)
    return tweets

def get_profile_by_username(user_name):
    c = twint.Config()
    c.Username = user_name
    c.Store_object = True
    c.Database = TWITTER_DATABASE
    c.Hide_output = False
    twint.run.Lookup(c)

def get_tweets_from_timeline(user_name, limit):
    c = twint.Config()
    c.Username = user_name
    c.Store_object = True
    c.Retweets = True
    c.Replies = False
    c.Limit = limit
    c.Database = TWITTER_DATABASE
    c.Profile_full = False
    c.Hide_output = False
    twint.run.Profile(c)
    return twint.output.tweets_list

def get_favorites_by_username(user_name, limit):
    c = twint.Config()
    c.Username = user_name
    c.Limit = limit
    c.Store_object = True
    c.Hide_output = False
    c.Database = TWITTER_DATABASE
    twint.run.Favorites(c)
    favorites = twint.output.tweets_list
    return favorites
