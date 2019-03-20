from playerclass import Player


class Scripting_Player(Player):
    def __init__(self, name, hand, position, game, stack):
        super().__init__(name, hand, position, game, stack)
        self.in_pot = 0

    @property
    def preflop(self):
        if self.game.raise_amt == self.game.BB*60:
            print(self.name, '5betC')
            self.Five_Bet_Call

        elif self.game.raise_amt == self.game.BB*25:
            print(self.name, '4betC')
            self.Four_Bet_Call
            if self.action:
                print(self.name, '5betR')
                self.Five_Bet_Raise

        elif self.game.raise_amt == self.game.BB*10:
            print(self.name, '3betC')
            self.Three_Bet_Call
            if self.action:
                print(self.name, '4betR')
                self.Four_Bet_Raise

        elif self.game.raise_amt == self.game.BB*3:
            print(self.name, 'Call')
            if self.position == 3:
                self.UTG_Call
            elif self.position == 4:
                self.MP_Call
            elif self.position == 5:
                self.Cut_Off_Call
            elif self.position == 0:
                self.Button_Call
            elif self.position == 1:
                self.Small_Blind_Call
            elif self.position == 2:
                self.Big_Blind_Call
            if self.action:
                print(self.name, '3betR')
                self.Three_Bet_Raise

        elif self.game.raise_amt == self.game.BB:
            print(self.name, 'OPR')
            if self.position == 3:
                self.UTG_Raise
            elif self.position == 4:
                self.MP_Raise
            elif self.position == 5:
                self.Cut_Off_Raise
            elif self.position == 0:
                self.Button_Raise
            elif self.position == 1:
                self.Small_Blind_Raise
            elif self.position == 2:
                self.Big_Blind_Raise

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

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
            print(self.name, 'Fold')

    @property
    def Three_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 7:
                self.game.re_raising(self, 10*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_raising(self, 10*self.game.BB)
            elif self.hand[1][0] >= 12:
                self.game.re_raising(self, 10*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_raising(self, 10*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Three_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 7:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 11:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_calling(self)
            elif self.hand[1][0] >= 12:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 13 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Four_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 11:
                self.game.re_raising(self, 25*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 13:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_raising(self, 25*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Four_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 10:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 12:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_calling(self)
            elif self.hand[1][0] >= 13:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')

    @property
    def Five_Bet_Raise(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 13:
                self.game.re_raising(self, 60*self.game.BB)
            else:
                self.game.checking
                print(self.name, 'Check')
        else:
            self.game.checking
            print(self.name, 'Check')

    @property
    def Five_Bet_Call(self):
        if self.hand[0][0] == self.hand[1][0]:
            if self.hand[0][0] >= 13:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        elif self.hand[0][0] == 14 and self.hand[1][0] >= 13:
            if self.hand[0][1] == self.hand[1][1]:
                self.game.re_calling(self)
            else:
                self.folding
                print(self.name, 'Fold')
        else:
            self.folding
            print(self.name, 'Fold')
