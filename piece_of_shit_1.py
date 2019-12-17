import random
import time
import copy
import gomoku
import math

class mlgpro:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """
    def __init__(self, black_=True):
        """Constructor for the player."""
        self.black = black_

    def new_game(self, black_):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_

    def findSpotToExpand(self, nRoot):
        game = gomoku.gomoku_game(19, nRoot.board)
        # print(len(nRoot.valid_moves))
        if not nRoot.valid_moves:
            return nRoot
        if nRoot.valid_moves:
            # print(len(nRoot.valid_moves))
            # move = random.choice(nRoot.valid_moves)
            move = nRoot.valid_moves[0]
            game.move(move)
            nRoot.valid_moves.remove(move)
            # print(len(nRoot.valid_moves))
            color = not nRoot.color
            nChild = Node(game.current_board(), nRoot.valid_moves, color, move, nRoot)
            nRoot.children.append(nChild)
            return nChild
        nChild = nRoot.children[0]
        for child in nRoot.children:
            if child.UCT() > nChild.UCT():
                nChild = child
        return self.findSpotToExpand(nChild)

    def rollout(self, nLeaf):
        # print("rollout")
        me = True
        game = gomoku.gomoku_game(19, nLeaf.board)
        lastMove = copy.deepcopy(nLeaf.last_move)
        validMoves = copy.deepcopy(nLeaf.valid_moves)
        while (lastMove is None or (not game.check_win(lastMove))) and validMoves:
            move = random.choice(validMoves)
            game.move(move)
            validMoves.remove(move)
            # print(len(nLeaf.valid_moves))
            me = not me
            lastMove = move
        if not validMoves:
            return 0.5
        return me
    
    def backupValue(self, n, val):
        opp = False
        while n is not None:
            n.N += 1
            if opp:
                n.Q -= val
            else:
                n.Q += val
            opp = not opp
            n = n.parent



    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        startTime = int(round(time.time() * 1000))
        nRoot = Node(board, valid_moves, self.black, last_move)
        while int(round(time.time() * 1000)) - startTime < max_time_to_move-5:
            nLeaf = self.findSpotToExpand(nRoot)
            val = self.rollout(nLeaf)
            self.backupValue(nLeaf, val)
        # bestChild = nRoot.children[0]
        bestChild = max(nRoot.children, key=lambda c : c.Q)
        # for child in nRoot.children:
        #     if child.UCT() > bestChild.UCT():
        #         bestChild = child
        gomoku.prettyboard(board)
        print('\n')
        return bestChild.last_move

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Youri de Vor 17491751"


class Node:
    def __init__(self, board, valid_moves, color = True, lastmove = (), parent = None):
        self.board = board
        self.valid_moves = valid_moves
        self.children = []
        self.parent = parent
        self.color = color
        self.last_move = lastmove
        self.N = 0
        self.Q = 0

    def UCT(self, constant=0.7):
        left = self.Q / self.N
        right = constant*math.sqrt((2*math.log2(self.parent.N))/(self.N))
        return left + right
