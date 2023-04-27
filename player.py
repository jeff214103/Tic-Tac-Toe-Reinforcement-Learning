from copy import deepcopy
import sys
import os
import numpy as np
import pickle

class Player:
    def __init__(self, name, marker):
        if (not isinstance(name,str)):
            raise TypeError("name must have string type")
        if (not isinstance(marker,str)):
            raise TypeError("marker must have string type")
        if(len(marker) != 1 and (marker.lower() != 'x' or marker.lower() != 'o')):
            raise ValueError("marker must be either 'o' or 'x' ")
        self.name = name
        self.marker = marker.lower()
    
    def getMove(self):
        raise RuntimeError("It is just an abstract class. Please choose either human or computer player")

class HumanPlayer(Player):
    def __init__(self, name, marker):
        super().__init__(name,marker)
    
    def getMove(self, current_board):
        print("Avaialbe Move: {}".format(current_board.getAvailableMove()))
        data = input("Please input (row, col): ")
        row = 0
        col = 0
        if (len(data.split(",")) == 2):
            row, col = data.split(",")
        elif (len(data.split(" ")) == 2):
            row, col = data.split(" ")
        else:
            raise ValueError("Cannot find valid seperator, please either use space or ','")
        return int(row), int(col)

#AI player class reference from https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542
class AIPlayer(Player):
    def __init__(self, name, marker, random_rate=0):
        super().__init__(name,marker)
        self.states = []  # record all positions taken
        self.learning_rate = 0.2
        self.random_rate = random_rate #Only applicable when training
        self.decay_gamma = 0.9
        self.game_dictionary = {}  # State, with the value of that state

        if (os.path.exists(self.marker+'_AI')):
            print(self.marker+"_AI file found")
            self.loadPolicy()
        else:
            print(self.marker+"_AI file not found")
            print("Please perform training before using AI player")
            raise FileNotFoundError(self.marker+"_AI file not found")
    
    def getMove(self, current_board):
        positions = current_board.getAvailableMove()
        print("Avaialbe Move: {}".format(positions))

        # Random Behaviour when for training
        if np.random.uniform(0, 1) <= self.random_rate:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:

            # Choose the max value choice
            max_value = -sys.maxsize - 1
            for pos in positions:
                potential_board = deepcopy(current_board)
                potential_board.place(self, pos)
                potential_board_hash = potential_board.getBoardHash()
                value = 0 if self.game_dictionary.get(potential_board_hash) is None else self.game_dictionary.get(potential_board_hash)
                if value >= max_value:
                    max_value = value
                    action = pos

        next_board = deepcopy(current_board)
        next_board.place(self, action)

        # Add the choosing state to list of state
        self.addState(next_board.getBoardHash())
        print("AI Player choose: {}".format(action))
        return action

    def addState(self, state):
        self.states.append(state)

    # As we take place after finish, the following state will be the max state, therefore max value ignore here
    def feedReward(self, reward):
        for state in reversed(self.states):
            if self.game_dictionary.get(state) is None:
                self.game_dictionary[state] = 0
            self.game_dictionary[state] += self.learning_rate * (self.decay_gamma * reward - self.game_dictionary[state])
            reward = self.game_dictionary[state]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open(self.marker+'_AI', 'wb')
        pickle.dump(self.game_dictionary, fw)
        fw.close()

    def loadPolicy(self):
        fr = open(self.marker+'_AI', 'rb')
        self.game_dictionary = pickle.load(fr)
        fr.close()

    