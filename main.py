from measuring_luck_generation import datamuse_api as datamuse
import scraper as scraper
import csv

if __name__ == '__main__':
    set_generated = datamuse.generate_set("find job", 0)
    tweets = scraper.get_random_tweets()
    with open('tweets.csv', mode='a') as tweets_file:
        fieldnames = ['screen_name', 'username', 'tweet']
        employee_writer = csv.DictWriter(tweets_file, fieldnames=fieldnames)
        employee_writer.writeheader()
        for tweet in tweets:
            employee_writer.writerow({'screen_name': tweet.__dict__['screen_name'], 'username': tweet.__dict__['username'], 'tweet': tweet.__dict__['text']})
    profile = scraper.get_twitter_profile("realDonaldTrump")
    with open('twitter_profiles.csv', mode='a') as twitter_profiles:
        fieldnames = ['name', 'username', 'birthday', 'biography', 'website', 'profile_photo', 'likes_count', 'tweets_count', 'followers_count', 'following_count']
        writer = csv.DictWriter(twitter_profiles, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(profile.to_dict())