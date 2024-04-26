from .game import Game

class GameData:
    
    game: Game
    game_size: dict
    isGameOver: bool
    bombs: int
    flags: int
    discoverd: int