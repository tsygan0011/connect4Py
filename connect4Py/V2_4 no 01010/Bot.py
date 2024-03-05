import random
#fix bot so that it will not f it's win over by dropping block directly below its winning block
#lvl 3 tend to atk before defending

# function prototypes
def getVictCond(p1, p2):
    # check how close player is to vict
    return numofLink, coltoWin

def getVictPath(p1, p2):
    # returns list of (direction to win, number of pieces already in place, position of mssing pieces)
    # paths should be sorted by shortest to win
    # Number of moves needed should also be given
    dir == "right"
    numAlrPiece = 2
    missingPiece1 = "11"
    missingPiece2 = "21"
    return [(dir, numAlrPiece, [missingPiece1, missingPiece2]),()]

#bot class
class c4_bot:
    def __init__(self, level, p1, p2, player, colheights):
        self.level = level
        self.p1 = p1
        self.p2 = p2
        self.player = player
        self.colheights = colheights

        self.bot3winconlist = []
        self.bot2winconlist = []
        #Dictionary for function callback
        self.moveDict = {
            0: self.move_lvl0,
            1: self.move_lvl1,
            2: self.move_lvl2,
            3: self.move_lvl3,
            4: self.move_lvl4
        }

    def make_move(self):
        # call the appropiate move level
        #make_move()
        return self.moveDict[self.level]() - 1

    def move_lvl0(self):
        # return a random col for move
        return random.randrange(1,8)

    def move_lvl1(self):
        # blocks the opponent only if he is winning next turn else random move
        ret = random.randrange(1,8)
        while self.colheights[ret]>=6:
            ret = random.randrange(1, 8)

        if self.bot3winconlist:
            #stop opponent from winning
            print("the blocking piece required is " + str(self.bot3winconlist))
            print(self.colheights)
            for i in self.bot3winconlist:
                # print("considering " + i)
                if int(i[1]) == self.colheights[int(i[0])] + 1:
                    # only try to block if next it will stack onto the correct location
                    # print("accepted " + i)
                    ret = int(i[0])
                    break
                elif int(i[1]) == self.colheights[int(i[0])] + 2:
                    # avoid drop a block directly below a winning tile
                    l = [1,2,3,4,5,6,7]
                    while len(l)>0:
                        ret = l[random.randrange(len(l))]
                        if ret == int(i[0]) or self.colheights[ret]>=6:
                            l.remove(ret)
                        else:
                            break
                    # print(i + " rejected, just below " + i)
                # else:
                    # print(i + " rejected, col height is " + str(self.colheights[int(i[0])] + 1))

            # print("the number is shuffles")
        # print("returning " + str(ret) + " and " + str(self.colheights[ret]))
        return ret

    def move_lvl2(self):
        # blocks the opponent only if he is winning next turn else try to win
        ret = random.randrange(1,8)
        while self.colheights[ret] >= 6:
            ret = random.randrange(1, 8)

        temp3 = self.bot3winconlist.copy()

        # temp2 = self.bot2winconlist.copy() #Not in use
        self.nextnum()
        for i in self.bot3winconlist:
            # winning is possible
            if int(i[1]) == self.colheights[int(i[0])] + 1:
                # only try to win if next it will stack onto the correct location
                return int(i[0])
        for i in temp3:
            if int(i[1]) == self.colheights[int(i[0])] + 1:
                # only try to block if next it will stack onto the correct location
                return int(i[0])
            elif int(i[1]) == self.colheights[int(i[0])] + 2:
                # avoid drop a block directly below a winning tile
                l = [1, 2, 3, 4, 5, 6, 7]
                while len(l) > 0:
                    ret = l[random.randrange(len(l))]
                    if ret == int(i[0]) or self.colheights[ret] >= 6:
                        l.remove(ret)
                    else:
                        return ret

        for ii in self.bot2winconlist:
            for i in ii:
                # build up to win
                if int(i[1]) == self.colheights[int(i[0])] + 1:
                    #put in to complete 3 blocks in a row
                    return int(i[0])

        return ret

    def move_lvl3(self):
        # Will start prevent traps by stopping blocking at 2 chains
        ret = random.randrange(1,8)
        blacklist=[]
        while self.colheights[ret] >= 6:
            ret = random.randrange(1, 8)

        temp3 = self.bot3winconlist.copy()
        temp2 = self.bot2winconlist.copy()
        self.nextnum()

        print(self.bot3winconlist)
        for i in self.bot3winconlist:
            # winning is possible
            if int(i[1]) == self.colheights[int(i[0])] + 1:
                # only try to win if next it will stack onto the correct location
                return int(i[0])
        print(temp3)
        for i in temp3:
            if int(i[1]) == self.colheights[int(i[0])] + 1:
                # only try to block if next it will stack onto the correct location
                return int(i[0])
            elif int(i[1]) == self.colheights[int(i[0])] + 2:
                # avoid drop a block directly below a winning tile
                blacklist.append(int(i[0]))
                while len(blacklist)<7:
                    ret = random.randrange(1,8)
                    if ret in blacklist or self.colheights[ret] >= 6:
                        if ret not in blacklist:
                            blacklist.append(ret)
                        # If there is no other choice, just drop below winning piece
                        if len(blacklist) == 7:
                            print("There was no other choice int")
                            return int(i[0])
                    else:
                        break
        print(str(temp2) + " is blocking " + str(blacklist) + " Is blacklist")
        for ii in temp2:
            for i in ii:
                if int(i[1]) == self.colheights[int(i[0])] + 1 and int(i[0]) not in blacklist:
                    # only try to block if next it will stack onto the correct location
                    return int(i[0])
        print(self.bot2winconlist)
        for ii in self.bot2winconlist:
            for i in ii:
                # build up to win
                if int(i[1]) == self.colheights[int(i[0])] + 1 and int(i[0]) not in blacklist:
                    #put in to complete 3 blocks in a row
                    return int(i[0])
        print("all else has failed, returning " + str(ret))
        return ret

    def move_lvl4(self):
        # Makes use of weights to decide on next move
        weights = {
            "1":0,
            "2":0,
            "3":0,
            "4":0,
            "5":0,
            "6":0,
            "7":0
        }
        for i in range(1,8):
            if self.colheights[i]>=6:
                weights[str(i)] -= 1000
        for i in self.p2:
            toleft=3
            toright=3
            if i[0]!="1":
                toleft = int(i[1]) - self.colheights[int(i[0])-1]
            if i[0]!="7":
                toright = int(i[1]) - self.colheights[int(i[0])+1]
            if abs(toleft)<=1 and int(i[0]) >=4:
                weights[str(int(i[0])-1)] +=1
            if abs(toright)<=1 and int(i[0]) <=4:
                weights[str(int(i[0])+1)] +=1

        temp3 = self.bot3winconlist.copy()
        temp2 = self.bot2winconlist.copy()
        self.nextnum()

        print(self.bot3winconlist)
        for i in self.bot3winconlist:
            # winning is possible
            if int(i[1]) == self.colheights[int(i[0])] + 1:
                # only try to win if next it will stack onto the correct location
                weights[i[0]] += 1000
            elif int(i[1]) == self.colheights[int(i[0])] + 2:
                weights[i[0]] -= 100
        print(temp3)
        for i in temp3:
            if int(i[1]) == self.colheights[int(i[0])] + 1:
                # only try to block if next it will stack onto the correct location
                weights[i[0]] += 400
            elif int(i[1]) == self.colheights[int(i[0])] + 2:
                # avoid drop a block directly below a winning tile
                weights[i[0]] -= 200
        print(temp2)
        for ii in temp2:
            for i in ii:
                # be more likely to block if iblock
                # the less blocks needed to stack, the higher the weight
                # directly below is no good
                temp = int(i[1]) - self.colheights[int(i[0])] # 1 if placement there, 2 if directly below
                if temp == 1:
                    weights[i[0]] += 5
                elif temp == 2:
                    weights[i[0]] -= 4
        print(self.bot2winconlist)
        for ii in self.bot2winconlist:
            for i in ii:
                # build up to win
                temp = int(i[1]) - self.colheights[int(i[0])] # 1 if placement there, 2 if directly below
                if temp == 2:
                    weights[i[0]] -= 5
                else:
                    weights[i[0]] += 5 - (int(i[1]) - self.colheights[int(i[0])])

        print(weights)
        temp = -2000
        l = []
        for i in range(1,8):
            if weights[str(i)]>temp:
                l.clear()
                temp = weights[str(i)]
                l.append(i)
            elif weights[str(i)]==temp:
                l.append(i)
        return l[random.randrange(len(l))]

    def wincon1110(self, player, nextpiece, horizontal, vertical):  # bot check if 3 in a row have win condition
        if player == 1:
            oppopieces = self.p2
        elif player == 2:
            oppopieces = self.p1

        # check for 0 1 1 1 0 win condition
        if nextpiece not in oppopieces + self.bot3winconlist:
            self.bot3winconlist.append(nextpiece)

        nextpiece = '%s%s' % (int(nextpiece[0]) - (int(horizontal) * 4), int(nextpiece[1]) - (int(vertical) * 4))
        if nextpiece not in oppopieces + self.bot3winconlist and 0 < int(nextpiece[0]) < 8 and 0 < int(nextpiece[1]) < 7:
            self.bot3winconlist.append(nextpiece)

    def wincon1101_1100(self, player, nextpiece, horizontal, vertical):  # bot check if 2 in a row has win condition
        if player == 1:
            playerpieces = self.p1
            oppopieces = self.p2
        elif player == 2:
            playerpieces = self.p2
            oppopieces = self.p1

        # check for 1 1 0 1 win condition
        slot1 = '%s%s' % (int(nextpiece[0]) + int(horizontal), int(nextpiece[1]) + int(vertical))
        if nextpiece not in oppopieces + self.bot3winconlist and slot1 in playerpieces:
            self.bot3winconlist.append(nextpiece)

        slot2 = '%s%s' % (int(nextpiece[0]) - (int(horizontal) * 3), int(nextpiece[1]) - (int(vertical) * 3))
        slot3 = '%s%s' % (int(nextpiece[0]) - (int(horizontal) * 4), int(nextpiece[1]) - (int(vertical) * 4))
        if slot2 not in oppopieces + self.bot3winconlist and slot3 in playerpieces:
            self.bot3winconlist.append(slot2)

        # check for 1 1 0 0 win condition
        temp = [nextpiece, slot1]
        if nextpiece not in playerpieces + oppopieces and slot1 not in playerpieces + oppopieces and temp not in self.bot2winconlist:
            if 1 < int(nextpiece[0]) < 7 and 0 < int(nextpiece[1]) < 6:
                self.bot2winconlist.append(temp)

        temp = [slot2, slot3]
        if slot2 not in playerpieces + oppopieces and slot3 not in playerpieces + oppopieces and temp not in self.bot2winconlist:
            if 1 < int(slot2[0]) < 7 and 0 < int(slot2[1]) < 6:
                self.bot2winconlist.append(temp)

        # check for 0 1 1 0 win condition
        temp = [nextpiece, slot2]
        if nextpiece not in playerpieces + oppopieces and slot2 not in playerpieces + oppopieces and temp not in self.bot2winconlist:
            temp2 = [slot2, nextpiece]
            if int(vertical) == 0 and 0 < int(nextpiece[0]) < 8 and 0 < int(slot2[0]) < 8 and temp2 not in self.bot2winconlist:
                self.bot2winconlist.append(temp)

    def wincon1011_01010(self, player, nextpiece, horizontal, vertical):  # bot check for trap and diagonal wincon
        if player == 1:
            playerpieces = self.p1
            oppopieces = self.p2
        elif player == 2:
            playerpieces = self.p2
            oppopieces = self.p1

        actualpiece = '%s%s' % (int(nextpiece[0]) - int(horizontal), int(nextpiece[1]) - int(vertical))
        slot1 = '%s%s' % (int(nextpiece[0]) + int(horizontal), int(nextpiece[1]) + int(vertical))
        slot2 = '%s%s' % (int(nextpiece[0]) + (int(horizontal) * 2), int(nextpiece[1]) + (int(vertical) * 2))
        slot3 = '%s%s' % (int(nextpiece[0]) - (int(horizontal) * 2), int(nextpiece[1]) - (int(vertical) * 2))

        if int(actualpiece[1]) > 1 or (2 < int(actualpiece[0]) < 6 and int(actualpiece[1]) == 1):  # check for diagonal
            if slot1 in playerpieces and slot2 in playerpieces and nextpiece not in playerpieces + oppopieces and nextpiece not in self.bot3winconlist:
                self.bot3winconlist.append(nextpiece)

    def wincon(self, pieces, nextpiece, horizontal, vertical, player):
        # check how close the bot is to winning
        for i in range(1, 4):
            nextpiece = '%s%s' % (int(nextpiece[0]) + int(horizontal), int(nextpiece[1]) + int(vertical))
            if nextpiece not in pieces:
                if i == 3:  # check for bot wincon with 3 in a row
                    self.wincon1110(player, nextpiece, horizontal, vertical)
                elif i == 2:  # check for bot wincon with 2 in a row
                    self.wincon1101_1100(player, nextpiece, horizontal, vertical)
                elif i == 1:  # check for traps
                    self.wincon1011_01010(player, nextpiece, horizontal, vertical)
                break

    def nextnum(self):
        pieces = []
        msg = ''
        self.bot3winconlist.clear()
        self.bot2winconlist.clear()

        if self.player == 1:
            pieces = self.p1
        elif self.player == 2:
            pieces = self.p2

        for x in pieces:
            if int(x[0]) > 3:  # checks to the left
                self.wincon(pieces, x, '-1', '0', self.player)

            if int(x[0]) > 3 and int(x[1]) < 4:  # checks diagonally left
                self.wincon(pieces, x, '-1', '1', self.player)

            if int(x[0]) < 5:  # checks to the right
                self.wincon(pieces, x, '1', '0', self.player)

            if int(x[0]) < 5 and int(x[1]) < 4:  # checks diagonally right
                self.wincon(pieces, x, '1', '1', self.player)

            if int(x[1]) < 4:  # checks upwards
                self.wincon(pieces, x, '0', '1', self.player)
