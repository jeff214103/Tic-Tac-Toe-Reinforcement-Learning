from numpy.lib.arraysetops import isin
from argparse import ArgumentParser
from game_board import Board
from player import HumanPlayer
from player import AIPlayer
import time
import sys
import os
from tqdm import tqdm

class TicTacToe:
    def __init__(self, player):
        self.board = Board()
        if (len(player) != 2):
            raise ValueError("There can only be two player in the game")
        if (player[0].marker == player[1].marker):
            raise RuntimeError("Two player contains the same mark")
        self.player = player
    
    def start(self):
        turn = 0
        self.board.reset()
        while self.board.hasWinner() == -1:
            print("================")
            self.board.printBoard()
            print("Player "+self.player[turn].name+" Turn (Marker: "+self.player[turn].marker+") ")

            isValidInput = False
            while (isValidInput == False):
                try:
                    pos = self.player[turn].getMove(self.board)
                    self.board.place(self.player[turn], pos)
                    isValidInput = True
                except Exception as e:
                    print("Invalid Input! Please try again")
                    print("Details: "+str(e))
            turn = (turn + 1) % 2
        
        if (self.board.hasWinner() > 0):
            winner = (turn + 1) % 2
            print("================")
            self.board.printBoard()
            print("================")
            print("Player "+self.player[winner].name+" Win! (Marker: "+self.player[winner].marker+") ")

            #Return which player win, 0 = player 1, 1 = player 2
            return winner
        else:
            print("================")
            self.board.printBoard()
            print("================")
            print("Tie Game! ")
            #Return no winner
            return -1

    
    def trainAI(self, round):
        if (not isinstance(round, int)):
            raise ValueError("Round must have int type")
        if (all (type(player) != AIPlayer for player in self.player)):
            raise RuntimeError("train AI must have all player to be AIPlayer class")
        try:
            for i in tqdm(range(round)):
                sys.stdout = open(os.devnull, 'w')
                print("======= Round {} =======".format(i))
                winner = self.start()
                if (winner == -1):
                    print("Tie Reward")
                    self.player[0].feedReward(0.5)
                    self.player[1].feedReward(0.5)
                else:
                    print("Winner {} Reward".format(winner))
                    for i in range(2):
                        if (i == winner):
                            self.player[i].feedReward(1)
                        else:
                            self.player[i].feedReward(0)
                        self.player[i].reset()
                sys.stdout = sys.__stdout__

            self.player[0].savePolicy()
            self.player[1].savePolicy()
        except KeyboardInterrupt:
            print("Trying to save player policy before end..")
            self.player[0].savePolicy()
            self.player[1].savePolicy()


if (__name__ == "__main__"):
    parser = ArgumentParser(description="Tic Tac Toe")

    subparsers = parser.add_subparsers(dest="mode", required=True, help="sub commands")
    train_parser = subparsers.add_parser("train", help="AI Training")
    play_parser = subparsers.add_parser("play", help="Play a game")

    train_parser.add_argument("--iteration",type=int, help="Numbers of epoch would like to train", dest="epoch", default=50000)

    play_parser.add_argument("--o", type=int, help="o player (0: AI/1: player)", dest="o_player", required=True)
    play_parser.add_argument("--x", type=int, help="x player (0: AI/1: player)", dest="x_player", required=True)

    opt = parser.parse_args()

    if(opt.mode == "train"):
        players = [AIPlayer('com_1','o',0.2),AIPlayer('com_2','x',0.2)]
        game = TicTacToe(players)
        game.trainAI(opt.epoch)

    elif(opt.mode == "play"):
        players = []
        if (opt.o_player == 0):
            players.append(AIPlayer('com_1','o'))
        elif (opt.o_player == 1):
            players.append(HumanPlayer('1','o'))
        if (opt.x_player == 0):
            players.append(AIPlayer('com_2','x'))
        elif (opt.x_player == 1):
            players.append(HumanPlayer('2','x'))
        TicTacToe(players).start()
