
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
    def fold(self):
        self.game.fold(self)

    @property
    def check(self):
        self.game.check(self)

    @property
    def call(self):
        self.game.call(self)

    @property
    def re_call(self):
        self.game.re_call(self)

    def open_raise(self, amount):
        self.game.open_raise(self, amount)

    def re_raise(self, amount):
        self.game.re_raise(self, amount)

    @property
    def print_hand(self):  # Player info printer
        p = self.position
        print(f'{self.name}:{self.hand}, stack:{self.stack}, position:{p}.')

    def hand_compare(self, board):  # Who has what and hand power decider
        self.hand_power = []
        self.hand.extend(board)
        self.hand.sort()
        flush = self.is_flush(self.hand)
        pair = self.is_pair_triple_quad(self.hand)[0]
        triple = self.is_pair_triple_quad(self.hand)[1]
        quad = self.is_pair_triple_quad(self.hand)[2]
        straight = self.is_straight_straightflush(self.hand)[0]
        straight_flush = self.is_straight_straightflush(self.hand)[1]
        if straight_flush:
            self.hand_power.append(8)
            self.hand_power.append(straight_flush[-1])
            return f'Straight flush : {straight_flush}'
        elif quad:
            while len(quad) < 5:
                if self.hand[-1] in quad:
                    self.hand.pop()
                else:
                    quad.append(self.hand[-1])
            self.hand_power.append(7)
            self.hand_power.append(quad[0])
            self.hand_power.append(quad[-1])
            return f'Quads: {quad}'
        elif triple and pair:
            if len(pair) > 2:
                pair.pop(0)
                pair.pop(0)
            triple.extend(pair)
            self.hand_power.append(6)
            self.hand_power.append(triple[0])
            self.hand_power.append(triple[-1])
            return f'Full house: {triple}'
        elif flush:
            while len(flush) > 5:
                flush.pop(0)
            self.hand_power.append(5)
            self.hand_power.append(flush[-1])
            return f'Flush: {flush}'
        elif straight:
            self.hand_power.append(4)
            self.hand_power.append(straight[-1])
            return f'Straight: {straight}'
        elif triple:
            while len(triple) < 5:
                if self.hand[-1] in triple:
                    self.hand.pop()
                else:
                    triple.insert(3, self.hand.pop())
            self.hand_power.append(3)
            self.hand_power.append(triple[0])
            for x in range(2):
                self.hand_power.append(triple[-(x+1)])
            return f'Triple: {triple}'
        elif len(pair) > 2:
            while len(pair) < 5:
                if self.hand[-1] in pair:
                    self.hand.pop()
                else:
                    pair.insert(4, self.hand.pop())
            self.hand_power.append(2)
            self.hand_power.append(pair[2])
            self.hand_power.append(pair[0])
            self.hand_power.append(pair[-1])
            return f'Two pairs: {pair}'
        elif pair:
            while len(pair) < 5:
                if self.hand[-1] in pair:
                    self.hand.pop()
                else:
                    pair.insert(2, self.hand.pop())
            self.hand_power.append(1)
            self.hand_power.append(pair[0])
            for x in range(3):
                self.hand_power.append(pair[-(x+1)])
            return f'Pair: {pair}'
        else:
            self.hand.pop(0)
            self.hand.pop(0)
            self.hand_power.append(0)
            self.hand.reverse()
            self.hand_power.extend(self.hand)
            return f'Kicker: {self.hand}'

    def is_flush(self, hand):
        hearts, diamonds, clubs, spades = [], [], [], []
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

    def is_pair_triple_quad(self, hand):
        pair, triple, quad = [], [], []
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
        if len(pair) > 4:
            pair.pop(0)
            pair.pop(0)
        if len(triple) > 3:
            triple.pop(0)
            triple.pop(0)
            triple.pop(0)
        return pair, triple, quad

    def is_straight_straightflush(self, hand):
        straight, straight_flush = [], []
        for x in range(3):
            if hand[x+4][0] - hand[x+3][0] == 1:
                if hand[x+3][0] - hand[x+2][0] == 1:
                    if hand[x+2][0] - hand[x+1][0] == 1:
                        if hand[x+1][0] - hand[x][0] == 1:
                            straight = [hand[x], hand[x+1], hand[x+2],
                                        hand[x+3], hand[x+4]]
                            if self.is_flush(straight):
                                straight_flush = straight
        return straight, straight_flush
