import gomoku
import random_player
import time
import piece_of_shit_1 as ps

class competition:
    """This class runs the competition between the submitted players.
    A player needs to have the new_game(black) and move(board, prev_move, valid_moves_list)
    methods implemented. Players are registered one by one using the register_player method.
    The competition is started using the play_competition method."""
    def __init__(self, bsize_=19):
        """Initialises the competition. The board size (default 19) for the entire competition can be set here."""
        self.players = []
        self.results = []
        self.bsize = bsize_

    def register_player(self, player_):
        """This method registers an AI player that the students have implemented.
        This player needs to be in a separate file."""
        self.players.append(player_)

    def play_competition(self, maxtime_per_move=100, tolerance=0.05):
        """This method runs the actual competition between the registered players.
        Each player plays each other player twice: once with black and once with white."""
        self.results = []
        mtime = maxtime_per_move * (1.0+tolerance) * 1000000 #operational maxtime in nanoseconds
        for i in range(len(self.players)):
            self.results.append([0.0]*len(self.players)) #set the results matrix to all zeroes
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                if (i==j):
                    continue #players do not play themselves
                self.players[i].new_game(True) #player i is black
                self.players[j].new_game(False) # player j is white
                game = gomoku.gomoku_game(bsize_=self.bsize) #initialise the game
                over = False
                while not over:
                    if game.ply%2==1: #black to move
                        current_player = self.players[i]
                        pid = i
                        pid_other = j
                    else: #white to move
                        current_player = self.players[j]
                        pid = j
                        pid_other = i
                    start_time = time.time_ns()
                    move = current_player.move(game.current_board(), game.previous_move, game.valid_moves(), max_time_to_move=maxtime_per_move)
                    stop_time = time.time_ns()
                    #print(str((stop_time-start_time)/1000000)+"/"+str(maxtime_per_move*(1+tolerance)))
                    ok, win = game.move(move) #perform the move, and obtain whether the move was valid (ok) and whether the move results in a win
                    if  (stop_time-start_time) > mtime:
                        #player who made the illegal move should be disqualified. This needs to be done manually.
                        print("disqualified for exceeding maximum time per move: player "+str(pid))
                    if not ok:
                        #player who made the illegal move should be disqualified. This needs to be done manually.
                        print("disqualified for illegal move: player "+str(pid))
                        print("on board: ")
                        gomoku.prettyboard(game.current_board())
                        print("trying to play: ("+str(move[0])+","+str(move[1])+")")
                        if game.ply % 2 == 1:
                            print("as black")
                        else:
                            print("as white")
                    if win:
                        over = True
                        self.results[pid][pid_other] += 1
                    elif len(game.valid_moves()) == 0:
                        #if there are no more valid moves, the board is full and it's a draw
                        over = True
                        self.results[pid][pid_other] += 0.5
                        self.results[pid_other][pid] += 0.5

    def print_scores(self):
        """This method prints the results of the competition to sysout"""
        i = 0
        for line in self.results:
            for res in line:
                print(str(res), end=" ")
            print("["+self.players[i].id()+", "+str(sum(line))+"]")
            i+=1


##Now follows the main script for running the competition
# At present the competition consists of just three random dummy players playing each other
# When the students submit a player file, they should be entered one by one.
game = gomoku.gomoku_game()
player = random_player.random_dummy_player()
player2 = ps.mlgpro()
player3 = ps.mlgpro()
player4 = ps.mlgpro()
player5 = ps.mlgpro()
player6 = ps.mlgpro()
player7 = ps.mlgpro()
player8 = ps.mlgpro()
player9 = ps.mlgpro()
comp = competition()
comp.register_player(player)
comp.register_player(player2)
comp.register_player(player3)
comp.register_player(player4)
comp.register_player(player5)
comp.register_player(player6)
comp.register_player(player7)
comp.register_player(player8)
comp.register_player(player9)
comp.play_competition()
comp.print_scores()