#!/usr/bin/python
#AI for RPSLW game.  Methods implimented include:

#0: constant Spock: always throws spock
#1: random: picks a purely random throw
#2: weighted random: weights each choice based on previous history, but still random
#3: average (MAP): checks the average move of the player, and beats it
#4: Bayes Average: combines the average move that beats a player, and uses it
#5: N rotation: determines the average rotation of the player, and counters it
#6: pattern detection: looks in the history for the longest string of the pattern detected, and attempts to beat the next move
#7: Bayes pattern detection: weights multiple patterns found and computes the best move
#8: category player: determines what category of person you are, and uses algorithms 1-7 to beat you

import random, operator, itertools

class Moves:
    SCISSORS = "S"
    ROCK = "R"
    PAPER = "P"
    LIZARD = "L"
    SPOCK = "W"

    combinations = [''.join(i) for i in itertools.product(['R', 'P', 'S', 'L', 'S'], repeat = 3)]

    @staticmethod
    def getAllMoves():
        return [Moves.SCISSORS, Moves.ROCK, Moves.PAPER, Moves.LIZARD, Moves.SPOCK]

    @staticmethod
    def parseMove(inputString):
        lowerInputString = inputString.lower()

        if lowerInputString == 's' or 'sci' in lowerInputString:
            return Moves.SCISSORS
        elif lowerInputString == 'r' or 'roc' in lowerInputString:
            return Moves.ROCK
        elif lowerInputString == 'p' or 'pap' in lowerInputString:
            return Moves.PAPER
        elif lowerInputString == 'l' or 'liz' in lowerInputString:
            return Moves.LIZARD
        elif lowerInputString == 'w' or 'spo' in lowerInputString:
            return Moves.SPOCK

        raise Exception("Unrecognized move string was provided.")

    @staticmethod
    def compare(move1, move2):
        """
        Returns 1 if move1 beats move2
        Returns 0 if move1 is equal to move2 (tie)
        Returns -1 if move2 beats move1
        """

        if move1 == Moves.ROCK:
            if move2 == Moves.LIZARD or move2 == Moves.SCISSORS:
                return 1
            elif move2 == Moves.PAPER or move2 == Moves.SPOCK:
                return -1
            else:
                return 0
        elif move1 == Moves.PAPER:
            if move2 == Moves.ROCK or move2 == Moves.SPOCK:
                return 1
            elif move2 == Moves.SCISSORS or move2 == Moves.LIZARD:
                return -1
            else:
                return 0
        elif move1 == Moves.SCISSORS:
            if move2 == Moves.PAPER or move2 == Moves.LIZARD:
                return 1
            elif move2 == Moves.ROCK or move2 == Moves.SPOCK:
                return -1
            else:
                return 0
        elif move1 == Moves.LIZARD:
            if move2 == Moves.SPOCK or move2 == Moves.PAPER:
                return 1
            elif move2 == Moves.SCISSORS or move2 == Moves.ROCK:
                return -1
            else:
                return 0
        else: #Moves.SPOCK
            if move2 == Moves.ROCK or move2 == Moves.SCISSORS:
                return 1
            elif move2 == Moves.PAPER or move2 == Moves.LIZARD:
                return -1
            else:
                return 0

    @staticmethod
    def getRandomMove():
        return random.choice(Moves.getAllMoves())

    @staticmethod
    def getMovesThatCounter(move):
        counterMoves = []

        if move == Moves.ROCK:
            counterMoves.append(Moves.PAPER)
            counterMoves.append(Moves.SPOCK)
        elif move == Moves.PAPER:
            counterMoves.append(Moves.SCISSORS)
            counterMoves.append(Moves.LIZARD)
        elif move == Moves.SCISSORS:
            counterMoves.append(Moves.ROCK)
            counterMoves.append(Moves.SPOCK)
        elif move == Moves.LIZARD:
            counterMoves.append(Moves.SCISSORS)
            counterMoves.append(Moves.ROCK)
        else:
            counterMoves.append(Moves.PAPER)
            counterMoves.append(Moves.LIZARD)

        return counterMoves

class PlayerFactory:
    @staticmethod
    def initPlayer(playerNum):
        if (playerNum == 0):
            return Player0()
        elif (playerNum == 1):
            return Player1()
        elif (playerNum == 2):
            return Player2()
        elif (playerNum == 3):
            return Player3()
        elif (playerNum == 4):
            return Player4()
        elif (playerNum == 5):
            return Player5()
        elif (playerNum == 6):
            return Player6()
        elif (playerNum == 7):
            return Player7()
        elif (playerNum == 8):
            return Player8()
        else:
            return None

class Player:
    def getPlayerName(self):
        return "General Player"
        
    # Picks a sample from the population with
    def weighted_choice(self, moves):
        total = sum(weight for move, weight in moves.iteritems())
        r = random.uniform(0, total)
        upto = 0

        for move, weight in moves.iteritems():
            if upto + weight >= r:
                return move

            upto += weight

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return "Rock"

