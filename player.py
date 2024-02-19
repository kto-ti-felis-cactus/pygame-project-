class Player:
    def __init__(self, stats_path, position, image_name):
        self.stats_path = stats_path
        self.position = position
        self.type_of_entity = '[player]'
        self.player_data = {}
        self.image_class = image_name
        self.health = 10

    def read_player_stats(self):
        file = open(fr'player_stats\{self.stats_path}.txt', 'r', encoding='utf-8')
        for i in file.read().split('\n'):
            self.player_data[i.split('--')[0]] = i.split('--')[1]
        file.close()

    def write_player_stats(self):
        file = open(fr'{self.stats_path}.txt', 'w', encoding='utf-8')
        output = ''
        for i in self.player_data.keys():
            output += f'{i}--{self.player_data[i]}\n'
        file.write(output)
        file.close()

    def set_image(self, image_name):
        self.image_class = image_name

