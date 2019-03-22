from Player import Player


class Scripting_Player(Player):
    def __init__(self, name, hand, position, game, stack):
        super().__init__(name, hand, position, game, stack)
        self.in_pot = 0
        self.value_OPR = self.game.BB*3
        self.value_3Bet = self.game.BB*10
        self.value_4Bet = self.game.BB*25
        self.value_5Bet = self.game.BB*50
        self.value_6Bet = self.game.BB*100

    def higher(self, num):
        if self.hand[0][0] >= num:
            return True
        return False

    def lower(self, num):
        if self.hand[1][0] >= num:
            return True
        return False

    @property
    def pocket_pair(self):
        if self.hand[0][0] == self.hand[1][0]:
            return True
        return False

    def pocket_pair_higher(self, num):
        if self.pocket_pair and self.lower(num):
            return True
        return False

    @property
    def suited(self):
        if self.hand[0][1] == self.hand[1][1]:
            return True
        return False

    @property
    def connected(self):
        if abs(self.hand[0][0] - self.hand[1][0]) == 1:
            return True
        return False

    def connectors(self, num):
        if self.connected and self.lower(num):
            return True
        return False

    def suited_connectors(self, num):
        if self.connectors(num) and self.suited:
            return True
        return False

    @property
    def one_gapped(self):
        if abs(self.hand[0][0] - self.hand[1][0]) == 2:
            return True
        return False

    def one_gappers(self, num):
        if self.one_gapped and self.lower(num):
            return True
        return False

    def suited_one_gappers(self, num):
        if self.one_gappers(num) and self.suited:
            return True
        return False

    def preflop(self):
        reactions = {self.value_6Bet: self.Six_Bet_Call,
                     self.value_5Bet: self.Six_Bet_Raise,
                     self.value_4Bet: self.Five_Bet_Raise,
                     self.value_3Bet: self.Four_Bet_Raise,
                     self.value_OPR: self.Three_Bet_Raise,
                     self.game.BB: self.OP_Raise}
        return reactions[self.game.current_raise]()

    def OPR_Call(self):
        OPRsCall = [self.Button_Call, self.SB_Call, self.BB_Call,
                    self.UTG_Call, self.MP_Call, self.Cut_Off_Call]
        return OPRsCall[self.position]()

    def OP_Raise(self):
        OPRs = [self.Button_Raise, self.SB_Raise, self.BB_Raise,
                self.UTG_Raise, self.MP_Raise, self.Cut_Off_Raise]
        return OPRs[self.position]()

    def UTG_Raise(self):
        range = [self.pocket_pair, self.connectors(12),
                 all([self.higher(14), self.lower(10), self.suited]),
                 all([self.higher(14), self.lower(11)])]
        if any(range):
            self.open_raise(self.value_OPR)
        else:
            self.fold

    def MP_Raise(self):
        range = [self.pocket_pair,
                 all([self.higher(14), self.lower(10)]),
                 all([self.higher(13), self.lower(11)])]
        if any(range):
            self.open_raise(self.value_OPR)
        else:
            self.fold

    def Cut_Off_Raise(self):
        range = [self.pocket_pair, self.suited_connectors(5),
                 self.suited_one_gappers(8), self.connectors(7),
                 all([self.higher(14), self.lower(6), self.suited]),
                 all([self.higher(14), self.lower(9)]),
                 all([self.higher(10), self.lower(9)])]
        if any(range):
            self.open_raise(self.value_OPR)
        else:
            self.fold

    def Button_Raise(self):
        range = [self.pocket_pair, self.higher(14),
                 all([self.higher(11), self.lower(7), self.suited]),
                 all([self.higher(11), self.lower(8)]),
                 self.connectors(4), self.one_gappers(7)]
        if any(range):
            self.open_raise(self.value_OPR)
        else:
            self.fold

    def SB_Raise(self):
        range = [self.pocket_pair, self.suited_connectors(6),
                 all([self.higher(14), self.lower(6), self.suited]),
                 all([self.higher(14), self.lower(10)]),
                 all([self.higher(11), self.lower(8), self.suited]),
                 all([self.higher(11), self.lower(9)])]
        if any(range):
            self.open_raise(self.value_OPR)
        else:
            self.fold

    def BB_Raise(self):
        range = [self.pocket_pair, self.higher(14),
                 all([self.higher(11), self.lower(7), self.suited]),
                 all([self.higher(11), self.lower(8)]),
                 self.connectors(4), self.one_gappers(7)]
        if any(range):
            self.open_raise(self.value_OPR)
        else:
            self.fold

    def UTG_Call(self):
        range = [self.pocket_pair, self.connectors(12),
                 all([self.higher(14), self.lower(10), self.suited]),
                 all([self.higher(14), self.lower(11)])]
        if any(range):
            self.call
        else:
            self.fold

    def MP_Call(self):
        range = [self.pocket_pair,
                 all([self.higher(14), self.lower(10)]),
                 all([self.higher(13), self.lower(11)])]
        if any(range):
            self.call
        else:
            self.fold

    def Cut_Off_Call(self):
        range = [self.pocket_pair, self.suited_connectors(5),
                 self.suited_one_gappers(8), self.connectors(7),
                 all([self.higher(14), self.lower(6), self.suited]),
                 all([self.higher(14), self.lower(9)]),
                 all([self.higher(10), self.lower(9)])]
        if any(range):
            self.call
        else:
            self.fold

    def Button_Call(self):
        range = [self.pocket_pair, self.higher(14),
                 all([self.higher(11), self.lower(7), self.suited]),
                 all([self.higher(11), self.lower(8)]),
                 self.connectors(4), self.one_gappers(7)]
        if any(range):
            self.call
        else:
            self.fold

    def SB_Call(self):
        range = [self.pocket_pair, self.suited_connectors(6),
                 all([self.higher(14), self.lower(6), self.suited]),
                 all([self.higher(14), self.lower(10)]),
                 all([self.higher(11), self.lower(8), self.suited]),
                 all([self.higher(11), self.lower(9)])]
        if any(range):
            self.call
        else:
            self.fold

    def BB_Call(self):
        range = [self.pocket_pair, self.higher(14),
                 all([self.higher(11), self.lower(7), self.suited]),
                 all([self.higher(11), self.lower(8)]),
                 self.connectors(4), self.one_gappers(7)]
        if any(range):
            self.call
        else:
            self.fold

    def Three_Bet_Raise(self):
        self.OPR_Call()
        if self.action:
            range = [self.pocket_pair_higher(7),
                     all([self.higher(14), self.lower(11), self.suited]),
                     all([self.higher(14), self.lower(12)]),
                     self.suited_connectors(12)]
            if any(range):
                self.re_raise(self.value_3Bet)
            else:
                self.check

    def Three_Bet_Call(self):
        range = [self.pocket_pair_higher(7),
                 all([self.higher(14), self.lower(11), self.suited]),
                 all([self.higher(14), self.lower(12)]),
                 self.suited_connectors(12)]
        if any(range):
            self.re_call
        else:
            self.fold

    def Four_Bet_Raise(self):
        self.Three_Bet_Call()
        if self.action:
            range = [self.pocket_pair_higher(11), self.connectors(13)]
            if any(range):
                self.re_raise(self.value_4Bet)
            else:
                self.check

    def Four_Bet_Call(self):
        range = [self.pocket_pair_higher(10),
                 all([self.higher(14), self.lower(12), self.suited]),
                 all([self.higher(14), self.lower(13)])]
        if any(range):
            self.re_call
        else:
            self.fold

    def Five_Bet_Raise(self):
        self.Four_Bet_Call()
        if self.action:
            range = [self.pocket_pair_higher(12), self.suited_connectors(13)]
            if any(range):
                self.re_raise(self.value_5Bet)
            else:
                self.check

    def Five_Bet_Call(self):
        if self.pocket_pair_higher(13):
            self.re_call
        else:
            self.fold

    def Six_Bet_Raise(self):
        self.Five_Bet_Call()
        if self.action:
            if self.pocket_pair_higher(14):
                self.re_raise(self.value_6Bet)
            else:
                self.check

    def Six_Bet_Call(self):
        if self.pocket_pair_higher(14):
            self.re_call
        else:
            self.fold
