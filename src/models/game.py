from random import randint


class Game:

    def __init__(self, size, bombs, start_coords):
        self.table = [
            [
                [[0 for _ in range(size["X"])] for _ in range(size["Y"])]
                for _ in range(size["Z"])
            ]
            for _ in range(size["W"])
        ]
        self._generate_table(size, bombs, start_coords)

    def _generate_table(self, size, bombs, start_coords):
        bmb = 0
        nb_try = 0
        while bmb < bombs:
            coords = [
                randint(0, size["W"] - 1),
                randint(0, size["Z"] - 1),
                randint(0, size["Y"] - 1),
                randint(0, size["X"] - 1),
            ]
            # si il n'y a pas de bombe sur la case
            # la bombs ne peut pas être sur la case de départ
            if self.table[coords[0]][coords[1]][coords[2]][coords[3]] != -1  and coords != start_coords:
                print(coords, nb_try)
                # la bombs ne peut pas être sur la un voisin de la case de départ
                # si sur 25 tentatives on a pas trouvé de case valide on accepte les voisins
                if nb_try >= 25 or ( abs(coords[0] - start_coords[0]) > 1 or abs(coords[1] - start_coords[1]) > 1 or abs(coords[2] - start_coords[2]) > 1 or abs(coords[3] - start_coords[3]) > 1 ):
                    self._set_bombs(coords, size)
                    bmb += 1
                    nb_try = 0
                else :
                    nb_try += 1

    def _set_bombs(self, coords, size):
        neighbors_range = range(-1, 2)
        for i in neighbors_range:
            for j in neighbors_range:
                for k in neighbors_range:
                    for l in neighbors_range:
                        self._set_neighbors_to_bombs(
                            [
                                coords[0] + i,
                                coords[1] + j,
                                coords[2] + k,
                                coords[3] + l,
                            ],
                            size,
                        )
        self.table[coords[0]][coords[1]][coords[2]][coords[3]] = -1

    def _set_neighbors_to_bombs(self, coords, size):
        if (
            coords[0] >= 0
            and coords[0] < size["W"]
            and coords[1] >= 0
            and coords[1] < size["Z"]
            and coords[2] >= 0
            and coords[2] < size["Y"]
            and coords[3] >= 0
            and coords[3] < size["X"]
            and self.table[coords[0]][coords[1]][coords[2]][coords[3]] != -1
        ):
            self.table[coords[0]][coords[1]][coords[2]][coords[3]] += 1

    def __str__(self):
        text = ""
        for w in range(len(self.table)):
            for y in range(len(self.table[w][0])):
                for z in range(len(self.table[w])):
                    text += str(self.table[w][z][y])
                text += "\n"
            text += "\n"
        return text
