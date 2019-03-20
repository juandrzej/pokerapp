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
    def __init__(self, BB, stack, players):
        self.deck = create_deck()
        self.BB = BB
        self.SB = BB/2
        self.stack = stack
        self.players = players
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
        self.flop = []
        self.turn = []
        self.river = []
        self.board = []
        self.flop.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.flop.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.flop.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.turn.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.river.append(self.deck.pop(self.deck.index(random.choice(self.deck))))
        self.board = self.flop
        self.board.extend(self.turn)
        self.board.extend(self.river)

    @property
    def print_hands(self):
        for x in range(len(self.players)):
            self.players[x].print_hand

    @property
    def print_stacks(self):
        for x in range(len(self.players)):
            print(f'Stack: {self.players[x].stack}')

    @property
    def hand_comparer_printing(self):
        for x in range(len(self.players)):
            print(self.players[x].hand_compare(self.board))

    @property
    def hand_comparer(self):
        for x in range(len(self.players)):
            self.players[x].hand_compare(self.board)

    @property
    def winner(self):  # Decides who wins
        AIs = []
        who = None
        for p in range(len(self.players)):
            if self.players[p].action:
                AIs.append(self.players[p])
        if len(AIs) == 0:
            for p in range(len(self.players)):
                if self.players[p].position == 2:
                    who = self.players[p]
                    break
            who.stack += self.pot
            return f'The winner is {who.name} without any action.'
        elif len(AIs) == 1:
            who = AIs[0]
            who.stack += self.pot
            return f'The winner is {who.name} without showdown.'
        else:
            return self.winner_2(AIs)

    def winner_2(self, AIs):  # Decides who wins
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
        self.create_board
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
    def next_round(self):
        for p in range(len(self.players)):
            if self.players[p].position == (len(self.players)-1):
                self.players[p].position = 0
            else:
                self.players[p].position += 1
        self.pot = 0
        self.deck = create_deck()
        self.raise_amt = self.BB
        for p in range(len(self.players)):
            self.players[p].hand = self.create_hand

    def play_game(self, num):
        self.print_hands
        for i in range(num):
            self.start_round
            self.preflop_round
            self.hand_comparer
            self.winner
            self.next_round
            # self.print_hands
            # print('\n\n')
        self.print_stacks
