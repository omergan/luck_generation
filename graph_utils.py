from enums import Info
def map_colors(luck, nodelist, center, user_dict, type="luck", threshold=100):
    first_list = list(luck)
    second_list = list(luck)
    if type == "luck":
        first_list.sort(key=lambda x: x['luck'], reverse=True)
        second_list.sort(key=lambda x: x['luck'], reverse=True)
    elif type in ["relevance_and_surprise", "relevance", "surprise"]:
        first_list.sort(key=lambda x: x['relevance'], reverse=True)
        second_list.sort(key=lambda x: x['surprise'], reverse=True)

    color_map = []
    show_relevance = (type == 'relevance' or type == 'relevance_and_surprise' or type == 'luck')
    show_surprise = (type == 'surprise' or type == 'relevance_and_surprise')

    for i, node in enumerate(nodelist):
        # Set Color
        if node == center.id:
            color_map.append('#00FF00')
        else:
            index = 0
            for x in range(threshold):
                if user_dict[node].username == first_list[x].get('username') and show_relevance:
                    if type == 'luck':
                        color_map.append('#FF5733')  # orange - luck
                    else:
                        color_map.append('#EEAF29')  # orange - relevance
                    break
                elif user_dict[node].username == second_list[x].get('username') and show_surprise:
                    color_map.append('#CC41F2')  # pink - surprise
                    break
                index+=1
            if index >= threshold:
                color_map.append('#3390FF')
    return color_map

def map_size(luck, nodelist, center, user_dict, type="luck", threshold=100):
    first_list = list(luck)
    second_list = list(luck)
    if type == "luck":
        first_list.sort(key=lambda x: x['luck'], reverse=True)
        second_list.sort(key=lambda x: x['luck'], reverse=True)
    elif type in ["relevance_and_surprise", "relevance", "surprise"]:
        first_list.sort(key=lambda x: x['relevance'], reverse=True)
        second_list.sort(key=lambda x: x['surprise'], reverse=True)

    size_map = []
    show_relevance = (type == 'relevance' or type == 'relevance_and_surprise' or type == 'luck')
    show_surprise = (type == 'surprise' or type == 'relevance_and_surprise')
    for i, node in enumerate(nodelist):
        # Set Color
        if node == center.id:
            size_map.append(700)
        else:
            index = 0
            for x in range(threshold):
                if user_dict[node].username == first_list[x].get('username') and show_relevance:
                    size_map.append(400)
                    break
                elif user_dict[node].username == second_list[x].get('username') and show_surprise:
                    size_map.append(400)
                    break
                index+=1
            if index >= threshold:
                size_map.append(30)
    return size_map

def map_labels(luck, nodelist, center, user_dict, type="luck", threshold=100):
    first_list = list(luck)
    second_list = list(luck)
    if type == "luck":
        first_list.sort(key=lambda x: x['luck'], reverse=True)
        second_list.sort(key=lambda x: x['luck'], reverse=True)
    elif type in ["relevance_and_surprise", "relevance", "surprise"]:
        first_list.sort(key=lambda x: x['relevance'], reverse=True)
        second_list.sort(key=lambda x: x['surprise'], reverse=True)

    label_map = {}
    show_relevance = (type == 'relevance' or type == 'relevance_and_surprise' or type == 'luck')
    show_surprise = (type == 'surprise' or type == 'relevance_and_surprise')
    for node in nodelist:
        label = ""
        if node == center.id:
            if user_dict[node].username in Info.LABEL:
                label = Info.LABEL[user_dict[node].username]
            else:
                label = user_dict[node].username
        else:
            index = 0
            for x in range(threshold):
                if user_dict[node].username == first_list[x].get('username') and show_relevance:
                    # label = user_dict[node].username
                    label = ""
                    break
                elif user_dict[node].username == second_list[x].get('username') and show_surprise:
                    # label = user_dict[node].username
                    label = ""
                    break
                index += 1
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
