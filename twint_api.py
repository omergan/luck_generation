import twint
USERS_DATABASE = "datasets/users.db"
TWEETS_DATABASE = "datasets/tweets.db"

def get_followers(user_id, limit):
    c = twint.Config()
    c.User_id = user_id
    c.Store_object = True
    c.Database = USERS_DATABASE
    c.Limit = limit
    c.User_full = True
    # c.Hide_output = True
    twint.run.Followers(c)
    return twint.output.users_list

def get_following(user_id, limit):
    c = twint.Config()
    c.User_id = user_id
    c.Store_object = True
    c.Database = USERS_DATABASE
    c.Limit = limit
    c.User_full = True
    # c.Hide_output = True
    twint.run.Following(c)
    return twint.output.users_list

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
    c.Store_object = True
    c.Database = USERS_DATABASE
    twint.run.Lookup(c)
    return twint.output.users_list

def get_tweets_from_timeline(user_name, limit):
    c = twint.Config()
    c.Username = user_name
    c.Store_object = True
    c.Retweets = True
    c.Replies = True
    c.Limit = limit
    c.Database = TWEETS_DATABASE
    c.Profile_full = True
    twint.run.Profile(c)
    return twint.output.tweets_list

def get_favorites_by_username(user_name, limit):
    c = twint.Config()
    c.Username = user_name
    c.Limit = limit
    c.Store_object = True
    c.Database = TWEETS_DATABASE
    twint.run.Favorites(c)
    favorites = twint.output.tweets_list

    return favorites
