#   Import packages
from requests_html import HTMLSession
from requests_html import HTML

#   I didn't find any free api wich can provide new unsolved sudoku's
#   But i find a website wich do the job so i decide to srap him
def scrap(board):
    session = HTMLSession()
    response = session.get("https://www.sudokuweb.org/")

    lines = response.html.find("#line")
    for i in range(1,9):
        lines.append(response.html.find(f"#line{i}")[0])

    for line in lines:
        tmpboard = []
        for piece in line.html.split('<'):
            if "vloz" in piece or "sedy" in piece:
                tmp = piece.split(">")[1]
                if tmp.isdigit():
                    tmpboard.append(int(tmp))
                else:
                    tmpboard.append(0)
        board.append(tmpboard)

#   Find the next empty element
def findEmpty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i,j)
    return None

def printBoard(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-"*15)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|",end="")
            if j == 8:
                print(board[i][j])
            else:
                print(board[i][j],end="")

#   Check if coud be a valid solution
def valid(board, num, pos):
    #   Check for the row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    #   Check for the column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    
    #   Check for the box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3 ):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

def solve(board):
    pos = findEmpty(board)
    if not pos: #   If we don't have more empty spot we are done
        return True
    else:
        row, col = pos
        for i in range(1,10):   #   Try every possible solutions
            if valid(board,i,(row,col)):
                board[row][col] = i
                if solve(board):    #   If it can be a valid solution repeat
                    return True
                board[row][col] = 0 #   If it can't we set it back to 0
    return False    #   If we can't find any possible solution 
            

def main():
    board = []
    scrap(board)
    printBoard(board)
    solve(board)
    print("*"*20)
    printBoard(board)


main()