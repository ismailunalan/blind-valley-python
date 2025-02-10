import sys


def boardCreator(lenVer,lenHor):
    # Creates a table suitable for the size given in the input.
    board = []
    for row in range(lenVer):
        board.append([])
        for col in range(lenHor):
            board[row].append(" ")
    return board


def neighbourChecker(board, currentRow, currentCol):
    # Checks the neighbors of the location to be placed.
    if board[currentRow][currentCol] != "N":
        if currentRow + 1 < len(board) and board[currentRow + 1][currentCol] == board[currentRow][currentCol]:
            return False
        elif currentRow - 1 >= 0 and board[currentRow - 1][currentCol] == board[currentRow][currentCol]:
            return False
        elif currentCol + 1 < len(board[0]) and board[currentRow][currentCol + 1] == board[currentRow][currentCol]:
            return False
        elif currentCol - 1 >= 0 and board[currentRow][currentCol - 1] == board[currentRow][currentCol]:
            return False
        else:
            return True
    else:
        # Skips if the location to be checked contains "N".
        return True


def limitchecker(board,  lenVer, lenHor, inputContent):
    # It checks whether the filled table complies with the limit values.
    for i in range(lenVer):
        # For row control, the values given in the input and the values in the table are assigned to variables.
        hcountrow = board[i].count("H")
        hlimitrow = int(inputContent[0][i])
        bcountrow = board[i].count("B")
        blimitrow = int(inputContent[1][i])
        if hlimitrow == -1 or hcountrow == hlimitrow:
            if blimitrow == -1 or bcountrow == blimitrow:
                for j in range(lenHor):
                    # Does the same thing for columns.
                    hcountcol = [row[j] for row in board].count("H")
                    hlimitcol = int(inputContent[2][j])
                    bcountcol = [row[j] for row in board].count("B")
                    blimitcol = int(inputContent[3][j])
                    if hlimitcol == -1 or hcountcol == hlimitcol:
                        if blimitcol == -1 or bcountcol == blimitcol:
                            # Repeats until all rows and columns are checked.
                            continue
                        else:
                            return False
                    else:
                        return False
            else:
                return False
        else:
            return False
    return True


def solver(style, inputContent, board, currentRow, currentCol, lenVer, lenHor, possibilities):
    # The function where the actual placement steps of the game are made
    # according to style, neighbor control and limit control.
    for i in range(3):
        # A for loop to try the values "H B, B H and N N".
        if style[currentRow][currentCol] == "L":
            # For horizontal placement.
            board[currentRow][currentCol], board[currentRow][currentCol + 1] = possibilities[i]
            if neighbourChecker(board, currentRow, currentCol) and neighbourChecker(board, currentRow, currentCol + 1):
                # Decides which location to take next.
                if currentCol + 2 < len(board[0]) and currentRow < len(board):
                    # Recursion call for next position.
                    if solver(style, inputContent, board, currentRow, currentCol + 2, lenVer, lenHor, possibilities):
                        return True
                    else:
                        continue
                elif currentRow + 1 < len(board):
                    # Recursion call for next position.
                    if solver(style, inputContent, board, currentRow + 1, 0, lenVer, lenHor, possibilities):
                        return True
                    else:
                        continue
                else:
                    # If the end of the table is reached, limit values are checked.
                    if limitchecker(board,  lenVer, lenHor, inputContent):
                        return board
                    else:
                        continue
            else:
                continue

        elif style[currentRow][currentCol] == "U":
            # For vertical placement.
            board[currentRow][currentCol], board[currentRow + 1][currentCol] = possibilities[i]
            if neighbourChecker(board, currentRow, currentCol) and neighbourChecker(board, currentRow + 1, currentCol):
                # Decides which location to take next.
                if currentCol + 1 < len(board[0]) and currentRow < len(board):
                    # Recursion call for next position.
                    if solver(style, inputContent, board, currentRow, currentCol + 1, lenVer, lenHor, possibilities):
                        return True
                    else:
                        continue
                elif currentRow + 1 < len(board):
                    # Recursion call for next position.
                    if solver(style, inputContent, board, currentRow + 1, 0, lenVer, lenHor, possibilities):
                        return True
                    else:
                        continue
                else:
                    # If the end of the table is reached, limit values are checked.
                    if limitchecker(board, lenVer, lenHor, inputContent):
                        return board
                    else:
                        continue
            else:
                continue

        else:
            if currentCol + 1 < len(board[0]) and currentRow < len(board):
                # Recursion call for next position.
                if solver(style, inputContent, board, currentRow, currentCol + 1, lenVer, lenHor, possibilities):
                    return True
                else:
                    return False
            elif currentRow + 1 < len(board):
                # Recursion call for next position.
                if solver(style, inputContent, board, currentRow + 1, 0, lenVer, lenHor, possibilities):
                    return True
            else:
                # If the end of the table is reached, limit values are checked.
                if limitchecker(board, lenVer, lenHor, inputContent):
                    return board
                else:
                    continue
    return False


def main():
    # Reads input file.
    with open(sys.argv[1], "r") as inputfile:
        inputContent = [list(row.split()) for row in inputfile]
    possibilities = [["H","B"],["B","H"],["N","N"]] # Possibilities to be tried in order.
    lenVer = len(inputContent[0]) # Vertical length of the table.
    lenHor = len(inputContent[2]) # Horizontal length of the table.
    style = inputContent[4::] # Information to be placed horizontally or vertically on the table.
    board = boardCreator(lenVer,lenHor)
    currentRow = 0 # Keeps current row information.
    currentCol = 0 # Keeps current column information.
    with open(sys.argv[2], "w") as outputfile:
        if solver(style, inputContent, board, currentRow, currentCol, lenVer, lenHor, possibilities):
            i = 0
            for line in board:
                i += 1
                outputfile.write(" ".join(map(str, line)))
                if i != len(board):
                    outputfile.write("\n")
        else:
            outputfile.write("No solution!")


if __name__ == "__main__":
    main()