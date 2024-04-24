from .game import Game

class GameData:
    
    game: Game
    game_size: dict
    is_game_over: bool
    bombs: int
    flags: int
    discoverd: int