# playing the game
import re
import random

class MineBoard:
    def __init__(self, DimSize, NumBombs):
        # here we'll keep track of our parameters
        self.DimSize = DimSize
        self.NumBombs = NumBombs

        # here we'll create board
        self.Board = self.MakeNewBoard()
        self.AssingValuesToBoard()

        # we also need to keep track of where we've dug and where
        # the remaining bombs are
        self.dug = set()

    def MakeNewBoard(self):
        Board = [[None for _ in range(self.DimSize)] for _ in range(self.DimSize)]
    
    # plant bombs
        BombsPlanted = 0

        while BombsPlanted < self.NumBombs:
            Location = random.randint(0, self.DimSize**2 - 1) # return a random in N that a <= N <= B
            Row = Location // self.DimSize
            Coloumn = Location % self.DimSize

            if Board[Row][Coloumn] == '*':
                # this means we already have a bomb keep iterating
                continue

            Board[Row][Coloumn] = '*' # plant bomb
            BombsPlanted += 1

        return Board

    def AssingValuesToBoard(self):
        # after we place bombs we need to give each square a value to show
        # how close they are to a relative bomb
        for r in range(self.DimSize):
            for c in range(self.DimSize):
                if self.Board[r][c] == '*':
                    # if its a bomb dont calculate a value
                    continue
                self.Board[r][c] = self.GetNumNeighborBombs(r, c)

    def GetNumNeighborBombs(self, Row, Coloumn):

        # must iterat through each square adjacent to the current space
        # so imagine a 3x3 grid and how would you tell the computer
        # to navigate through each of those spots
        NumNeighborBombs = 0
        for r in range(max(0, Row - 1), min(self.DimSize - 1, Row + 1) + 1):
            for c in range(max(0, Coloumn-1), min(self.DimSize - 1, Coloumn + 1) + 1):
                if r == Row and c == Coloumn: # this is the original location
                    continue
                if self.Board[r][c] == '*':
                    NumNeighborBombs += 1
        return NumNeighborBombs
                
    def dig(self, Row, Coloumn):
        # possibilites
        # can hit a bomb
        # dig and reveal neighboring bombs
        # dig and theres nothing nearby, contiue recursively until 
        # a nearby bomb is found

        self.dug.add((Row, Coloumn))
        
        if self.Board[Row][Coloumn] == '*':
            return False
        elif self.Board[Row][Coloumn] > 0:
            return True

        for r in range(max(0, Row - 1), min(self.DimSize - 1, Row + 1) + 1):
            for c in range(max(0, Coloumn-1), min(self.DimSize - 1, Coloumn + 1) + 1):
                if (r, c) in self.dug:
                    continue # dont dig where you've been
                self.dig(r, c)
        # should have already checked for bombs so should be good
        return True
        
    def __str__(self):
        # this useful function where when called
        # itll print whatever this returns
        # so we'll use it to show the board to the player
        VisibleBoard = [[None for _ in range(self.DimSize)] for _ in range(self.DimSize)]
        for Row in range(self.DimSize):
            for Coloumn in range(self.DimSize):
                if (Row,Coloumn) in self.dug:
                    VisibleBoard[Row][Coloumn] = str(self.Board[Row][Coloumn])
                else:
                    VisibleBoard[Row][Coloumn] = ' '

        # put this entire string together to represent board
        StringRep = ''

        widths = []
        for idx in range(self.DimSize):
            columns = map(lambda x: x[idx], VisibleBoard)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.DimSize)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(VisibleBoard)):
            row = VisibleBoard[i]
            StringRep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            StringRep += ' |'.join(cells)
            StringRep += ' |\n'

        str_len = int(len(StringRep) / self.DimSize)
        StringRep = indices_row + '-'*str_len + '\n' + StringRep + '-'*str_len

        return StringRep




def MineSweep(DimSize = 10, NumBombs = 10):
    Board = MineBoard(DimSize, NumBombs)


    # Outline
    # 1. Create grid and bombs
    # 2. Present or hide board and give player square selection
    # 3. a. If they hit a bomb the game ends
    #       b. If no bomb is present, we dig recursively until
    #        the square is at least next to a bomb. Show number
    #        to represent how many bombs are adjacent
    # 4. Repeat steps 2 and 3 until no more squares are left
    while len(Board.dug) < Board.DimSize ** 2 - NumBombs:
        print(Board)
        UserInput = re.split(',(\\s)*', input("Where would you like to dig? Input row, coloumn: "))
        Row, Coloumn = int(UserInput[0]), int(UserInput[-1])
        if Row < 0 or Row >= Board.DimSize or Coloumn < 0 or Coloumn >= DimSize:
            print("Invalid location, Try again.")
            continue

        # if its valid we accept it
        safe = Board.dig(Row, Coloumn)
        if not safe:
            # dug a bomb
            

            break # game ends
            

    # you win by uncovering bombs or you hit a bomb

    if safe:
        print("Congradulations! You succesfully swept the Mine Field.")
    else:
        print("You lost! Try again?")
        # Reveal the hidden bombs
        Board.dug = [(r,c) for r in range(Board.DimSize) for c in range(Board.DimSize)]
        print(Board)


if __name__ == '__main__':
# good practice for only running whats in this one file
    MineSweep()
