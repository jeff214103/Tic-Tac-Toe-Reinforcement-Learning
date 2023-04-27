from player import Player
import numpy as np

class Board:
    def __init__(self):
        self.board = np.array([[None,None,None],[None,None,None],[None,None,None]])
        self.reset()

    def reset(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = None

    def __isValidMove(self,pos):
        if (not isinstance(pos, tuple) and len(pos) != 2):
            raise TypeError("Position must be a tuple of (row, col)")
        if ((pos[0] <= 0 and pos[0] > 3) or (pos[1] <= 0 and pos[1] > 3)):
            raise ValueError("Row and Column must be in range of 1 to 3")
        
        if (self.board[pos[0]-1][pos[1]-1] != None):
            return False
        else:
            return True

    def getAvailableMove(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] == None):
                    positions.append((i+1,j+1))
        return positions

    # (row, col)
    def place(self, player, pos):
        if (not issubclass(type(player), Player)):
            raise TypeError("player must have a player inherited class")
        if (not isinstance(pos, tuple) and len(pos) != 2):
            raise TypeError("Position must be a tuple of (row, col)")
        if ((pos[0] <= 0 and pos[0] > 3) or (pos[1] <= 0 and pos[1] > 3)):
            raise ValueError("Row and Column must be in range of 1 to 3")
        if (self.__isValidMove(pos) == False):
            raise ValueError(str(pos) + " is not a valid move! ")
        
        self.board[pos[0]-1][pos[1]-1] = player.marker

    # Return either mark or bool
    def hasWinner(self):
        #row
        for row in range(3):
            if (all(ele == self.board[row, 0] for ele in self.board[row, :]) and self.board[row, 0] != None):
                return 1
        #col
        for col in range(3):
            if (all(ele == self.board[0, col] for ele in self.board[:, col]) and self.board[0, col] != None):
                return 1
        
        #Diagonal
        if (all(self.board[0, 0] == self.board[col, col] for col in range(3)) and self.board[0][0] != None):
            return 1

        #Diagonal
        if (all(self.board[2, 0] == self.board[col, 3-col-1] for col in range(3)) and self.board[2][0] != None):
            return 1

        if (len(self.getAvailableMove()) == 0):
            return 0

        return -1

    def printBoard(self):
        board_string = "  1   2   3\n"
        for i in range(3):
            board_string += str(i+1)+" "
            for j in range(3):
                if (self.board[i][j] == None):
                    board_string += " "
                else:
                    board_string += str(self.board[i][j])
                if (j != 2):
                    board_string += " | "
            board_string += "\n"
            if (i != 2):
                board_string += " -----------\n"
        print(board_string)

    def getBoardHash(self):
        return str(self.board.reshape(3 * 3))
