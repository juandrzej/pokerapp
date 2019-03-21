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

    @property
    def preflop(self):
        reactions = {self.value_6Bet: self.Six_Bet_Call,
                     self.value_5Bet: self.BB50,
                     self.value_4Bet: self.BB25,
                     self.value_3Bet: self.BB10,
                     self.value_OPR: self.BB3,
                     self.game.BB: self.Open_Raise}
        return reactions[self.game.raise_amt]()

    def BB50(self):
        self.Five_Bet_Call
        if self.action:
            self.Six_Bet_Raise

    def BB25(self):
        self.Four_Bet_Call
        if self.action:
            self.Five_Bet_Raise

    def BB10(self):
        self.Three_Bet_Call
        if self.action:
            self.Four_Bet_Raise

    def BB3(self):
        self.OPR_Call
        if self.action:
            self.Three_Bet_Raise

    @property
    def OPR_Call(self):
        OPRsCall = [self.Button_Call, self.SB_Call, self.BB_Call,
                    self.UTG_Call, self.MP_Call, self.Cut_Off_Call]
        return OPRsCall[self.position]()

    def Open_Raise(self):
        OPRs = [self.Button_Raise, self.SB_Raise, self.BB_Raise,
                self.UTG_Raise, self.MP_Raise, self.Cut_Off_Raise]
        return OPRs[self.position]()

    def UTG_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(14) and self.lower(10):
            if self.suited or self.lower(11):
                self.game.raising(self, 3*self.game.BB)
            else:
                self.fold
        elif self.connectors(12):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.fold

    def MP_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(14) and self.lower(10):
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(13) and self.lower(11):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.fold

    def Cut_Off_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(14) and self.lower(6):
            if self.suited or self.lower(9):
                self.game.raising(self, 3*self.game.BB)
            else:
                self.fold
        elif self.higher(10) and self.lower(9):
            self.game.raising(self, 3*self.game.BB)
        elif self.suited_one_gappers(8):
            self.game.raising(self, 3*self.game.BB)
        elif self.suited_connectors(5):
            self.game.raising(self, 3*self.game.BB)
        elif self.connectors(7):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.fold

    def Button_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(14):
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(11) and self.lower(7):
            if self.suited or self.lower(8):
                self.game.raising(self, 3*self.game.BB)
            else:
                self.fold
        elif self.one_gappers(7):
            self.game.raising(self, 3*self.game.BB)
        elif self.connectors(4):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.fold

    def SB_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(14) and self.lower(6):
            if self.suited or self.lower(10):
                self.game.raising(self, 3*self.game.BB)
            else:
                self.fold
        elif self.higher(11) and self.lower(8):
            if self.suited or self.lower(9):
                self.game.raising(self, 3*self.game.BB)
            else:
                self.fold
        elif self.suited_connectors(6):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.fold

    def BB_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(14):
            self.game.raising(self, 3*self.game.BB)
        elif self.higher(11) and self.lower(7):
            if self.suited or self.lower(8):
                self.game.raising(self, 3*self.game.BB)
            else:
                self.fold
        elif self.one_gappers(7):
            self.game.raising(self, 3*self.game.BB)
        elif self.connectors(4):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.fold

    def UTG_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.higher(14) and self.lower(10):
            if self.suited or self.lower(11):
                self.game.calling(self)
            else:
                self.fold
        elif self.connectors(12):
            self.game.calling(self)
        else:
            self.fold

    def MP_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.higher(14) and self.lower(10):
            self.game.calling(self)
        elif self.higher(13) and self.lower(11):
            self.game.calling(self)
        else:
            self.fold

    def Cut_Off_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.higher(14) and self.lower(6):
            if self.suited or self.lower(9):
                self.game.calling(self)
            else:
                self.fold
        elif self.higher(10) and self.lower(9):
            self.game.calling(self)
        elif self.suited_one_gappers(8):
            self.game.calling(self)
        elif self.suited_connectors(5):
            self.game.calling(self)
        elif self.connectors(7):
            self.game.calling(self)
        else:
            self.fold

    def Button_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.higher(14):
            self.game.calling(self)
        elif self.higher(11) and self.lower(7):
            if self.suited or self.lower(8):
                self.game.calling(self)
            else:
                self.fold
        elif self.connectors(4):
            self.game.calling(self)
        elif self.one_gappers(7):
            self.game.calling(self)
        else:
            self.fold

    def SB_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.higher(14) and self.lower(6):
            if self.suited or self.lower(10):
                self.game.calling(self)
            else:
                self.fold
        elif self.higher(11) and self.lower(8):
            if self.suited or self.lower(9):
                self.game.calling(self)
            else:
                self.fold
        elif self.suited_connectors(6):
            self.game.calling(self)
        else:
            self.fold

    def BB_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.higher(14):
            self.game.calling(self)
        elif self.higher(11) and self.lower(7):
            if self.suited or self.lower(8):
                self.game.calling(self)
            else:
                self.fold
        elif self.connectors(4):
            self.game.calling(self)
        elif self.one_gappers(7):
            self.game.calling(self)
        else:
            self.fold

    def Three_Bet_Raise(self):
        if self.pocket_pair_higher(7):
            self.game.re_raising(self, 10*self.game.BB)
        elif self.higher(14) and self.lower(11):
            if self.suited or self.lower(12):
                self.game.re_raising(self, 10*self.game.BB)
            else:
                self.check
        elif self.suited_connectors(12):
            self.game.re_raising(self, 10*self.game.BB)
        else:
            self.check

    def Three_Bet_Call(self):
        if self.pocket_pair_higher(7):
            self.game.re_calling(self)
        elif self.higher(14) and self.lower(11):
            if self.suited or self.lower(12):
                self.game.re_calling(self)
            else:
                self.fold
        elif self.suited_connectors(12):
            self.game.re_calling(self)
        else:
            self.fold

    def Four_Bet_Raise(self):
        if self.pocket_pair_higher(11):
            self.game.re_raising(self, 25*self.game.BB)
        elif self.connectors(13):
            self.game.re_raising(self, 25*self.game.BB)
        else:
            self.check

    def Four_Bet_Call(self):
        if self.pocket_pair_higher(10):
            self.game.re_calling(self)
        elif self.higher(14) and self.lower(12):
            if self.suited or self.lower(13):
                self.game.re_calling(self)
            else:
                self.fold
        else:
            self.fold

    def Five_Bet_Raise(self):
        if self.pocket_pair_higher(12):
            self.game.re_raising(self, 50*self.game.BB)
        elif self.suited_connectors(13):
            self.game.re_raising(self, 50*self.game.BB)
        else:
            self.check

    def Five_Bet_Call(self):
        if self.pocket_pair_higher(13):
            self.game.re_calling(self)
        else:
            self.fold

    def Six_Bet_Raise(self):
        if self.pocket_pair_higher(14):
            self.game.re_raising(self, 100*self.game.BB)
        else:
            self.check

    def Six_Bet_Call(self):
        if self.pocket_pair_higher(14):
            self.game.re_calling(self)
        else:
            self.fold
