import subprocess

def get_board(process):
    process.stdin.write("eval\n")
    process.stdin.flush()

    board = []
    response = ""
    while not response.startswith("0"):
        response = process.stdout.readline()
        if not response.startswith("0"):
            board.append(response.strip().split()[1:])
    response = process.stdout.readline()
    response = process.stdout.readline()   

    return board

def make_moves(process, moves):
    process.stdin.write(f"position startpos moves {' '.join(moves)}\n")
    process.stdin.flush()

def get_board_moves(process, moves = []):
    make_moves(process, moves)
    board = get_board(process)

    return board

def format_board(board):
    formatted = ""
    
    for i in range(8):
        formatted += str(8 - i) + ' ' + ' '.join(board[i]) + '\n'
        
    formatted += "  a b c d e f g h"
    
    return formatted

def get_movelist(process):
    process.stdin.write("perftsplit 1\n")
    process.stdin.flush()

    movelist = []
    response = ""
    
    while not is_integer(response):
        response = process.stdout.readline()
        if not is_integer(response):
            movelist.append(response.strip())

    return movelist

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def square_to_coord(sq):
    x = ord(sq[0]) - ord('a')
    y = ord('8') - ord(sq[1])
    return x, y

def coord_to_square(x, y):
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][x] + str(8 - y)
