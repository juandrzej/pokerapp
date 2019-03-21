from Player import Player


class Scripting_Player(Player):
    def __init__(self, name, hand, position, game, stack):
        super().__init__(name, hand, position, game, stack)
        self.in_pot = 0

    @property
    def pocket_pair(self):
        if self.hand[0][0] == self.hand[1][0]:
            return True
        else:
            return False

    def pocket_pair_higher(self, num):
        if self.pocket_pair and self.lower(num):
            return True
        else:
            return False

    @property
    def suited(self):
        if self.hand[0][1] == self.hand[1][1]:
            return True
        else:
            return False

    @property
    def connected(self):
        if abs(self.hand[0][0] - self.hand[1][0]) == 1:
            return True
        else:
            return False

    def lower(self, num):
        if self.hand[1][0] >= num:
            return True
        else:
            return False

    def connectors(self, num):
        if self.connected and self.lower(num):
            return True
        else:
            return False

    def suited_connectors(self, num):
        if self.connectors(num) and self.suited:
            return True
        else:
            return False

    @property
    def preflop(self):
        reactions = {self.game.BB*100: self.BB100, self.game.BB*50: self.BB50,
                     self.game.BB*25: self.BB25, self.game.BB*10: self.BB10,
                     self.game.BB*3: self.BB3, self.game.BB: self.BB1}
        return reactions[self.game.raise_amt]

    @property
    def BB100(self):
        print(self.name, '6betC')
        self.Six_Bet_Call

    @property
    def BB50(self):
        print(self.name, '5betC')
        self.Five_Bet_Call
        if self.action:
            print(self.name, '6betR')
            self.Six_Bet_Raise

    @property
    def BB25(self):
        print(self.name, '4betC')
        self.Four_Bet_Call
        if self.action:
            print(self.name, '5betR')
            self.Five_Bet_Raise

    @property
    def BB10(self):
        print(self.name, '3betC')
        self.Three_Bet_Call
        if self.action:
            print(self.name, '4betR')
            self.Four_Bet_Raise

    @property
    def BB3(self):
        print(self.name, 'Call')
        self.OPR_Call
        if self.action:
            print(self.name, '3betR')
            self.Three_Bet_Raise

    @property
    def BB1(self):
        print(self.name, 'OPR')
        self.Open_Raise

    @property
    def OPR_Call(self):
        OPRs = [self.Button_Call, self.SB_Call, self.BB_Call,
                self.UTG_Call, self.MP_Call, self.Cut_Off_Call]
        return OPRs[self.position]

    @property
    def Open_Raise(self):
        OPRs = [self.Button_Raise, self.SB_Raise, self.BB_Raise,
                self.UTG_Raise, self.MP_Raise, self.Cut_Off_Raise]
        return OPRs[self.position]

    @property
    def UTG_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 11:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.connectors(12):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def MP_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 11:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Cut_Off_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 9:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 10 and self.hand[1][0] == 8:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.connectors(7):
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Button_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 8:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.raising(self, 3*self.game.BB)
        elif self.connectors(4):
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def SB_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 10:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[0][0] >= 11:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 11 and self.hand[1][0] == 8:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def BB_Raise(self):
        if self.pocket_pair:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 14:
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.suited:
                self.game.raising(self, 3*self.game.BB)
            elif self.hand[1][0] >= 8:
                self.game.raising(self, 3*self.game.BB)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.raising(self, 3*self.game.BB)
        elif self.connectors(4):
            self.game.raising(self, 3*self.game.BB)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.raising(self, 3*self.game.BB)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def UTG_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            if self.suited:
                self.game.calling(self)
            elif self.hand[1][0] >= 11:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.connectors(12):
            self.game.calling(self)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def MP_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 10:
            self.game.calling(self)
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 11:
            self.game.calling(self)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Cut_Off_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.suited:
                self.game.calling(self)
            elif self.hand[1][0] >= 9:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            self.game.calling(self)
        elif self.hand[0][0] == 10 and self.hand[1][0] == 8:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 6 and self.hand[1][0] == 5:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.connectors(7):
            self.game.calling(self)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Button_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.hand[0][0] == 14:
            self.game.calling(self)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.suited:
                self.game.calling(self)
            elif self.hand[1][0] >= 8:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.calling(self)
        elif self.connectors(4):
            self.game.calling(self)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.calling(self)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def SB_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 6:
            if self.suited:
                self.game.calling(self)
            elif self.hand[1][0] >= 10:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] >= 10 and self.hand[1][0] >= 9:
            if self.suited:
                self.game.calling(self)
            elif self.hand[0][0] >= 11:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 11 and self.hand[1][0] == 8:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 7 and self.hand[1][0] == 6:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 8 and self.hand[1][0] == 7:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 9 and self.hand[1][0] == 8:
            if self.suited:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def BB_Call(self):
        if self.pocket_pair:
            self.game.calling(self)
        elif self.hand[0][0] == 14:
            self.game.calling(self)
        elif self.hand[0][0] >= 11 and self.hand[1][0] >= 7:
            if self.suited:
                self.game.calling(self)
            elif self.hand[1][0] >= 8:
                self.game.calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 10 and self.hand[1][0] >= 8:
            self.game.calling(self)
        elif self.connectors(4):
            self.game.calling(self)
        elif self.hand[0][0] == 9 and self.hand[1][0] >= 7:
            self.game.calling(self)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Three_Bet_Raise(self):
        if self.pocket_pair_higher(7):
            self.game.re_raising(self, 10*self.game.BB)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.suited:
                self.game.re_raising(self, 10*self.game.BB)
            elif self.hand[1][0] >= 12:
                self.game.re_raising(self, 10*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.suited:
                self.game.re_raising(self, 10*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Three_Bet_Call(self):
        if self.pocket_pair_higher(7):
            self.game.re_calling(self)
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.suited:
                self.game.re_calling(self)
            elif self.hand[1][0] >= 12:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.suited:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Four_Bet_Raise(self):
        if self.pocket_pair_higher(11):
            self.game.re_raising(self, 25*self.game.BB)
        elif self.connectors(13):
            self.game.re_raising(self, 25*self.game.BB)
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Four_Bet_Call(self):
        if self.pocket_pair_higher(10):
            self.game.re_calling(self)
        elif self.hand[0][0] == 14 and self.lower(12):
            if self.suited or self.lower(13):
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Five_Bet_Raise(self):
        if self.pocket_pair_higher(12):
            self.game.re_raising(self, 50*self.game.BB)
        elif self.suited_connectors(13):
            self.game.re_raising(self, 50*self.game.BB)
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Five_Bet_Call(self):
        if self.pocket_pair_higher(13):
            self.game.re_calling(self)
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Six_Bet_Raise(self):
        if self.pocket_pair_higher(14):
            self.game.re_raising(self, 100*self.game.BB)
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Six_Bet_Call(self):
        if self.pocket_pair_higher(14):
            self.game.re_calling(self)
        else:
            self.folding
            print(self.name, 'Fold')