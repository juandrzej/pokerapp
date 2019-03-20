from playerclass import Player


class Scripting_Player(Player):
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
    def preflop_3bet(self):
        if self.game.raise_amt == self.game.BB*3:
            self.Three_Bet_Raise
        if self.game.raise_amt == self.game.BB*10:
            self.Three_Bet_Call

    @property
    def preflop_4bet(self):
        if self.game.raise_amt == self.game.BB*10:
            self.Four_Bet_Raise
        if self.game.raise_amt == self.game.BB*25:
            self.Four_Bet_Call

    @property
    def preflop_5bet(self):
        if self.game.raise_amt == self.game.BB*25:
            self.Five_Bet_Raise
        if self.game.raise_amt == self.game.BB*60:
            self.Five_Bet_Call

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
