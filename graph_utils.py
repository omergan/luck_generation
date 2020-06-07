def map_colors(luck, nodelist, center_id):
    color_map = []
    for node in nodelist:
        luck_value = 0
        for x in luck:
            if x['follower_id'] == node:
                luck_value = x['luck']

        # Set Color
        if node == center_id:
            color_map.append('#00FF00')
        elif luck_value > 3:
            color_map.append('#FF5733')
        elif 3.33 >= luck_value > 2.5:
            color_map.append('#F6FF33')
        elif 2.5 >= luck_value > 2:
            color_map.append('#90FF33')
        else:
            color_map.append('#3390FF')
    return color_map

def map_shapes(luck, nodelist):
    shape_map = []
    for node in nodelist:
        topology = 0

        for x in luck:
            if x['follower_id'] == node:
                topology = x['topology']
        # Set Shape
        if topology == 0:
            "."
        if topology == 2:
            shape_map.append('o')
        elif topology == 3:
            shape_map.append('D')
        elif topology == 4:
            shape_map.append('p')
        elif topology == 5:
            shape_map.append('H')
        else:
            shape_map.append('*')
    return shape_map