import random


def create_deck():
    colors = ('H', 'D', 'C', 'S')
    card_nums = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    deck = []
    for x in colors:
        for y in card_nums:
            deck.append((y, x))
    return deck


class Game:
    def __init__(self, BB, stack):
        self.deck = create_deck()
        self.BB = BB
        self.SB = BB/2
        self.stack = stack
        self.players = []
        self.pot = 0
        self.flop = []
        self.turn = []
        self.river = []
        self.board = []
        self.raise_amt = self.BB

    @property
    def create_hand(self):
        hand = []
        hand.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        hand.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        hand.sort(reverse=True)
        return hand

    @property
    def create_board(self):
        self.flop.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.flop.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.flop.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.turn.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.river.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.board = self.flop
        self.board.extend(self.turn)
        self.board.extend(self.river)
        return self.board

    def create_player(self, name, position):
        return Player(self.BB, self.stack, name, self.create_hand, position)

    def add_players(self, *pls):
        for x in range(len(pls)):
            self.add_player(pls[x])

    def add_player(self, who):
        self.players.append(who)

    @property
    def create_ais(self):
        for x in range(len(self.players)):
            self.players[x] = self.create_ai(f'AI0{x}', x)

    def create_ai(self, name, position):
        return AI(self.BB, self.stack, name, self.create_hand, position, self)

    @property
    def winner(self):  # Decides who wins
        AIs = self.players
        hands = []
        for x in range(len(AIs)):
            hands.append(AIs[x].hand_power)
        winner = hands[0]
        who = AIs[0]
        for x in range(len(hands)):
            if hands[x][0] > winner[0]:
                winner = hands[x]
                who = AIs[x]
        for x in range(len(hands)):
            if hands[x][0] == winner[0]:
                for y in range(len(hands[x])-1):
                    if hands[x][y+1][0] < winner[y+1][0]:
                        break
                    if hands[x][y+1][0] > winner[y+1][0]:
                        winner = hands[x]
                        who = AIs[x]
                        break
        who.stack += self.pot
        return f'The winner is {who.name} with hand: {winner}'

    @property
    def start_round(self):
        for x in range(len(self.players)):
            self.players[x].action = True
            if self.players[x].position == 1:
                self.players[x].stack -= self.SB
                self.pot += self.SB
            if self.players[x].position == 2:
                self.players[x].stack -= self.BB
                self.pot += self.BB

    @property
    def preflop_round(self):
        for y in range(len(self.players)):
            if self.players[y].position == 3:
                self.players[y].preflop
                break
        for y in range(len(self.players)):
            if self.players[y].position == 4:
                self.players[y].preflop
                break
        for y in range(len(self.players)):
            if self.players[y].position == 5:
                self.players[y].preflop
                break
        for y in range(len(self.players)):
            if self.players[y].position == 0:
                self.players[y].preflop
                break
        for y in range(len(self.players)):
            if self.players[y].position == 1:
                self.players[y].preflop
                break
        for y in range(len(self.players)):
            if self.players[y].position == 2:
                self.players[y].preflop
                break

    @property
    def checking(self):
        pass

    def calling(self, who):
        if who.position == 1:
            self.pot += self.raise_amt-self.SB
            who.stack -= self.raise_amt-self.SB
        elif who.position == 2:
            self.pot += self.raise_amt-self.BB
            who.stack -= self.raise_amt-self.BB
        else:
            self.pot += self.raise_amt
            who.stack -= self.raise_amt

    def raising(self, who, how_much):
        self.raise_amt = how_much
        if who.position == 1:
            self.pot += self.raise_amt-self.SB
            who.stack -= self.raise_amt-self.SB
        elif who.position == 2:
            self.pot += self.raise_amt-self.BB
            who.stack -= self.raise_amt-self.BB
        else:
            self.pot += self.raise_amt
            who.stack -= self.raise_amt

    @property
    def folding(self):
        self.action = False


