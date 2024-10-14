# tourneyreportline.py
# 1/21/2020
# Used to hold the info for each line in the Tourney Report for each week.
# this is essentially a struct
class TourneyReportLine:
    def __init__(self, pid, accno, clubno, gpts, gwon, sprd, taken, cash = 0):
        self.pid = pid
        self.accno = accno
        self.clubno = clubno
        self.gpts = gpts
        self.gwon = gwon
        self.sprd = sprd
        self.natpts = natpts if self.gpts > 11 else self.natpts = 0
        self.cash = 0
        self.taken = taken
        self.given