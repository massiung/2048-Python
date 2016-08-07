'Allows a user to play the game 2048'
import numpy as np


class GameState:
    'Models the current state of the game.'
    defaultState = np.zeros((4, 4), np.int8)

    def __init__(self, state=defaultState, score=0):
        self.state = state
        self.score = score

    def randomTileIs4():
        'Roll dice to determine if next tile is a four'
        return (1 == np.random.random_integers(10))

    def placeTile(self):
        'Place a tile randomly'
        # What should it be set to?
        value = 4 if GameState.randomTileIs4() else 2

        # Where should it go?
        freeSpots = self.freeSpots()
        spot = np.random.random_integers(len(freeSpots) - 1)
        self.state[freeSpots[spot]] = value

    def freeSpots(self):
        'The indices of free spots'
        return(np.nonzero(self.state != 0))

    def randomStart(self):
        'Place two random tiles'
        self.placeTile()
        self.placeTile()

    # TODO Improve the visualization
    def printState(self):
        'Print the current state of the board'
        for row in range(4):
            line = ''
            for column in range(4):
                line += str(self.state[row, column])
            print line

    def moveLeft(self):
        'Move the blocks to the left'
        for row in range(4):
            for column in range(3):
                # Neighbouring block matches
                if (self.state[row, column] != 0 and
                    self.state[row, column] == self.state[row, column + 1]):
                    # Merge blocks and update score
                    self.state[row, column] += 1
                    self.state[row, column+1] = 0
                    self.score += self.state[row, column]
            # TODO Shift all to the left

    def moveRight(self):
        'Move the blocks to the right'
        # TODO

    def moveUp(self):
        'Move the blocks up'
        self.state.transpose()
        self.moveLeft()
        self.state.transpose()

    def moveDown(self):
        'Move the blocks down'
        self.state.transpose()
        self.moveRight()
        self.state.transpose()

if __name__ == "__main__":
    # TODO Write I/O loop
    game = GameState()
    game.randomStart()
    cmd = ''
    while cmd != 'q':
        # Ask for input

        # Cases for a d s w as commands
