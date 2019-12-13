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
        if game.check_win(nRoot.last_move):
                return nRoot
        if nRoot.valid_moves:
            move = random.choice(nRoot.valid_moves)
            game.move(move)
            nRoot.valid_moves.remove(move)
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
        me = True
        game = gomoku.gomoku_game(19, nLeaf.board)
        lastMove = nLeaf.last_move
        validMoves = nLeaf.valid_moves
        while not game.check_win(lastMove) and validMoves:
            move = random.choice(validMoves)
            game.move(move)
            validMoves.remove(move)
            me = not me
        if not validMoves:
            return 0.5
        return me
    
    def backupValue(self, n, val):
        while n is not None:
            n.N += 1
            if some bullshit:
                n.Q -= val
            else:
                n.Q += val
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
        while int(round(time.time() * 1000)) - startTime < max_time_to_move-100:
            nLeaf = self.findSpotToExpand(nRoot)
            val = rollout(nLeaf)
            backupValue(nLeaf, val)
        return random.choice(valid_moves)

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
        self.lastmove = lastmove
        self.N = 0
        self.Q = 0

    def UCT(self, constant=1):
        left = self.Q / self.N
        right = constant*math.sqrt((2*math.log2(self.parent.N))/(self.N))
        return left + right
