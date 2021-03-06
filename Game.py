import random
from operator import attrgetter


def create_deck():  # H = Hearts, D = Diamonds, C = Clubs, S =Spades
    colors = ('H', 'D', 'C', 'S')
    card_nums = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    deck = []
    for x in colors:
        for y in card_nums:
            deck.append((y, x))
    random.shuffle(deck)
    return deck


class Game:
    def __init__(self, BB, stack, players):
        self.BB = BB
        self.SB = BB/2
        self.stack = stack
        self.players = players
        self.pot = 0
        self.deck = create_deck()
        self.flop = []
        self.turn = []
        self.river = []
        self.board = []
        self.current_raise = self.BB

    @property
    def create_hand(self):
        hand = []
        hand.append(self.deck.pop())
        hand.append(self.deck.pop())
        hand.sort(reverse=True)
        return hand

    @property
    def create_board(self):
        self.flop = []
        self.turn = []
        self.river = []
        self.board = []
        self.flop.append(self.deck.pop())
        self.flop.append(self.deck.pop())
        self.flop.append(self.deck.pop())
        self.turn.append(self.deck.pop())
        self.river.append(self.deck.pop())
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

    def check(self, who):
        print(who.name, 'Check')

    def fold(self, who):
        print(who.name, 'Fold')
        who.action = False

    def call(self, who):
        print(who.name, 'Call')
        who.in_pot = self.current_raise
        if who.position == 1:
            self.pot += self.current_raise-self.SB
            who.stack -= self.current_raise-self.SB
        elif who.position == 2:
            self.pot += self.current_raise-self.BB
            who.stack -= self.current_raise-self.BB
        else:
            self.pot += self.current_raise
            who.stack -= self.current_raise

    def re_call(self, who):
        print(who.name, 'Re-call')
        who.in_pot = self.current_raise
        self.pot += self.current_raise
        who.stack -= self.current_raise

    def open_raise(self, who, how_much):
        print(who.name, 'Raise')
        self.current_raise = how_much
        who.in_pot = self.current_raise
        if who.position == 1:
            self.pot += self.current_raise-self.SB
            who.stack -= self.current_raise-self.SB
        elif who.position == 2:
            self.pot += self.current_raise-self.BB
            who.stack -= self.current_raise-self.BB
        else:
            self.pot += self.current_raise
            who.stack -= self.current_raise

    def re_raise(self, who, how_much):
        print(who.name, 'Re-raise')
        self.current_raise = how_much
        who.in_pot = self.current_raise
        self.pot += self.current_raise
        who.stack -= self.current_raise

    def winner(self):  # Decides who wins
        active_players = []
        who = None
        for p in range(len(self.players)):
            if self.players[p].action:
                active_players.append(self.players[p])
        if len(active_players) == 0:
            for p in range(len(self.players)):
                if self.players[p].position == 2:
                    who = self.players[p]
                    break
            who.stack += self.pot
            return f'The winner is {who.name} without any action.'
        elif len(active_players) == 1:
            who = active_players[0]
            who.stack += self.pot
            return f'The winner is {who.name} without showdown.'
        else:
            return self.winner_2(active_players)

    def winner_2(self, active_players):  # Decides who wins
        hands = []
        for x in range(len(active_players)):
            hands.append(active_players[x].hand_power)
        winner = hands[0]
        who = active_players[0]
        for x in range(len(hands)):
            if hands[x][0] > winner[0]:
                winner = hands[x]
                who = active_players[x]
        for x in range(len(hands)):
            if hands[x][0] == winner[0]:
                for y in range(len(hands[x])-1):
                    if hands[x][y+1][0] < winner[y+1][0]:
                        break
                    if hands[x][y+1][0] > winner[y+1][0]:
                        winner = hands[x]
                        who = active_players[x]
                        break
        who.stack += self.pot
        return f'The winner is {who.name} with hand: {winner}'

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

    def preflop_round(self):
        active_players = self.players
        active_players = sorted(active_players, key=attrgetter('position'))
        active_players.append(active_players.pop(0))
        active_players.append(active_players.pop(0))
        active_players.append(active_players.pop(0))
        act_players = []
        for p in range(len(active_players)):
            active_players[p].preflop()
            # print(active_players[p].in_pot)
            if active_players[p].action:
                act_players.append(active_players[p])
        print(f'First circle: {self.pot}')
        act_players2 = []
        if len(act_players) > 1:
            for a in range(len(act_players)):
                if act_players[a].in_pot < self.current_raise:
                    act_players[a].preflop()
                    if act_players[a].action:
                        act_players2.append(act_players[a])
        print(f'Second circle: {self.pot}')
        if len(act_players2) > 1:
            for a in range(len(act_players2)):
                if act_players2[a].in_pot < self.current_raise:
                    act_players2[a].preflop()
        print(f'Third circle: {self.pot}')

    def next_round(self):
        for p in range(len(self.players)):
            if self.players[p].position == (len(self.players)-1):
                self.players[p].position = 0
            else:
                self.players[p].position += 1
        self.pot = 0
        self.deck = create_deck()
        self.current_raise = self.BB
        for p in range(len(self.players)):
            self.players[p].in_pot = 0
            self.players[p].hand = self.create_hand

    def play_game(self, num):
        self.print_hands
        for i in range(num):
            self.start_round()
            print(self.board)
            self.preflop_round()
            self.hand_comparer
            self.winner()
            self.next_round()
            self.print_hands
            print('\n\n')
