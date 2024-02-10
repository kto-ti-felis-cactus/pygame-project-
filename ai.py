def find_danger(list_of_entities, type_of_entity, self_name):
    danger = []
    for i in list_of_entities:
        if type_of_entity == '[human]':
            if i != 'player':
                if i.type_of_entity == '[cuscas]':
                    danger.append((i.name, i.level * ((i.weapon_id * average_damage_level) + (i.to_the_human * -1))))
                if i.type_of_entity == '[human]':
                    if eval(self_name).group != i.group:
                        danger.append((i.name, i.level * ((i.weapon_id * average_damage_level) +
                                                          (i.to_the_noname_humans * -1))))
                    else:
                        danger.append((i.name, 0))
            else:
                danger.append(('player',
                               5 * ((5 * average_damage_level) + (eval(self_name).to_the_player * -1))))
        elif type_of_entity == '[cuscas]':
            if i != 'player':
                if i.type_of_entity == '[cuscas]':
                    danger.append((i.name, 0))
                if i.type_of_entity == '[human]':
                    danger.append((i.name, i.level * ((i.weapon_id * average_damage_level) + (i.to_the_cuscas * -1))))

            else:
                danger.append(('player',
                               5 * ((5 * average_damage_level) + (eval(self_name).to_the_player * -1))))

    return danger


class Entity:
    def __init__(self, level):
        self.level = level
        self.type_of_entity = '[NULL]'


class Human(Entity):
    def __init__(self, level, to_the_player, is_dead, weapon_id, group, position, list_of_entities, name, player_pos,
                 image_class, board):
        super().__init__(level)
        self.to_the_player = to_the_player
        self.type_of_entity = '[human]'
        self.is_dead = is_dead
        self.weapon_id = weapon_id
        self.group = group
        self.position = position[0], position[1]
        self.enemy_position = ['[NULL]', '[NULL]']
        self.list_of_entities = list_of_entities
        self.danger = find_danger(list_of_entities, self.type_of_entity, name)
        self.name = name
        self.target = '[NULL]'
        self.enemy = '[NULL]'
        self.to_the_cuscas = -5
        self.to_the_noname_humans = 0
        self.health = 10
        self.image_class = image_class
        self.image = image_class.image
        self.angle = 0
        self.board = board
        self.perseverance(player_pos)

    def perseverance(self, player_pos):
        self.update_danger()
        if self.to_the_player > 0 and self.to_the_player > 4:
            self.target = 'best to player'

        if self.to_the_player > 0 and self.to_the_player < 4:
            self.target = 'good to player'

        if self.to_the_player == 0:
            self.target = 'neutral to player'

        if self.to_the_player < 0 and self.to_the_player > -4:
            self.target = 'bad to player'

        if self.to_the_player < 0 and self.to_the_player <= -4:
            self.target = 'worst to player'

        self.check_health()

        if self.is_dead is False:
            self.do(player_pos)

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def update_danger(self):
        self.danger = find_danger(self.list_of_entities, self.type_of_entity, self.name)

    def find_max_danger(self):
        self.max_danger = ('player', 0)
        for i in self.danger:
            if i[1] > self.max_danger[1]:
                self.max_danger = i

    def do(self, player_pos):
        self.find_max_danger()
        if self.max_danger[0] == 'player':
            if self.target == 'worst to player':
                self.target = 'kill player'
        else:
            self.target = 'destroy danger'

        if self.target == 'kill player':
            self.enemy = 'player'
            self.enemy_position = player_pos

        elif self.target == 'destroy danger':
            if self.max_danger[0] != 'player':
                self.enemy = self.max_danger[0]
                self.enemy_position = eval(self.enemy).position

        if self.target == 'destroy danger' or self.target == 'kill player':
            # x - 11, y - 4

            if abs(self.enemy_position[0] - self.position[0]) != 5:
                if abs(self.enemy_position[0] - self.position[0]) < 5:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]
                else:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]
            else:
                self.position = [self.position[0], self.position[1]]

            if abs(self.enemy_position[1] - self.position[1]) != 5:
                if abs(self.enemy_position[1] - self.position[1]) < 5:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]
                else:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]
            else:
                self.position = [self.position[0], self.position[1]]
                '''if abs(self.enemy_position[0] - self.position[0]) != 5:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]
                else:
                    self.position = [self.position[0], self.position[1]]

                if abs(self.enemy_position[1] - self.position[1]) != 5:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]
                else:
                    self.position = [self.position[0], self.position[1]]'''

    def kill(self):
        self.is_dead = True

    def set_image(self, image_class):
        self.image_class = image_class
        self.image = self.image_class.image

    def all_parameters(self):
        print('>->->->->-<-<-<-<-<')
        print(f'all parameters of entity <{self.name}>')
        print('------------------')
        print(f'level: {self.level}')
        print(f'to_the_player: {self.to_the_player}')
        print(f'type_of_entity: {self.type_of_entity}')
        print(f'is_dead: {self.is_dead}')
        print(f'weapon_id: {self.weapon_id}')
        print(f'group: {self.group}')
        print(f'position: {self.position}')
        print(f'enemy_position: {self.enemy_position}')
        print(f'list_of_entities: {self.list_of_entities}')
        print(f'danger: {self.danger}')
        print(f'max_danger: {self.max_danger}')
        print(f'name: {self.name}')
        print(f'target: {self.target}')
        print(f'enemy: {self.enemy}')
        print(f'to_the_cuscas: {self.to_the_cuscas}')
        print(f'to_the_noname_humans: {self.to_the_noname_humans}')
        print(f'health: {self.health}')
        print(f'image_class: {self.image_class}')
        print(f'image: {self.image}')
        print(f'angle: {self.angle}')
        print('>->->->->-<-<-<-<-<')


