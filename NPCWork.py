from random import randint, choice
import datetime


def generator_random_words(names):
    output = ''
    run = True
    letters = {'0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5': 'f', '6': 'g', '7': 'h', '8': 'i', '9': 'j'}
    while run:
        number = str(randint(1, 99999))
        for i in number:
            output += letters[i]
        if output not in names:
            run = False
    return output


def make_npc(mode, names, complexity):
    output = ''
    if mode == 0:
        name = generator_random_words(names)
        output = f"{name}(Human {randint(1, 10)} {randint(-3, 3) - complexity} False {randint(1, 10)} " + \
                 f"{randint(1, 2)} [|] entities '{name}' " + \
                 "player.position animation.AnimatedSprite(load_image('npc_human_1.png') 4 1 0 0) cells.board)"
    elif mode == 1:
        name = generator_random_words(names)
        output = f"{name}(Cuscas {randint(1, 10)} {randint(-3, 3) - complexity} False 3 3 [|] entities '{name}' " + \
                 "player.position animation.AnimatedSprite(load_image('npc_cuscas_1.png') 4 1 0 0) cells.board)"
    elif mode == 2:
        name = generator_random_words(names)
        output = f"{name}(Robot {randint(2, 10)} {randint(-3, 3) - complexity} False {randint(1, 10)} " + \
                 f"{randint(1, 2)} [|] entities '{name}' " + \
                 "player.position animation.AnimatedSprite(load_image('npc_robot_1.png') 4 1 0 0) cells.board)"
    return output


def spawn_npc(map_data, entities_positions):
    while True:
        position_y = choice(map_data)
        position_x = choice(position_y)
        try:
            if map_data[map_data.index(position_y)][position_y.index(position_x)] == '2' or \
                    map_data[map_data.index(position_y)][position_y.index(position_x)] == '_' or \
                    [map_data.index(position_y), position_y.index(position_x)] in entities_positions:
                a = 5 / 0

            print(a)
        except ZeroDivisionError:
            pass
        except UnboundLocalError:
            break
    entities_positions.append([map_data.index(position_y), position_y.index(position_x)])
    return f'{position_y.index(position_x)} {map_data.index(position_y)}'


def create_npc(location, complexity, very_important_number):
    complexity = int(complexity)
    very_important_number = int(very_important_number)
    file = open('1.txt', 'r', encoding='utf-8')
    file_data = file.read().split('-</>-\n')
    if file_data[0].split(':')[0] != 'npc_objects':
        map_data = file_data[0].split('\n')
        for i in range(len(map_data)):
            map_data[i] = map_data[i].split(',')

        entities = []
        entities_positions = []
        names = []
        time_now = str(datetime.datetime.now().time())
        time_now = time_now.replace(':', ' ')
        time_now = time_now.split('.')[0]
        time_now = [int(x) for x in time_now.split()]
        time_now = sum(time_now)
        time_now *= very_important_number
        time_now = str(time_now)
        time_now = time_now.replace('0', '1')
        time_now = list(time_now)
        if len(time_now) < 3:
            time_now = [1, time_now[0], time_now[1]]
        time_now = [int(x) for x in time_now]

        quantity_of_cuscass = int(max(time_now))
        time_now.pop(time_now.index(quantity_of_cuscass))
        quantity_of_robots = int(min(time_now))
        time_now.pop(time_now.index(quantity_of_robots))
        quantity_of_humans = int(time_now[0])
        del time_now

        for i in range(quantity_of_humans):
            npc = make_npc(0, names, complexity)
            npc = npc.replace('|', str(spawn_npc(map_data, entities_positions)))
            entities.append(npc)

        for i in range(quantity_of_cuscass):
            npc = make_npc(1, names, complexity)
            npc = npc.replace('|', str(spawn_npc(map_data, entities_positions)))
            entities.append(npc)

        for i in range(quantity_of_robots):
            npc = make_npc(2, names, complexity)
            npc = npc.replace('|', str(spawn_npc(map_data, entities_positions)))
            entities.append(npc)

        entities = 'npc_objects:[' + ';\n             '.join(entities) + ';\n             player]:\n-</>-\n'
        file.close()
        file = open('1.txt', 'r', encoding='utf-8')
        file_data = file.read()
        file.close()
        file = open('1.txt', 'w')
        file.write(entities + file_data)
    file.close()

