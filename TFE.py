'Allows a user to play the game 2048'
import numpy as np
import Tkinter as tk

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

def runCLI():
    'Command Line Interface for the 2048 game.'
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

    # I/O loop. Exit the loop using 'q'
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

colours = {
    0: 'white',
    1: 'yellow',
    2: 'orange',
    3: 'green',
    4: 'blue',
    5: 'brown',
    6: 'grey'
}

class GUITFE(tk.Frame):
    'Graphical User Interface for 2048'
    def __init__(self, master, gameState):
        tk.Frame.__init__(self, master)
        self.gameState = gameState
        self.canvases = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.rectangles = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.texts = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.scoreCanvas = None
        self.createBlocks()
        self.master.title('GUI 2048')
        self.master.bind('<Left>', self.leftBind)
        self.master.bind('<Up>', self.upBind)
        self.master.bind('<Right>', self.rightBind)
        self.master.bind('<Down>', self.downBind)
        self.grid()

    def createBlocks(self):
        for row in range(4):
            for column in range(4):
                self.canvases[row][column] = canvas = tk.Canvas(self, width=60, height=60)
                canvas.grid(row=row, column=column)
                value=self.gameState.state[row,column]

                # Determine the colour of the square from the value
                colour = ''
                if value in colours:
                    colour = colours[value]
                else:
                    colour = 'grey'
                # Determine the text on the square
                text = ''
                if value == 0:
                    text = ''
                else:
                    text = repr(2**value)

                # Make the coloured square
                self.rectangles[row][column] = canvas.create_rectangle(2,2,58,58,fill=colour)
                # Put the text on the square
                self.texts[row][column] = canvas.create_text(30,30,text=text)

        self.scoreCanvas = tk.Canvas(self, width=120, height=60)
        self.scoreCanvas.grid(row=4, column=2, columnspan=2)
        self.scoreCanvas.create_text(60,30,text="Score: " + repr(self.gameState.score))

    def updateBlocks(self):
        for row in range(4):
            for column in range(4):
                canvas = self.canvases[row][column]
                canvas.delete("all")
                value = self.gameState.state[row,column]

                # Determine the colour of the square from the value
                colour = ''
                if value in colours:
                    colour = colours[value]
                else:
                    colour = 'grey'
                # Determine the text on the square
                text = ''
                if value == 0:
                    text = ''
                else:
                    text = repr(2**value)

                self.rectangles[row][column] = canvas.create_rectangle(2,2,58,58,fill=colour)
                self.texts[row][column] = canvas.create_text(30,30,text=text)
        self.scoreCanvas.delete("all")
        self.scoreCanvas.create_text(60,30,text="Score: " + repr(self.gameState.score))

    def leftBind(self, event=None):
        oldState = np.copy(self.gameState.state)
        self.gameState.moveLeft()
        if not np.array_equal(self.gameState.state, oldState):
            self.gameState.placeTile()
            self.updateBlocks()

    def rightBind(self, event=None):
        oldState = np.copy(self.gameState.state)
        self.gameState.moveRight()
        if not np.array_equal(self.gameState.state, oldState):
            self.gameState.placeTile()
            self.updateBlocks()

    def upBind(self, event=None):
        oldState = np.copy(self.gameState.state)
        self.gameState.moveUp()
        if not np.array_equal(self.gameState.state, oldState):
            self.gameState.placeTile()
            self.updateBlocks()

    def downBind(self, event=None):
        oldState = np.copy(self.gameState.state)
        self.gameState.moveDown()
        if not np.array_equal(self.gameState.state, oldState):
            self.gameState.placeTile()
            self.updateBlocks()

def test(event):
    print('Left!!!')

game = GameState()
game.randomStart()

app = GUITFE(None, game)
app.mainloop()

#if __name__ == "__main__":
#    runCLI()
