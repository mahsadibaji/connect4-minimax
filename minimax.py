import math
import random


class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    board = None
    colors = ["x", "o"]
    PLAYER_PIECE = colors[0]
    AI_PIECE = colors[1]
    ROW_COUNT = 6
    COL_COUNT = 7

    def __init__(self, board):

        self.board = board.copy()

    def best_move(self, state, depth, alpha, beta, maximizing_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        # enumerate all legal moves
        valid_moves = []
        for col in range(self.COL_COUNT):
            # if column i is a legal move...
            if self.is_valid_move(col, state):
                valid_moves.append(col)

        if depth == 0 or self.is_game_over(state):
            return None, self.value(state, self.AI_PIECE)
        if len(valid_moves) == 0:
            return None, 0

        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                temp = self.make_move(state, col, self.AI_PIECE)
                _, new_score = self.best_move(temp, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # minimizing player
            value = math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                temp = self.make_move(state, col, self.PLAYER_PIECE)
                _, new_score = self.best_move(temp, depth - 1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    column = col
                alpha = min(alpha, value)
                if alpha >= beta:
                    break
            return column, value

    def is_valid_move(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        for i in range(self.ROW_COUNT):
            if state[i][column] == ' ':
                return True
        # if we get here, the column is full
        return False

    def is_game_over(self, state):

        return self.count_streak(state, self.PLAYER_PIECE, 4) >= 1 \
               or self.count_streak(state, self.AI_PIECE, 4) >= 1

    def make_move(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'

            Returns a copy of new state array with the added move
        """
        temp = [x[:] for x in state]
        for i in range(self.ROW_COUNT):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
        """
        if color == self.PLAYER_PIECE:
            o_color = self.AI_PIECE
        else:
            o_color = self.PLAYER_PIECE

        center_array = [row[self.COL_COUNT // 2] for row in state]
        center_count = center_array.count(color)

        my_fours = self.count_streak(state, color, 4)
        my_threes = self.count_streak(state, color, 3)
        my_twos = self.count_streak(state, color, 2)
        opp_fours = self.count_streak(state, o_color, 4)
        opp_threes = self.count_streak(state, o_color, 3)

        if opp_fours > 0:
            return -100000
        else:
            return center_count * 3 + my_fours * 100 + my_threes * 5 + my_twos * 2 - opp_threes * 4

    def count_streak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(self.ROW_COUNT):
            for j in range(self.COL_COUNT):
                if state[i][j].lower() == color.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.vertical_streak(i, j, state, streak)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontal_streak(i, j, state, streak)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonal_streak(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count

    def vertical_streak(self, row, col, state, streak):
        consecutive_count = 0
        color = state[row][col].lower()
        for i in range(row, self.ROW_COUNT):
            if state[i][col].lower() == color:
                consecutive_count += 1
            else:
                break

        return 1 if consecutive_count >= streak else 0

    def horizontal_streak(self, row, col, state, streak):
        consecutive_count = 0
        color = state[row][col].lower()

        for j in range(col, self.COL_COUNT):
            if state[row][j].lower() == color:
                consecutive_count += 1
            else:
                break

        return 1 if consecutive_count >= streak else 0

    def diagonal_streak(self, row, col, state, streak):
        color = state[row][col].lower()
        total = 0
        # check for diagonals with positive slope
        consecutive_count = 0
        j = col
        for i in range(row, self.ROW_COUNT):
            if j > self.COL_COUNT - 1:
                break
            elif state[i][j].lower() == color:
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > self.COL_COUNT - 1:
                break
            elif state[i][j].lower() == color:
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= streak:
            total += 1

        return total
