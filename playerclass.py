
class Player:
    def __init__(self, name, hand, position, game, stack):
        self.name = name
        self.hand = hand
        self.position = position
        self.game = game
        self.stack = stack
        self.action = False
        self.hand_power = []

    @property
    def folding(self):
        self.action = False

    @property
    def print_hand(self):  # Player info printer
        print(f'{self.name}\'s hand: {self.hand}, stack: {self.stack}, position: {self.position}.')

    def hand_compare(self, board):  # Who has what and hand power decider
        self.hand_power = []
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
    def __init__(self, name, hand, position, game, stack):
        super().__init__(name, hand, position, game, stack)

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
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[1][0] >= 11:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding

    @property
    def MP_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 11:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding

    @property
    def Cut_Off_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 9:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding

    @property
    def Button_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 8:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 5 and self.hand[1][0] == 4:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding

    @property
    def Small_Blind_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 10:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
                if self.hand[0][1] == self.hand[1][1]:
                    self.game.raising(self, 3*self.game.BB)
            elif self.hand[0][0] >= 11:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 11 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
        else:
            self.folding

    @property
    def Big_Blind_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 8:
                self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 5 and self.hand[1][0] == 4:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding

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
            self.folding

    @property
    def MP_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            self.game.calling(self)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 11:
            self.game.calling(self)
        else:
            self.folding

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
            self.folding

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
            self.folding

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
            self.folding

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
            self.folding

    @property
    def Three_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 7:
                self.game.raising(self, 10*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 10*self.game.BB)
            elif self.hand[1][0] >= 12:
                self.game.raising(self, 10*self.game.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 10*self.game.BB)
        else:
            self.game.checking

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
            self.folding

    @property
    def Four_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 11:
                self.game.raising(self, 25*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 13:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.raising(self, 25*self.game.BB)
        else:
            self.game.checking

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
            self.folding

    @property
    def Five_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 13:
                self.game.raising(self, 60*self.game.BB)
        else:
            self.game.checking

    @property
    def Five_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 13:
                self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 13:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.calling(self)
        else:
            self.folding