class Player0(Player):
    def getPlayerName(self):
        return "Constant Player"
        
    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return Moves.SPOCK

class Player1(Player):
    def getPlayerName(self):
        return "Random Player"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return Moves.getRandomMove()

class Player2(Player):
    def getPlayerName(self):
        return "Weighted Random"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        moveDict = {}
        for move in Moves.getAllMoves():
            moveDict[move] = 0

        for i in range(scoreHistory):
            if scoreHistory[i] == maximization:
                moveDict[myHistory[move]] += 1
            elif scoreHistory[i] == 0:
                moveDict[myHistory[move]] += 0.5

        return self.weighted_choice(moveDict)

class Player3(Player):
    def __init__(self):
        self.opponentPlayer = Player1()

    def getPlayerName(self):
        return "MLE/MAP"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return random.choice(Moves.getMovesThatCounter(self.opponentPlayer.getNextMove(theirHistory, myHistory, scoreHistory, -maximization)))

class Player4(Player):
    def getPlayerName(self):
        return "Bayes Average"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        moveDict = {}

        for move in Moves.getAllMoves():
            moveDict[move] = 0

        for move_human_opponent_outcome in theirHistory:
            move = move_human_opponent_outcome[0]
            moveDict[move] += 1

        rockUtility = 0.1*moveDict[Moves.ROCK]-1*moveDict[Moves.PAPER]+1*moveDict[Moves.SCISSORS]+1*moveDict[Moves.LIZARD]-1*moveDict[Moves.SPOCK]
        paperUtility = 1.0*moveDict[Moves.ROCK]+0.1*moveDict[Moves.PAPER]-1*moveDict[Moves.SCISSORS]-1*moveDict[Moves.LIZARD]+1*moveDict[Moves.SPOCK]
        scissorsUtility = -1*moveDict[Moves.ROCK]+1*moveDict[Moves.PAPER]+.1*moveDict[Moves.SCISSORS]+1*moveDict[Moves.LIZARD]-1*moveDict[Moves.SPOCK]
        lizardUtility = -1*moveDict[Moves.ROCK]+1*moveDict[Moves.PAPER]-1*moveDict[Moves.SCISSORS]+.1*moveDict[Moves.LIZARD]+1*moveDict[Moves.SPOCK]
        spockUtility = 1.0*moveDict[Moves.ROCK]-1*moveDict[Moves.PAPER]+1*moveDict[Moves.SCISSORS]-1*moveDict[Moves.LIZARD]+.1*moveDict[Moves.SPOCK]

        if rockUtility is max(rockUtility,paperUtility,scissorsUtility,lizardUtility,spockUtility):
            return Moves.ROCK
        elif paperUtility is max(rockUtility,paperUtility,scissorsUtility,lizardUtility,spockUtility):
            return Moves.PAPER
        elif scissorsUtility is max(rockUtility,paperUtility,scissorsUtility,lizardUtility,spockUtility):
            return Moves.SCISSORS
        elif lizardUtility is max(rockUtility,paperUtility,scissorsUtility,lizardUtility,spockUtility):
            return Moves.LIZARD
        elif spockUtility is max(rockUtility,paperUtility,scissorsUtility,lizardUtility,spockUtility):
            return Moves.SPOCK

class Player5(Player):
    def getPlayerName(self):
        return "N Rotation w/l"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return
    
class Player6(Player):
    def __init__(self):
        combine = {Moves.combinations[i] : str(i) for i in range(0, len(Moves.combinations))}
        split = {str(i) : Moves.combinations[i] for i in range(0, len(Moves.combinations))}

    def getPlayerName(self):
        return "Pattern Detection"

    def convertHistoriesIntoDna(self, myHistory, theirHistory):
        dna = ""

        if myHistory == "":
            return dna

        for i in range(0, len(myHistory)):
            dna += Moves.combine[myHistory[i]+theirHistory[i]]

        return dna

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        dna = self.convertHistoriesIntoDna(myHistory, theirHistory)

        if dna == "":
            return Moves.getRandomMove()

        result = None

        for patternLength in range(min(5, len(dna)-1), 0, -1):
            pattern = dna[-patternLength:]
            patternIndex = dna.find(pattern, 0, -1)

            if patternIndex != -1:
                nextMoveAfterPattern = dna[patternIndex + patternLength]
                expectedOpponentMove = Moves.split[nextMoveAfterPattern][1]
                result = Moves.getMovesThatCounter(expectedOpponentMove)
                break

        if result is not None:
            result = random.choice(result)
        else:
            result = Moves.getRandomMove()

        return result
    
class Player7(Player6):
    def getPlayerName(self):
        return "Bayes Pattern Detection"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return
    
class Player8(Player):
    def getPlayerName(self):
        return "Best Category"

    def getNextMove(self, myHistory, theirHistory, scoreHistory, maximization):
        return