class Player(Game):
    def __init__(self, BB, stack, name, hand, position, game):
        super().__init__(BB, stack)
        self.name = name
        self.hand = hand
        self.position = position
        self.game = game
        self.action = False
        self.start_hand = tuple(hand)
        self.next = None
        self.hand_power = []

    @property
    def p_hand(self):  # Player info printer
        print(f'{self.name}\'s hand: {self.start_hand}, stack: {self.stack}, position: {self.position}.')

    @property
    def next_round(self):
        self.position += 1

    def hand_compare(self, board):  # Who has what and hand power decider
        self.hand.extend(board)
        self.hand.sort()
        flush = self.is_flush
        pair = self.is_pair
        straight = self.is_straight
        if len(pair[0]) > 4:
            pair[0].pop(0)
            pair[0].pop(0)
        if len(pair[1]) > 3:
            pair[1].pop(0)
            pair[1].pop(0)
            pair[1].pop(0)
        if straight[1]:
            self.hand_power.append(8)
            self.hand_power.append(straight[1][-1])
            return f'Straight flush : {straight}'
        elif pair[2]:
            while len(pair[2]) < 5:
                if self.hand[-1] in pair[2]:
                    self.hand.pop()
                else:
                    pair[2].append(self.hand[-1])
            self.hand_power.append(7)
            self.hand_power.append(pair[2][0])
            self.hand_power.append(pair[2][-1])
            return f'Quads: {pair[2]}'
        elif pair[1] and pair[0]:
            if len(pair[0]) > 2:
                pair[0].pop(0)
                pair[0].pop(0)
            pair[1].extend(pair[0])
            self.hand_power.append(6)
            self.hand_power.append(pair[1][0])
            self.hand_power.append(pair[1][-1])
            return f'Full house: {pair[1]}'
        elif flush:
            while len(flush) > 5:
                flush.pop(0)
            self.hand_power.append(5)
            self.hand_power.append(flush[-1])
            return f'Flush: {flush}'
        elif straight[0]:
            self.hand_power.append(4)
            self.hand_power.append(straight[0][-1])
            return f'Straight: {straight[0]}'
        elif pair[1]:
            while len(pair[1]) < 5:
                if self.hand[-1] in pair[1]:
                    self.hand.pop()
                else:
                    pair[1].insert(3, self.hand.pop())
            self.hand_power.append(3)
            self.hand_power.append(pair[1][0])
            for x in range(2):
                self.hand_power.append(pair[1][-(x+1)])
            return f'Triple: {pair[1]}'
        elif len(pair[0]) > 2:
            while len(pair[0]) < 5:
                if self.hand[-1] in pair[0]:
                    self.hand.pop()
                else:
                    pair[0].insert(4, self.hand.pop())
            self.hand_power.append(2)
            self.hand_power.append(pair[0][2])
            self.hand_power.append(pair[0][0])
            self.hand_power.append(pair[0][-1])
            return f'Two pairs: {pair[0]}'
        elif pair[0]:
            while len(pair[0]) < 5:
                if self.hand[-1] in pair[0]:
                    self.hand.pop()
                else:
                    pair[0].insert(2, self.hand.pop())
            self.hand_power.append(1)
            self.hand_power.append(pair[0][0])
            for x in range(3):
                self.hand_power.append(pair[0][-(x+1)])
            return f'Pair: {pair[0]}'
        else:
            self.hand.pop(0)
            self.hand.pop(0)
            self.hand_power.append(0)
            self.hand.reverse()
            self.hand_power.extend(self.hand)
            return f'Kicker: {self.hand}'

    @property
    def is_flush(self):
        hearts = []
        diamonds = []
        clubs = []
        spades = []
        for x in range(len(self.hand)):
            if self.hand[x][1] == 'H':
                hearts.append(self.hand[x])
            if self.hand[x][1] == 'D':
                diamonds.append(self.hand[x])
            if self.hand[x][1] == 'C':
                clubs.append(self.hand[x])
            if self.hand[x][1] == 'S':
                spades.append(self.hand[x])
        if len(hearts) >= 5:
            return hearts
        if len(diamonds) >= 5:
            return diamonds
        if len(clubs) >= 5:
            return clubs
        if len(spades) >= 5:
            return spades
        else:
            return []

    @staticmethod
    def is_straightflush(straight):
        hand = straight
        hearts = []
        diamonds = []
        clubs = []
        spades = []
        for x in range(len(hand)):
            if hand[x][1] == 'H':
                hearts.append(hand[x])
            if hand[x][1] == 'D':
                diamonds.append(hand[x])
            if hand[x][1] == 'C':
                clubs.append(hand[x])
            if hand[x][1] == 'S':
                spades.append(hand[x])
        if len(hearts) >= 5:
            return hearts
        if len(diamonds) >= 5:
            return diamonds
        if len(clubs) >= 5:
            return clubs
        if len(spades) >= 5:
            return spades
        else:
            return []

    @property
    def is_pair(self):  # Checking if any pairs, triples or quads
        hand = self.hand
        pair = []
        triple = []
        quad = []
    # Solution w/o .sort()
    # for y in range(1, (len(hand))):
    #    for x in range(len(hand)-y):
    #        if hand[x][0] == hand[x+y][0]:
    #            p += 1
        for x in range(len(hand)-1):
            if hand[x][0] == hand[x+1][0]:
                if x < (len(hand)-2) and hand[x][0] == hand[x+2][0]:
                    if x < (len(hand)-3) and hand[x][0] == hand[x+3][0]:
                        quad.extend((hand[x], hand[x+1], hand[x+2], hand[x+3]))
                        break
                    triple.extend((hand[x], hand[x+1], hand[x+2]))
                if hand[x] in triple:
                    continue
                pair.extend((hand[x], hand[x+1]))
        return pair, triple, quad

    @property
    def is_straight(self):
        hand = self.hand
        straight = []
        straight_flush = []
        for x in range(3):
            if hand[x+4][0] - hand[x+3][0] == 1:
                if hand[x+3][0] - hand[x+2][0] == 1:
                    if hand[x+2][0] - hand[x+1][0] == 1:
                        if hand[x+1][0] - hand[x][0] == 1:
                            straight = [hand[x], hand[x+1], hand[x+2],
                                        hand[x+3], hand[x+4]]
                            if straight in self.is_straightflush(straight):
                                straight_flush = straight
        return straight, straight_flush


