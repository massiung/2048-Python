'Allows a user to play the game 2048'
import numpy as np


class GameState:
    'Models the current state of the game.'
    defaultState = np.zeros((4, 4), np.int8)

    def __init__(self, state=defaultState, score=0):
        # State of the board is represented by log2 of original.
        # Stored as a numpy 4x4 matrix
        self.state = state
        self.score = score

    def randomTileIs4(self):
        'Roll dice to determine if next tile is a four'
        return (1 == np.random.random_integers(10))

    def placeTile(self):
        'Place a tile randomly'
        # What should it be set to?
        value = (2 if self.randomTileIs4() else 1)

        # Where should it go?
        (freeSpotsRow, freeSpotsColumn) = self.freeSpots()
        spot = np.random.choice(len(freeSpotsRow), 1)
        self.state[freeSpotsRow[spot], freeSpotsColumn[spot]] = value

    def freeSpots(self):
        'The indices of free spots'
        return(np.nonzero(self.state == 0))

    def countFreeSpots(self):
        return len(self.freeSpots()[0])

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
        print('Score: ' + repr(self.score))
        print('Free spots: ' + repr(self.countFreeSpots()))


    def moveLeft(self):
        'Move the blocks to the left'
        for row in range(4):
            # Move all the zeros to the end of row
            self.state[row, :] = pushZerosToEnd(self.state[row, :])

            for column in range(3):
                # Neighbouring block matches
                if (self.state[row, column] != 0 and
                    self.state[row, column] == self.state[row, column + 1]):

                    # Merge blocks and update score
                    self.state[row, column] += 1
                    self.state[row, column+1] = 0
                    self.score += 2 ** self.state[row, column]

            # Move all the zeros to the end of row again
            self.state[row, :] = pushZerosToEnd(self.state[row, :])


    def moveRight(self):
        'Move the blocks to the right'
        self.state = self.state[:, ::-1]
        self.moveLeft()
        self.state = self.state[:, ::-1]

    def moveUp(self):
        'Move the blocks up'
        self.state = self.state.transpose()
        self.moveLeft()
        self.state = self.state.transpose()


    def moveDown(self):
        'Move the blocks down'
        self.state = self.state.transpose()
        self.moveRight()
        self.state = self.state.transpose()


def pushZerosToEnd(arr):
    r'Push all the zeros in an array to the end of the array.'
    # See http://www.geeksforgeeks.org/move-zeroes-end-array/

    count = 0  # Number of non-zero elements

    # Traverse array.
    # If element encountered is nonzero, place it at count
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[count] = arr[i]
            count += 1

    # All nonzero have been shifted left, set rest to 0
    while count < len(arr):
        arr[count] = 0
        count += 1

    return arr


# Main I/O loop
if __name__ == "__main__":
    game = GameState()
    game.randomStart()
    cmd = ''
    instructions = 'Enter a d w or s to slide the blocks and q to quit.'

    # Dictionary for the commands
    cmdSwitcher = {
        'a': 'Left',
        'w': 'Up',
        'd': 'Right',
        's': 'Down'
    }

    # Exit the loop using 'q'
    while cmd != 'q':
        game.printState()
        # Ask for input
        cmd = raw_input('Command: ')
        if cmd in cmdSwitcher:
            # TODO: detect when you have lost.
            # Execute Swticher
            methodName = 'move' + cmdSwitcher[cmd]
            method = getattr(game, methodName, lambda: "Nothing")
            method()

            game.placeTile()
            if game.countFreeSpots() == 0:
                # Game over!
                print('Game over! Total score: ' + repr(game.score))
                break
        elif cmd == 'q':
            break
        else:
            print(instructions)