class Cuscas(Entity):
    def __init__(self, level, to_the_player, is_dead, weapon_id, group, position, list_of_entities, name, player_pos,
                 image_class, board):
        super().__init__(level)
        self.to_the_player = to_the_player
        self.type_of_entity = '[cuscas]'
        self.is_dead = is_dead
        self.weapon_id = weapon_id
        self.group = group
        self.position = position[0], position[1]
        self.enemy_position = ['[NULL]', '[NULL]']
        self.list_of_entities = list_of_entities
        self.danger = find_danger(list_of_entities, self.type_of_entity, name)
        self.name = name
        self.target = '[NULL]'
        self.enemy = '[NULL]'
        self.to_the_human = -5
        self.health = 5
        self.image_class = image_class
        self.image = image_class.image
        self.angle = 0
        self.board = board
        self.perseverance(player_pos)
        '''
        self.image_class = image_class
        self.image = image_class.image
        self.angle = 0
        self.board = board
        '''

    def perseverance(self, player_pos):
        self.update_danger()
        if self.to_the_player > 0 and self.to_the_player > 4:
            self.target = 'best to player'

        if self.to_the_player > 0 and self.to_the_player < 4:
            self.target = 'good to player'

        if self.to_the_player == 0:
            self.target = 'neutral to player'

        if self.to_the_player < 0 and self.to_the_player > -4:
            self.target = 'bad to player'

        if self.to_the_player < 0 and self.to_the_player <= -4:
            self.target = 'worst to player'

        self.check_health()

        if self.is_dead is False:
            self.do(player_pos)

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def update_danger(self):
        self.danger = find_danger(self.list_of_entities, self.type_of_entity, self.name)

    def find_max_danger(self):
        self.max_danger = ('player', 0)
        for i in self.danger:
            if i[1] > self.max_danger[1]:
                self.max_danger = i

    def do(self, player_pos):
        self.find_max_danger()
        if self.max_danger[0] == 'player':
            if self.target == 'worst to player':
                self.target = 'kill player'
        else:
            self.target = 'destroy danger'

        if self.target == 'kill player':
            self.enemy = 'player'
            self.enemy_position = player_pos

        elif self.target == 'destroy danger':
            if self.max_danger[0] != 'player':
                self.enemy = self.max_danger[0]
                self.enemy_position = eval(self.enemy).position

        if self.target == ('destroy danger' or 'kill player'):
            # x - 11, y - 4

            if abs(self.enemy_position[0] - self.position[0]) != 1:
                if abs(self.enemy_position[0] - self.position[0]) < 1:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]
                else:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]
            else:
                self.position = [self.position[0], self.position[1]]

            if abs(self.enemy_position[1] - self.position[1]) != 1:
                if abs(self.enemy_position[1] - self.position[1]) < 1:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]
                else:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]
            else:
                self.position = [self.position[0], self.position[1]]

            '''if self.enemy_position[0] > self.position[0]:
                self.position = [self.position[0] + 1, self.position[1]]
            elif self.enemy_position[0] < self.position[0]:
                self.position = [self.position[0] - 1, self.position[1]]
            elif self.enemy_position[0] == self.position[0]:
                self.position = [self.position[0], self.position[1]]

            if self.enemy_position[1] > self.position[1]:
                self.position = [self.position[0], self.position[1] + 1]
            elif self.enemy_position[1] < self.position[1]:
                self.position = [self.position[0], self.position[1] - 1]
            elif self.enemy_position[1] == self.position[1]:
                self.position = [self.position[0], self.position[1]]
        elif self.target == 'destroy danger':
            if self.max_danger[0] != '[NULL]':
                self.enemy = self.max_danger[0]
                self.enemy_position = eval(self.enemy).position

                if self.enemy_position[0] > self.position[0]:
                    self.position = [self.position[0] + 1, self.position[1]]
                elif self.enemy_position[0] < self.position[0]:
                    self.position = [self.position[0] - 1, self.position[1]]
                elif self.enemy_position[0] == self.position[0]:
                    self.position = [self.position[0], self.position[1]]

                if self.enemy_position[1] > self.position[1]:
                    self.position = [self.position[0], self.position[1] + 1]
                elif self.enemy_position[1] < self.position[1]:
                    self.position = [self.position[0], self.position[1] - 1]
                elif self.enemy_position[1] == self.position[1]:
                    self.position = [self.position[0], self.position[1]]'''

    def kill(self):
        self.is_dead = True

    def set_image(self, image_class):
        self.image_class = image_class
        self.image = self.image_class.image

    def all_parameters(self):
        print('>->->->->-<-<-<-<-<')
        print(f'all parameters of entity <{self.name}>')
        print('------------------')
        print(f'level: {self.level}')
        print(f'to_the_player: {self.to_the_player}')
        print(f'type_of_entity: {self.type_of_entity}')
        print(f'is_dead: {self.is_dead}')
        print(f'weapon_id: {self.weapon_id}')
        print(f'group: {self.group}')
        print(f'position: {self.position}')
        print(f'list_of_entities: {self.list_of_entities}')
        print(f'danger: {self.danger}')
        print(f'max_danger: {self.max_danger}')
        print(f'name: {self.name}')
        print(f'target: {self.target}')
        print(f'to_the_cuscas: {self.to_the_human}')
        print('>->->->->-<-<-<-<-<')


