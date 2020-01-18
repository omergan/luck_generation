import database_api
import twint_api
import logging
logging.basicConfig(level=logging.INFO)

def measure_tie_strength(user, candidate, keywords, context):
    # likeness
    # Topology
    # Comms
    topology_score = topology(user, candidate)
    return topology_score

def topology(user, candidate):
    logging.info(f'Calculating topology for {user} --> {candidate}')
    user_followers = twint_api.get_followers(user, 300)
    print(user_followers)
    counter = 1
    # Checking for level 1 connection
    if candidate not in user_followers:
        counter = counter + 1
        # Checking for level 2 connection
        for follower in user_followers:
            follower_followers = twint_api.get_followers(follower, 300)
            counter = counter + 1
            # Checking for level 3 connection
            if candidate not in follower_followers:
                for level_2_follower in follower_followers:
                    level_2_follower_followers = twint_api.get_followers(level_2_follower, 300)
                    counter = counter + 1
                    # Checking for level 4 connection
                    if candidate not in level_2_follower_followers:
                        for level_3_follower in level_2_follower_followers:
                            level_3_follower_followers = twint_api.get_followers(level_3_follower, 300)
                            if candidate not in level_3_follower_followers:
                                counter = counter + 1
    return counter