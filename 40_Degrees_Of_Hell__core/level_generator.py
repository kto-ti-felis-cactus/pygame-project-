from random import randint


def gen_mat():
    matheight = randint(40, 80)
    matlenght = randint(40, 80)
    mat = []
    for i in range(matheight):
        mat.append(['_'] * matlenght)
    return mat


def gen_room(levelmat, count):
    for c in range(count):
        roomheight = randint(8, 10)
        roomlenght = randint(5, 15)
        x = randint(1, len(levelmat[0]) - roomlenght - 15)
        y = randint(1, len(levelmat) - roomheight - 10)
        ytmp = y
        for i in range(roomheight):
            xtmp = x
            ytmp += 1
            for o in range(roomlenght):
                levelmat[ytmp][xtmp] = str(randint(0, 1))
                xtmp += 1
    return levelmat


def save_level(levelmat, levelname):
    with open(f'{levelname}.txt', 'w', encoding='utf-8') as level:
        for i in range(len(levelmat)):
            levelline = ''
            for o in levelmat[i]:
                levelline += (o + ',')
            levelline = levelline[0:len(levelline) - 1]
            level.write(levelline + '\n')
    with open(f'{levelname}.txt', 'r', encoding='utf-8') as level:
        data = level.read().split('\n')
        data = data[:-2]
    with open(f'{levelname}.txt', 'w', encoding='utf-8') as level:
        level.write('\n'.join(data))


def start_process_create_level():
    mat = gen_mat()
    rmat = gen_room(mat, randint(60, 90))
    del mat
    save_level(rmat, '1')
    del rmat
