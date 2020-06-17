def map_colors(luck, nodelist, center, user_dict, type="luck", threshold=100):
    first_list = list(luck)
    second_list = list(luck)
    if type == "luck":
        first_list.sort(key=lambda x: x['luck'], reverse=True)
        second_list.sort(key=lambda x: x['luck'], reverse=True)
    elif type == "relevance_and_surprise":
        first_list.sort(key=lambda x: x['relevance'], reverse=True)
        second_list.sort(key=lambda x: x['surprise'], reverse=True)

    color_map = []

    for i, node in enumerate(nodelist):
        # Set Color
        if node == center.id:
            color_map.append('#00FF00')
        else:
            index = 0
            for x in range(threshold):
                if user_dict[node].username == first_list[x].get('username'):
                    color_map.append('#FF5733')  # orange - relevance
                    break
                elif user_dict[node].username == second_list[x].get('username'):
                    color_map.append('#CC41F2')  # pink - surprise
                    break
                index+=1
            if index >= threshold:
                color_map.append('#3390FF')
    return color_map

def map_size(luck, nodelist, center, user_dict):
    size_map = []
    for node in nodelist:
        size = 25
        if node == center.id:
            size = 250
        else:
            for x in luck:
                if x['username'] == user_dict[node].username and x['luck'] > 0:
                    size = 150
        size_map.append(size)
    return size_map

def map_labels(luck, nodelist, center, user_dict):
    label_map = {}
    for node in nodelist:
        label = ""
        if node == center.id:
            label = user_dict[node].username
        else:
            for x in luck:
                if x['username'] == user_dict[node].username and x['luck'] > 0:
                    label = x['username']
        label_map[node] = label
    return label_map

def get_topology(luck, username):
    for x in luck:
        if x['username'] == username:
            return x['topology']
    return 0 # Change this to 0 to display disconnected nodes (999)

def get_luck_value(luck, username):
    for x in luck:
        if x['username'] == username:
            return x['luck']
    return 0

def get_luck_threshold(n, luck):
    if n == 0:
        return 0
    return luck[n-1].get('luck')

def filter_topology(luck, orig_list, user, topology, user_dict):
    return [node for node in orig_list if get_topology(luck, user_dict[node].username) <= topology or node == user.id]

def filter_luck(luck, orig_list, user, luck_value, user_dict):
    return [node for node in orig_list if get_luck_value(luck, user_dict[node].username) >= luck_value or node == user.id]

def filter_excel(luck, nodes, user_dict):
    filtered_luck = []
    for user in luck:
        for node in nodes:
            if user['username'] == user_dict[node].username:
                filtered_luck.append(user)
    return filtered_luck
