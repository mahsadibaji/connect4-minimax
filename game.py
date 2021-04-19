import math
import os
import random

from minimax import Minimax


class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """
    board = []
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    ROW_COUNT = 6
    COL_COUNT = 7
    game_name = "Connect 4"
    colors = ["x", "o"]
    PLAYER_PIECE = colors[0]
    AI_PIECE = colors[1]

    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None

        os.system(['clear', 'cls'][os.name == 'nt'])
        print(f"Welcome to {self.game_name}!")

        # Player is always X and AI is always O
        name = str(input("What is Player's name? "))
        self.players[0] = Player(name, self.PLAYER_PIECE)

        print(f"{self.players[0].name} will be {self.PLAYER_PIECE}")

        diff = int(input("Enter difficulty for this AI (1 - 4) "))
        self.players[1] = AIPlayer(self.AI_PIECE, diff + 1)

        print(f"{self.players[1].name} will be {self.AI_PIECE}")

        # Randomly choose first Player
        self.turn = self.players[random.randint(0, 1)]

        self.board = self.create_empty_board()

    def create_empty_board(self):
        board = []
        for i in range(self.ROW_COUNT):
            board.append([])
            for j in range(self.COL_COUNT):
                board[i].append(' ')
        return board

    def reset(self):
        """ Function to reset the game, but not the names or colors
        """
        self.board = self.create_empty_board()

        # Randomly choose first player
        self.turn = self.players[random.randint(0, 1)]

        self.round = 1
        self.finished = False
        self.winner = None

    def switch_turn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        # increment the round
        self.round += 1

    def next_move(self):
        player = self.turn
        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > self.ROW_COUNT * self.COL_COUNT:
            self.finished = True

        chosen_col = player.move(self.board)

        for i in range(self.ROW_COUNT):
            if self.board[i][chosen_col] == ' ':
                self.board[i][chosen_col] = player.color
                self.switch_turn()
                self.check_for_fours()
                self.show_state()
                return

        print("Invalid move (column is full)")

    def check_for_fours(self):

        for i in range(self.ROW_COUNT):
            for j in range(self.COL_COUNT):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.vertical_check(i, j):
                        self.finished = True
                        self.highlight_four(i, j, 'vertical')

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontal_check(i, j):
                        self.finished = True
                        self.highlight_four(i, j, 'horizontal')

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonal_check(i, j)
                    if diag_fours:
                        self.finished = True
                        self.highlight_four(i, j, 'diagonal', slope)

    def vertical_check(self, row, col):
        four_in_a_row = False
        consecutive_count = 0
        color = self.board[row][col].lower()
        for i in range(row, self.ROW_COUNT):
            if self.board[i][col].lower() == color:
                consecutive_count += 1
            else:
                break

        if consecutive_count >= 4:
            four_in_a_row = True
            if color == self.PLAYER_PIECE:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return four_in_a_row

    def horizontal_check(self, row, col):
        four_in_a_row = False
        consecutive_count = 0
        color = self.board[row][col].lower()

        for j in range(col, self.COL_COUNT):
            if self.board[row][j].lower() == color:
                consecutive_count += 1
            else:
                break

        if consecutive_count >= 4:
            four_in_a_row = True
            if color == self.PLAYER_PIECE:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return four_in_a_row

    def diagonal_check(self, row, col):

        color = self.board[row][col].lower()
        positive_slope = False
        negative_slope = False
        slope = None

        # check for diagonals with positive slope
        consecutive_count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == color:
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= 4:
            positive_slope = True
            slope = 'positive'
            if color == self.PLAYER_PIECE:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == color:
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutive_count >= 4:
            negative_slope = True
            slope = 'negative'
            if color == self.PLAYER_PIECE:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        four_in_a_row = positive_slope or negative_slope
        if positive_slope and negative_slope:
            slope = 'both'
        return four_in_a_row, slope

    def highlight_four(self, row, col, direction, slope=None):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """
        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()

        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()

            if slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def show_state(self):
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])

        print(f"{self.game_name}!")
        print(f"Round: {self.round}")

        for i in range(self.ROW_COUNT - 1, -1, -1):
            print("\t", end="")
            for j in range(self.COL_COUNT):
                print(f"| {str(self.board[i][j])}", end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner is not None:
                print(f"{self.winner.name} is the winner")
            else:
                print("Game was a draw")


class Player(object):
    """ Player object.  This class is for human players.
    """
    name = None
    color = None

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def move(self, state):
        print(f"{self.name}'s turn.  {self.name} is {self.color}")
        column = None
        while column is None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                print("Invalid choice, try again")
                continue
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Column must be between 1 and 7, try again")
        return column


class AIPlayer(Player):
    """ AIPlayer object that extends Player
        The AI algorithm is minimax, the difficulty parameter is the depth to which
        the search tree is expanded.
    """
    difficulty = None

    def __init__(self, color, difficulty=5):
        self.name = 'AI'
        self.color = color
        self.difficulty = difficulty

    def move(self, state):
        print(f"{self.name}'s turn.  {self.name} is {self.color}")

        # time.sleep(random.randrange(8, 17, 1) / 10.0)
        # return random.randint(0, 6)

        m = Minimax(state)
        best_move, value = m.best_move(state=state, depth=self.difficulty, alpha=-math.inf, beta=math.inf,
                                       maximizing_player=True)

        return best_move


if __name__ == "__main__":
    game = Game()
    game.show_state()
    player = game.players[0]
    AI = game.players[1]

    while not game.finished:
        game.next_move()

    game.show_state()