class Robot(Entity):
    def __init__(self, level, to_the_player, is_dead, weapon_id, group, position, list_of_entities, name, player_pos,
                 image_class, board):
        super().__init__(level)
        self.to_the_player = to_the_player
        self.type_of_entity = '[robot]'
        self.is_dead = is_dead
        self.weapon_id = weapon_id
        self.group = group
        self.position = position[0], position[1]
        self.enemy_position = ['[NULL]', '[NULL]']
        self.list_of_entities = list_of_entities
        self.danger = find_danger(list_of_entities, self.type_of_entity, name)
        self.name = name
        self.target = '[NULL]'
        self.enemy = '[NULL]'
        self.to_the_cuscas = -5
        self.to_the_humans = -5
        self.health = 15
        self.image_class = image_class
        self.image = image_class.image
        self.angle = 0
        self.board = board
        self.perseverance(player_pos)

    def perseverance(self, player_pos):
        self.update_danger()
        if self.to_the_player > 0 and self.to_the_player > 4:
            self.target = 'best to player'

        if self.to_the_player > 0 and self.to_the_player < 4:
            self.target = 'good to player'

        if self.to_the_player == 0:
            self.target = 'neutral to player'

        if self.to_the_player < 0 and self.to_the_player > -4:
            self.target = 'bad to player'

        if self.to_the_player < 0 and self.to_the_player <= -4:
            self.target = 'worst to player'

        self.check_health()

        if self.is_dead is False:
            self.do(player_pos)

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def update_danger(self):
        self.danger = find_danger(self.list_of_entities, self.type_of_entity, self.name)

    def find_max_danger(self):
        self.max_danger = ('player', 0)
        for i in self.danger:
            if i[1] > self.max_danger[1]:
                self.max_danger = i

    def do(self, player_pos):
        self.find_max_danger()
        if self.max_danger[0] == 'player':
            if self.target == 'worst to player':
                self.target = 'kill player'
        else:
            self.target = 'destroy danger'

        if self.target == 'kill player':
            self.enemy = 'player'
            self.enemy_position = player_pos

        elif self.target == 'destroy danger':
            if self.max_danger[0] != 'player':
                self.enemy = self.max_danger[0]
                self.enemy_position = eval(self.enemy).position

        if self.target == 'destroy danger' or self.target == 'kill player':

            if abs(self.enemy_position[0] - self.position[0]) != 5:
                if abs(self.enemy_position[0] - self.position[0]) < 5:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]
                else:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]
            else:
                self.position = [self.position[0], self.position[1]]

            if abs(self.enemy_position[1] - self.position[1]) != 5:
                if abs(self.enemy_position[1] - self.position[1]) < 5:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]
                else:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]
            else:
                self.position = [self.position[0], self.position[1]]

    def kill(self):
        self.is_dead = True

    def set_image(self, image_class):
        self.image_class = image_class
        self.image = self.image_class.image

    def all_parameters(self):
        print('>->->->->-<-<-<-<-<')
        print(f'all parameters of entity <{self.name}>')
        print('------------------')
        print(f'level: {self.level}')
        print(f'to_the_player: {self.to_the_player}')
        print(f'type_of_entity: {self.type_of_entity}')
        print(f'is_dead: {self.is_dead}')
        print(f'weapon_id: {self.weapon_id}')
        print(f'group: {self.group}')
        print(f'position: {self.position}')
        print(f'enemy_position: {self.enemy_position}')
        print(f'list_of_entities: {self.list_of_entities}')
        print(f'danger: {self.danger}')
        print(f'max_danger: {self.max_danger}')
        print(f'name: {self.name}')
        print(f'target: {self.target}')
        print(f'enemy: {self.enemy}')
        print(f'to_the_cuscas: {self.to_the_cuscas}')
        print(f'to_the_humans: {self.to_the_humans}')
        print(f'health: {self.health}')
        print(f'image_class: {self.image_class}')
        print(f'image: {self.image}')
        print(f'angle: {self.angle}')
        print('>->->->->-<-<-<-<-<')


average_damage_level = 1
