from random import randint

class Game :
    
    def __init__(self, size = 3, bombs = 10):
        self.table = [ [ [ [ 0 for i in range(size) ] for j in range(size) ] for k in range(size) ] for l in range(size) ]
        bmb = 0
        while bmb < bombs:
            coords = [ randint(0, size - 1) for i in range(4) ]
            if self.table[coords[0]][coords[1]][coords[2]][coords[3]] != -1 :
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if coords[0] + i >= 0 and coords[0] + i < size and coords[1] + j >= 0 and coords[1] + j < size and coords[2] + k >= 0 and coords[2] + k < size and\
                                    coords[3] + l >= 0 and coords[3] + l < size and self.table[coords[0] + i][coords[1] + j][coords[2] + k][coords[3] + l] != -1 :
                                    self.table[coords[0] + i][coords[1] + j][coords[2] + k][coords[3] + l] += 1
                self.table[coords[0]][coords[1]][coords[2]][coords[3]] = -1
                bmb += 1
        print(self)
    
    def __str__(self):
        text = ""
        for w in range(len(self.table)) :
            for y in range(len(self.table[w][0])) :
                for z in range(len(self.table[w])) :
                    text += str(self.table[w][z][y])
                text += "\n"
        return text
    
    def play(self, x, y, z, w):
        if self.table[w][z][y][x] == -1 :
            return False
        if self.table[w][z][y][x] == 0 :
            size = len(self.table)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if w + i >= 0 and w + i < size and z + j >= 0 and z + j < size and y + k >= 0 and y + k < size and x + l >= 0 and x + l < size :
                                self.table[w + i][z + j][y + k][x + l] = str(self.table[w + i][z + j][y + k][x + l])
        self.table[w][z][y][x] = str(self.table[w][z][y][x])
        return True
    