class AI(Player):
    def __init__(self, BB, stack, name, hand, position, game):
        super().__init__(BB, stack, name, hand, position, game)

    @property
    def preflop(self):
        if self.game.raise_amt == self.game.BB:
            if self.position == 3:
                self.UTG_Raise
            if self.position == 4:
                self.MP_Raise
            if self.position == 5:
                self.Cut_Off_Raise
            if self.position == 0:
                self.Button_Raise
            if self.position == 1:
                self.Small_Blind_Raise
            if self.position == 2:
                self.Big_Blind_Raise
        if self.game.raise_amt == self.game.BB*3:
            if self.position == 3:
                self.UTG_Call
            if self.position == 4:
                self.MP_Call
            if self.position == 5:
                self.Cut_Off_Call
            if self.position == 0:
                self.Button_Call
            if self.position == 1:
                self.Small_Blind_Call
            if self.position == 2:
                self.Big_Blind_Call

    @property
    def UTG_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[1][0] >= 11:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            self.game.raising(self, 3*self.BB)
        else:
            self.game.folding

    @property
    def MP_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 11:
            self.game.raising(self, 3*self.BB)
        else:
            self.game.folding

    @property
    def Cut_Off_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
            elif self.hand[1][0] >= 9:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            self.game.raising(self, 3*self.BB)
        else:
            self.game.folding

    @property
    def Button_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 14:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
            elif self.hand[1][0] >= 8:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 5 and self.hand[1][0] == 4:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.raising(self, 3*self.BB)
        else:
            self.game.folding

    @property
    def Small_Blind_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
            elif self.hand[1][0] >= 10:
                self.game.raising(self, 3*self.BB)
            elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
                if self.hand[0][1] == self.hand[1][1]:
                    self.game.raising(self, 3*self.BB)
            elif self.hand[0][0] >= 11:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 11 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
        else:
            self.game.folding

    @property
    def Big_Blind_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 14:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.BB)
            elif self.hand[1][0] >= 8:
                self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 5 and self.hand[1][0] == 4:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.raising(self, 3*self.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.raising(self, 3*self.BB)
        else:
            self.game.folding

    @property
    def UTG_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 11:
                self.game.calling(self)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            self.game.calling(self)
        else:
            self.game.folding

    @property
    def MP_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            self.game.calling(self)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 11:
            self.game.calling(self)
        else:
            self.game.folding

    @property
    def Cut_Off_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 9:
                self.game.calling(self)
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            self.game.calling(self)
        elif self.hand[0][0] == 10 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.calling(self)
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            self.game.calling(self)
        else:
            self.game.folding

    @property
    def Button_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14:
            self.game.calling(self)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 8:
                self.game.calling(self)
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.calling(self)
        elif self.hand[0][0] == 5 and self.hand[1][0] == 4:
            self.game.calling(self)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            self.game.calling(self)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            self.game.calling(self)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.calling(self)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.calling(self)
        else:
            self.game.folding

    @property
    def Small_Blind_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 10:
                self.game.calling(self)
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[0][0] >= 11:
                self.game.calling(self)
        elif self.hand[0][0] == 11 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        else:
            self.game.folding

    @property
    def Big_Blind_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14:
            self.game.calling(self)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 8:
                self.game.calling(self)
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.calling(self)
        elif self.hand[0][0] == 5 and self.hand[1][0] == 4:
            self.game.calling(self)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            self.game.calling(self)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            self.game.calling(self)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.calling(self)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.calling(self)
        else:
            self.game.folding

    @property
    def Three_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 7:
                self.game.raising(self, 10*self.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 10*self.BB)
            elif self.hand[1][0] >= 12:
                self.game.raising(self, 10*self.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 10*self.BB)
        else:
            self.game.folding

    @property
    def Three_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 7:
                self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 12:
                self.game.calling(self)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        else:
            self.game.folding

    @property
    def Four_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 11:
                self.game.raising(self, 25*self.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 13:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 25*self.BB)
        else:
            self.game.folding

    @property
    def Four_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 10:
                self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
            elif self.hand[1][0] >= 13:
                self.game.calling(self)
        else:
            self.game.folding

    @property
    def Five_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 13:
                self.game.raising(self, 60*self.BB)
        else:
            self.game.folding

    @property
    def Five_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 13:
                self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 13:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        else:
            self.game.folding


game1 = Game(100, 10000)
game1.add_players('ai_1', 'ai_2', 'ai_3', 'ai_4', 'ai_5', 'ai_6')
game1.create_ais
board1 = game1.create_board
for x in range(len(game1.players)):
    game1.players[x].p_hand
print(f'\nBoard: {board1} \n')
game1.start_round
game1.preflop_round
for x in range(len(game1.players)):
    print(game1.players[x].hand_compare(board1))
print(f'\n{game1.winner}\n')
for x in range(len(game1.players)):
    game1.players[x].p_hand
print('\n', game1.pot)
