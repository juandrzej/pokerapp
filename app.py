import random
from Game import Game
from NPC import Non_Player_Character


def create_players(game):
    num = game.players
    pos = list(x for x in range(num))
    game.players = []
    for x in range(num):
        p = pos.pop(pos.index(random.choice(pos)))
        game.players.append(create_p(f'Player 0{x}', p, game))


def create_p(name, position, game):
    return Non_Player_Character(name, game.create_hand,
                                position, game, game.stack)


game1 = Game(100, 10000, 6)
create_players(game1)
game1.play_game(int(input('How many games? ')))
