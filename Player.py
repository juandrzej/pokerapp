
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
        self.action = False
        print(self.name, 'Fold')

    @property
    def check(self):
        print(self.name, 'Check')

    @property
    def print_hand(self):  # Player info printer
        p = self.position
        print(f'{self.name}:{self.hand}, stack:{self.stack}, position:{p}.')

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
