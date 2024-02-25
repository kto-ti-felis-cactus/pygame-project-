from random import randint


def gen_mat():
    matheight = randint(10, 20)
    matlenght = randint(20, 30)
    mat = []
    for i in range(matheight):
        mat.append(['2'] * matlenght)
    for i in range(1, matheight - 1):
        for o in range(1, matlenght - 1):
            mat[i][o] = '1'
    return mat


def gen_void(levelmat, count):
    for c in range(count):
        roomheight = randint(1, 5)
        roomlenght = randint(1, 15)
        x = randint(1, len(levelmat[0]) - roomlenght - 1)
        y = randint(1, len(levelmat) - roomheight - 1)
        ytmp = y
        for i in range(roomheight):
            xtmp = x
            ytmp += 1
            for o in range(roomlenght):
                levelmat[ytmp][xtmp] = '_'
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
    rmat = gen_void(mat, randint(2, 10))
    del mat
    save_level(rmat, '1')
    del rmat
