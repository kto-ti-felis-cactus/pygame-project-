from random import randint


def gen_mat():
    matheight = randint(20,40)
    matlenght = randint(30, 40)
    mat = []
    print(matheight, matlenght)
    for i in range(matheight):
        mat.append(['2'] * matlenght)
    for i in range(1, matheight - 1):
        for o in range(1, matlenght - 1):
            mat[i][o] = '1'
    return mat


def gen_void(levelmat, count):
    for c in range(count):
        roomheight = randint(1, 15)
        roomlenght = randint(1, 15)
        x = randint(1, len(levelmat[0]) - roomlenght - 1)
        y = randint(1, len(levelmat) - roomheight - 1)
        ytmp = y
        for i in range(roomheight):
            xtmp = x
            ytmp += 1
            for o in range(roomlenght):
                levelmat[ytmp][xtmp] = '-'
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


while input('Создать уровень? - Да\Нет\n') != 'Нет':
    mat = gen_mat()
    rmat = gen_void(mat, int(input('Кол-во пустот (могут пересекаться в одну большую)\n')))
    for i in rmat:
        print(i)
    if input('сохранить уровень? - Да\Нет\n') == 'Да':
        save_level(rmat, input('напишите название уровня\n'))
    else:
        print('ок')

