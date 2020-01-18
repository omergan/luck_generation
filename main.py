from measuring_luck_generation import generating_luck
import twint_api

followers = twint_api.get_followers("1212035324102111238", 100)
print(followers)
# generating_luck.generating_luck(1325385696, "software engineering job")
