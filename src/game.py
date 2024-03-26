from random import randint


class Game:

    def __init__(self, size, bombs):
        self.table = [
            [
                [[0 for i in range(size["X"])] for j in range(size["Y"])]
                for k in range(size["Z"])
            ]
            for l in range(size["W"])
        ]
        bmb = 0
        while bmb < bombs:
            coords = [
                randint(0, size["W"] - 1),
                randint(0, size["Z"] - 1),
                randint(0, size["Y"] - 1),
                randint(0, size["X"] - 1),
            ]
            if self.table[coords[0]][coords[1]][coords[2]][coords[3]] != -1:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if (
                                    coords[0] + i >= 0
                                    and coords[0] + i < size["W"]
                                    and coords[1] + j >= 0
                                    and coords[1] + j < size["Z"]
                                    and coords[2] + k >= 0
                                    and coords[2] + k < size["Y"]
                                    and coords[3] + l >= 0
                                    and coords[3] + l < size["X"]
                                    and self.table[coords[0] + i][coords[1] + j][
                                        coords[2] + k
                                    ][coords[3] + l]
                                    != -1
                                ):
                                    self.table[coords[0] + i][coords[1] + j][
                                        coords[2] + k
                                    ][coords[3] + l] += 1
                self.table[coords[0]][coords[1]][coords[2]][coords[3]] = -1
                bmb += 1

    def __str__(self):
        text = ""
        for w in range(len(self.table)):
            for y in range(len(self.table[w][0])):
                for z in range(len(self.table[w])):
                    text += str(self.table[w][z][y])
                text += "\n"
            text += "\n"
        return text
