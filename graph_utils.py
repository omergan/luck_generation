def map_colors(luck, nodelist, center_id, user_dict):
    color_map = []
    for node in nodelist:
        luck_value = 0
        for x in luck:
            if x['username'] == user_dict[node].username:
                luck_value = x['luck']

        # Set Color
        luck_threshold = get_luck_threshold(10, luck)  # top 10 will be marked as red
        if node == center_id:
            color_map.append('#00FF00')
        elif luck_value >= luck_threshold:
            color_map.append('#FF5733')
        elif luck_threshold > luck_value > 2.5:
            color_map.append('#F6FF33')
        # elif 2.5 >= luck_value > 2:
        #     color_map.append('#90FF33')
        else:
            color_map.append('#3390FF')
    return color_map

def map_size(luck, nodelist, center_id, user_dict):
    size_map = []
    for node in nodelist:
        size = 25
        for x in luck:
            if x['username'] == user_dict[node].username and x['luck'] > 0:
                size = 150
        size_map.append(size)
    return size_map

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