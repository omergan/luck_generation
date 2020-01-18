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
    user_followers = twint_api.get_followers(user, 2)
    print(user_followers)
    counter = 1
    # Checking for level 1 connection
    
    return counter