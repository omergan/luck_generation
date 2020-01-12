import database_api

followers = database_api.get_all_followers_by_username('IaakovExman')
print(followers)