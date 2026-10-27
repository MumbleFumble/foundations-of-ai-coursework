import numpy as np
import copy


def create_board(shape=(6, 7)) -> np.ndarray:
    """
    Outputs a board of zeros with the specified shape.
    Inputs:
        shape (tuple): Dimensions of the board.
    Outputs:
        board (np.ndarray): The board.
    """
    return np.zeros(shape, dtype=int)


def drop_piece(board: np.ndarray, row: int, col: int, piece: np.ndarray) -> np.ndarray:
    """
    Drop piece into the board at the specified location.
    Inputs:
        board (np.ndarray): The board.
        row (int): The row to drop the piece into.
        col (int): The column to drop the piece into.
        piece (int): The piece to drop (1 or 2).
    Outputs:
        board (np.ndarray): The board with the piece dropped.
    """
    board = copy.deepcopy(board)
    board[row][col] = piece
    return board


def is_valid_location(board: np.ndarray, col: int) -> bool:
    """
    Checks if is legal move

    Inputs:
        board (np.ndarray): The board.
        col (int): The column to drop the piece into.
    Outputs:
        valid_location (bool): True if the move is valid, False otherwise.
    """
    return board[-1][col] == 0


def get_next_open_row(board, col):
    """
    For a given column, return the first empty row.
    This is where a piece will end up.

    Inputs:
        board (np.ndarray): The board.
        col (int): The column to drop the piece into.
    Outputs:
        next_open_row (int): The row where the piece will end up.
    """
    rows = board.shape[0]
    for r in range(rows):
        if board[r][col] == 0:
            return r


def print_board(board: np.ndarray):
    """
    Visualize the board.
    """
    print(np.flipud(board))


def all_connect_four_slices(board: np.ndarray):
    """
    Get all possible 4 adjacent cells in a row, column, or diagonal (slice).

    Inputs:
        board (np.ndarray): The board.
    Outputs:
        connect_fours (np.ndarray): All possible 4 adjacent cells in a row, column, or diagonal.
    """
    rows, cols = board.shape
    connect_fours = []
    # All horizontal four-in-a-rows
    for c in range(cols - 3):
        connect_fours.append(board[:, c: c + 4])
    # All vertical four-in-a-rows
    for r in range(rows - 3):
        connect_fours.append(board[r: r + 4, :].T)
    # All diagonal four-in-a-rows
    for r in range(rows - 3):
        for c in range(cols - 3):
            # Add both diagonals for each 4x4 square in board
            square = board[r: r + 4, c: c + 4]
            connect_fours.append(
                [
                    square.diagonal(),
                    np.fliplr(square).diagonal(),
                ]
            )
    return np.concatenate(connect_fours).astype(int)


def winning_move(board: np.ndarray, piece: int):
    """
    Is this state terminal and did the given piece win?

    Inputs:
        board (np.ndarray): The board.
        piece (int): The piece to check for (1 or 2).
    Outputs:
        is_terminal (bool): True if the game is over and the specified piece color won
    """
    return (all_connect_four_slices(board) == piece).all(axis=1).any()