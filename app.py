import random
from gameclass import Game
from playerclass import AI


def create_ais(game):
    num = game.players
    pos = list(x for x in range(num))
    game.players = []
    for x in range(num):
        game.players.append(create_ai(game, f'AI0{x}', pos.pop(pos.index(random.choice(pos)))))


def create_ai(game, name, position):
    return AI(name, game.create_hand, position, game, game.stack)


game1 = Game(100, 10000, 6)
create_ais(game1)
game1.play_game(int(input('How many games? ')))
