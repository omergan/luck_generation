import database_api as db

class User(object):
    def __init__(self, user, is_id=False):
        """ Initialize a user instance with data """
        if is_id:
            user_profile = db.get_profile_by_id(user)
        else:
            user_profile = db.get_profile(user)
        self.id = user_profile[0]
        self.name = user_profile[2]
        self.username = user_profile[3]
        self.bio = user_profile[4]
        self.location = user_profile[5]
        self.url = user_profile[6]
        self.join_date = user_profile[7]
        self.join_time = user_profile[8]
        self.tweet_count = user_profile[9]
        self.following_count = user_profile[10]
        self.followers_count = user_profile[11]
        self.likes_count = user_profile[12]
        self.verified = user_profile[15]


    def get_tweets(self):
        """ Retrieve user tweets """
        tweets = db.get_all_tweets_by_username(self.username)
        tweets_obj = []
        for tweet in tweets:
            tweets_obj.append(Tweet(tweet))
        return tweets_obj

    def __str__(self):
        return f'{self.name}'
        # return f'{self.id} : {self.name}'

class Tweet(object):
    def __init__(self, tweet):
        self.id = tweet[0]
        self.tweet = tweet[2]
        self.conversation_id = tweet[3]
        self.date = tweet[5]
        self.time = tweet[6]
        self.timezone = tweet[7]
        self.replies_count = tweet[9]
        self.likes_count = tweet[10]
        self.retweets_count = tweet[11]
        self.user_id = tweet[12]
        self.username = tweet[14]
        self.link = tweet[16]

    def __str__(self):
        return f'{self.date} {self.username} : {self.tweet}'


