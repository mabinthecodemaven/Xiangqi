# Author: Mason Mabin
# Date: 3/10/2020
# Description: A recreation of the game Xiangxi. I had a lot of fun making this. This is my second draft. The main
# difference from this and the first is that I realized that having 7 unique piece classes for each type was not
# at all necessary. I also streamlined the potential move updating process. It used to be that each updating function
# for each type of piece scanned through all of the pieces and picked out its type of piece to update its potential
# moves. Now the update_all_moves function does one scan and passes each piece through its appropriate updating
# function. Other than these two things, everything is the same.


class Piece:
    """Used to represent all pieces in the game."""

    def __init__(self, location, team, type):
        """Sets the location, team, and what kind of piece it is."""
        self._location = location
        self._team = team
        self._type = type

        self._icon = self._type + self._team
        self._potential_moves = []

    def move(self, location):
        """To change the location data member."""
        self._location = location

    def get_location(self):
        """To retrieve the location."""
        return self._location

    def get_team(self):
        """To retrieve the team."""
        return self._team

    def get_type(self):
        """To retrieve the type."""
        return self._type

    def get_icon(self):
        """To retrieve the icon."""
        return self._icon

    def get_potential_moves(self):
        """To retrieve the potential moves."""
        return self._potential_moves

    def set_potential_moves(self, moves):
        """To set the potential moves."""
        self._potential_moves = moves

    def set_location(self, move):
        """To change the location data member."""
        self._location = move


class Board:
    """This is the main brain class. Dictates how each piece on the board can move, keeps track of the check and
    checkmate situation, whose turn it is, and contains a printable readout of the board."""

    def __init__(self):
        """Initializes all the data types, adds the pieces, sets their potential moves."""

        self._pieces = {}
        self._red_potential_moves = set()
        self._black_potential_moves = set()
        self._in_check = None
        self._turn = 'r'
        self._display = []
        self._winner = None
        self._temp_piece = None

        # Blank board.
        for i in range(11):
            self._display.append([])
            for j in range(10):
                self._display[i].append('  ')

        # This chunk adds labels to the rows and columns
        self._display[0][0] = '*'
        for i in range(9):
            self._display[i + 1][0] = str(i + 1)
        self._display[10][0] = 'X'
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for i in range(9):
            self._display[0][i + 1] = letters[i].upper() + ' '

        # ADDS SOLDIERS
        for i in range(1, 11, 2):  # adds red soldier pieces
            self._pieces[(4, i)] = Piece((4, i), 'r', 'S')
        for i in range(1, 11, 2):  # adds black soldier pieces
            self._pieces[(7, i)] = Piece((7, i), 'b', 'S')

        # ADDS HORSES
        for i in [2, 8]:  # Adds red horses
            self._pieces[(1, i)] = Piece((1, i), 'r', 'H')
        for i in [2, 8]:  # Adds black horses
            self._pieces[(10, i)] = Piece((10, i), 'b', 'H')

        # ADDS GENERALS
        self._pieces[(1, 5)] = Piece((1, 5), 'r', 'G')
        self._pieces[(10, 5)] = Piece((10, 5), 'b', 'G')

        # ADDS CHARIOTS
        for space in [(1, 1), (1, 9)]:
            self._pieces[space] = Piece(space, 'r', 'R')
        for space in [(10, 1), (10, 9)]:
            self._pieces[space] = Piece(space, 'b', 'R')

        # ADDS CANNONS
        for space in [(3, 2), (3, 8)]:
            self._pieces[space] = Piece(space, 'r', 'C')
        for space in [(8, 2), (8, 8)]:
            self._pieces[space] = Piece(space, 'b', 'C')

        # ADDS ADVISORS
        for space in [(1, 4), (1, 6)]:
            self._pieces[space] = Piece(space, 'r', 'A')
        for space in [(10, 4), (10, 6)]:
            self._pieces[space] = Piece(space, 'b', 'A')

        # ADDS ELEPHANTS
        for space in [(1, 3), (1, 7)]:
            self._pieces[space] = Piece(space, 'r', 'E')
        for space in [(10, 3), (10, 7)]:
            self._pieces[space] = Piece(space, 'b', 'E')

        # Sets potential moves for all pieces, updates display.
        self.update_all_moves()
        self.update_board()

    def update_board(self):
        """Sets each space on the board to the appropriate piece icon or blank."""
        for i in range(1, 11):
            for j in range(1, 10):
                if (i, j) in self._pieces:
                    self._display[i][j] = self._pieces[(i, j)].get_icon()
                else:
                    self._display[i][j] = '  '

    def show_board(self):
        """Displays the board as it is currently."""
        for i in range(10, -1, -1):
            print(self._display[i])

    def next_turn(self):
        """Increments who's turn it is."""
        if self._turn == 'r':
            self._turn = 'b'
        else:
            self._turn = 'r'

    def get_winner(self):
        """Retrieves the winner."""
        return self._winner

    def get_in_check(self):
        """Retrieves who is in check."""
        return self._in_check

    def update_soldier_moves(self, soldier):
        """Sets the potential moves of the soldier passed through."""

        location = soldier.get_location()
        team = soldier.get_team()
        on_board_moves = []
        valid_moves = []

        if team == 'r':

            # Adds north move unless piece is at the end of the board
            if location[0] <= 9:
                on_board_moves.append((location[0] + 1, location[1]))

            # Adds horizontal moves if piece is across the river and if their is room on the appropriate side
            if location[0] >= 6:
                if location[1] >= 2:
                    on_board_moves.append((location[0], location[1] - 1))
                if location[1] <= 8:
                    on_board_moves.append((location[0], location[1] + 1))

        # Same as above but for black soldier
        if team == 'b':

            if location[0] >= 2:
                on_board_moves.append((location[0] - 1, location[1]))
            if location[0] <= 5:
                if location[1] >= 2:
                    on_board_moves.append((location[0], location[1] - 1))
                if location[1] <= 8:
                    on_board_moves.append((location[0], location[1] + 1))

        # Only counts moves that are not occupied by same team.
        for move in on_board_moves:
            if move not in self._pieces or self._pieces[move].get_team() != team:
                valid_moves.append(move)

        soldier.set_potential_moves(valid_moves)

    def update_horse_moves(self, horse):
        """Sets the potential moves of the horse passed through."""
        location = horse.get_location()
        first_steps = []
        valid_moves = []

        # Adds up to 4 orthogonal 'first steps' iff they are not occupied by any piece.
        for i in [1, -1]:
            spot = (location[0] + i, location[1])
            if spot not in self._pieces:
                if spot[0] in range(1, 11) and spot[1] in range(1, 10):
                    first_steps.append(spot)

            spot = (location[0], location[1] + i)
            if spot not in self._pieces:
                if spot[0] in range(1, 11) and spot[1] in range(1, 10):
                    first_steps.append(spot)

        for step in first_steps:

            # Block 1. If the first step is 'north' or 'south' on the board
            for i in [1, -1]:
                if step[0] - location[0] == i:

                    for j in [1, -1]:
                        spot = (location[0] + 2 * i, location[1] + j)
                        if spot not in self._pieces or self._pieces[spot].get_team() != horse.get_team():
                            if spot[0] in range(1, 11) and spot[1] in range(1, 10):
                                # Adds move as long as the spot does not contain same team piece
                                valid_moves.append(spot)

            # Block 2 if the first step is 'east' or 'west'
            for i in [1, -1]:
                if step[1] - location[1] == i:

                    for j in [1, -1]:
                        spot = (location[0] + j, location[1] + 2 * i)
                        if spot not in self._pieces or self._pieces[spot].get_team() != horse.get_team():
                            if spot[0] in range(1, 11) and spot[1] in range(1, 10):
                                valid_moves.append(spot)

        horse.set_potential_moves(valid_moves)

    def update_general_moves(self, general):
        """Updates the potential moves of the general passed through."""
        location = general.get_location()
        valid_moves = []

        # Adds up to 4 orthogonal moves if they are inside the palace and not same team occupied.
        for i in [1, -1]:

            if general.get_team() == 'r':
                # Looks at both potential vertical moves
                spot = (location[0] + i, location[1])
                # Checks for non same team occupied space:
                if spot not in self._pieces or self._pieces[spot].get_team() != general.get_team():
                    # Checks for space to be inside palace
                    if spot[0] in range(1, 4) and spot[1] in range(4, 7):
                        valid_moves.append(spot)

                # Same but for left/right moves.
                spot = (location[0], location[1] + i)
                if spot not in self._pieces or self._pieces[spot].get_team() != general.get_team():
                    if spot[0] in range(1, 4) and spot[1] in range(4, 7):
                        valid_moves.append(spot)

            else:  # same but for black king, because the palace is different.
                spot = (location[0] + i, location[1])
                if spot not in self._pieces or self._pieces[spot].get_team() != general.get_team():
                    if spot[0] in range(8, 11) and spot[1] in range(4, 7):
                        valid_moves.append(spot)

                spot = (location[0], location[1] + i)
                if spot not in self._pieces or self._pieces[spot].get_team() != general.get_team():
                    if spot[0] in range(8, 11) and spot[1] in range(4, 7):
                        valid_moves.append(spot)

        general.set_potential_moves(valid_moves)

    def update_chariot_moves(self, chariot):
        """Updates the potential moves of the chariot passed through."""

        rank = chariot.get_location()[0]
        file = chariot.get_location()[1]
        chariot.set_potential_moves([])

        new_moves = []

        # Adds spaces along the same file up and down the ranks

        # For loop to look in both directions
        for i in [1, -1]:
            r = int(rank) + i
            piece_reached = False
            # Keeps adding pieces until any piece is reached, or end of the board.
            while not piece_reached and r in range(1, 11):
                if (r, file) in self._pieces:
                    piece_reached = True
                    # If the piece reached is enemy, it will add that space too.
                    if self._pieces[(r, file)].get_team() != chariot.get_team():
                        new_moves.append((r, file))
                else:
                    new_moves.append((r, file))
                r += i

        # Adds spaces along the same rank left and right across the files. Same exact method as above.
        for i in [1, -1]:
            f = int(file) + i
            piece_reached = False
            while not piece_reached and f in range(1, 10):
                if (rank, f) in self._pieces:
                    piece_reached = True
                    if self._pieces[(rank, f)].get_team() != chariot.get_team():
                        new_moves.append((rank, f))
                else:
                    new_moves.append((rank, f))
                f += i

        chariot.set_potential_moves(new_moves)

    def update_cannon_moves(self, cannon):
        """Updates the potential moves of the cannon passed through."""

        rank = cannon.get_location()[0]
        file = cannon.get_location()[1]
        cannon.set_potential_moves([])

        new_moves = []

        # Adds spaces along the same file up and down the ranks
        for i in [1, -1]:
            r = int(rank) + i
            piece_reached = False
            second_piece_reached = False
            # Adds spaces until a piece is reached/ end of board
            while not piece_reached and r in range(1, 11):
                if (r, file) in self._pieces:
                    piece_reached = True
                else:
                    new_moves.append((r, file))
                r += i
            # Looks at spots behind first piece reached. If the very next piece encountered is enemy, adds it.
            # Otherwise stops at same team piece/ end of board.
            while r in range(1, 11) and not second_piece_reached:
                if (r, file) in self._pieces:
                    second_piece_reached = True
                    if self._pieces[(r, file)].get_team() != cannon.get_team():
                        new_moves.append((r, file))
                r += i

        # Adds spaces horizontally across files.
        for i in [1, -1]:
            f = int(file) + i
            piece_reached = False
            second_piece_reached = False

            # Adds open spaces until a piece is reached.
            while not piece_reached and f in range(1, 10):
                if (rank, f) in self._pieces:
                    piece_reached = True
                else:
                    new_moves.append((rank, f))
                f += i

            # If a piece is reached, it then looks behind that piece and only adds one more move iff it is an
            # enemy.
            while f in range(1, 10) and not second_piece_reached:
                if (rank, f) in self._pieces:
                    second_piece_reached = True
                    if self._pieces[(rank, f)].get_team() != cannon.get_team():
                        new_moves.append((rank, f))
                f += i
        cannon.set_potential_moves(new_moves)

    def update_advisor_moves(self, advisor):
        """Updates the potential moves of the advisor passed through it."""
        location = advisor.get_location()
        team = advisor.get_team()
        valid_moves = []

        # For loops generate the 4 diagonal directions.
        for i in [1, -1]:
            for j in [1, -1]:
                space = (location[0] + i, location[1] + j)

                # Makes sure space is non same team occupied.
                if space not in self._pieces or self._pieces[space].get_team() != team:

                    # Makes sure space is in appropriate palace
                    if team == 'r':
                        if space[0] in range(1, 4) and space[1] in range(4, 7):
                            valid_moves.append(space)

                    if team == 'b':
                        if space[0] in range(8, 11) and space[1] in range(4, 7):
                            valid_moves.append(space)

        advisor.set_potential_moves(valid_moves)

    def update_elephant_moves(self, elephant):
        """Updates the potential moves of the elephant piece passed through it."""

        location = elephant.get_location()
        team = elephant.get_team()
        potential_moves = []

        # For loops to generate 4 diagonal directions.
        for i in [-1, 1]:
            for j in [-1, 1]:

                if team == 'r':

                    # This first step must be in the proper range of the board.
                    first_step = (location[0] + i, location[1] + j)
                    if first_step[0] in range(2, 5) and first_step[1] in range(2, 9):

                        # First step must be open
                        if first_step not in self._pieces:
                            new_rank = location[0] + 2 * i
                            new_file = location[1] + 2 * j
                            move = (new_rank, new_file)

                            # Final position of move must be open or enemy occupied, and on the correct side of
                            # the river.
                            if new_rank in range(1, 6) and new_file in range(1, 10):
                                if move not in self._pieces or self._pieces[move].get_team() != team:
                                    potential_moves.append(move)

                else:  # All the same, but for team black
                    first_step = (location[0] + i, location[1] + j)
                    if first_step[0] in range(7, 10) and first_step[1] in range(2, 9):
                        if first_step not in self._pieces:
                            new_rank = location[0] + 2 * i
                            new_file = location[1] + 2 * j
                            move = (new_rank, new_file)
                            if new_rank in range(6, 11) and new_file in range(1, 10):
                                if move not in self._pieces or self._pieces[move].get_team() != team:
                                    potential_moves.append(move)

        elephant.set_potential_moves(potential_moves)

    def update_potential_move_sets(self):
        """This is the data used to calculate check and checkmate."""

        # Clears the previous data
        self._red_potential_moves = set()
        self._black_potential_moves = set()

        # Adds all potential moves into one set for each team.
        for piece in [self._pieces[location] for location in self._pieces]:
            if piece.get_location() != 'captured':
                if piece.get_team() == 'r':
                    for potential_move in piece.get_potential_moves():
                        self._red_potential_moves.add(potential_move)
                else:
                    for potential_move in piece.get_potential_moves():
                        self._black_potential_moves.add(potential_move)

    def flying_general(self):
        """Returns a boolean of whether there is a flying general configuration on the board or not."""

        pieces = self._pieces
        redgen = [pieces[location] for location in pieces if pieces[location].get_icon() == 'Gr'][0]
        blkgen = [pieces[location] for location in pieces if pieces[location].get_icon() == 'Gb'][0]

        # If the two generals are in the same file
        if redgen.get_location()[1] == blkgen.get_location()[1]:
            pieces_in_rank = [location[1] for location in self._pieces if location[1] == redgen.get_location()[1]]
            # If they are the only two pieces in that file
            if len(pieces_in_rank) == 2:
                return True
            else:
                return False
        else:
            return False

    def set_in_check(self):
        """Checks to see if either general's position is in the opposing team's potential moves."""

        check = False

        for piece in [self._pieces[location] for location in self._pieces]:

            if piece.get_icon() == 'Gb':
                if piece.get_location() in self._red_potential_moves:
                    self._in_check = 'b'
                    check = True

            if piece.get_icon() == 'Gr':
                if piece.get_location() in self._black_potential_moves:
                    self._in_check = 'r'
                    check = True

        # Note to self, do not remove. Undoes check if necessary.
        if not check:
            self._in_check = None
            return

    def update_winner(self):
        """Looks for checkmate, and updates the game status accordingly."""

        checkmate = True

        # This works by essentially going through every single move a team in check can make, if it finds one that
        # takes it out of check, then there is no checkmate.
        if self._in_check == 'r':
            for red_pc in [self._pieces[i] for i in self._pieces if self._pieces[i].get_team() == 'r']:
                orig_loc = tuple(red_pc.get_location())
                for move in red_pc.get_potential_moves():

                    # Makes the move
                    # updates pieces dict
                    if move in self._pieces:
                        self._pieces[move].move('captured')
                        self._pieces['captured'] = self._pieces[move]
                    red_pc.move(move)
                    self._pieces[move] = red_pc
                    del self._pieces[orig_loc]

                    # updates potential moves, and in check
                    self.update_all_moves()
                    # Accounts for if move generates flying general condition.
                    if self.flying_general():
                        self._in_check = 'r'

                    # See if move undoes check situation.
                    if self._in_check != 'r':
                        checkmate = False

                    # Undoes the move.
                    # Updates pieces dict
                    self._pieces[orig_loc] = self._pieces[move]
                    self._pieces[orig_loc].move(orig_loc)
                    del self._pieces[move]
                    if 'captured' in self._pieces:
                        self._pieces[move] = self._pieces['captured']
                        self._pieces[move].move(move)
                        del self._pieces['captured']

                    self.update_all_moves()

                    # Breaks the scan if a move takes the team out of check.
                    if not checkmate:
                        return

        elif self._in_check == 'b':
            for blk_pc in [self._pieces[i] for i in self._pieces if self._pieces[i].get_team() == 'b']:
                orig_loc = tuple(blk_pc.get_location())
                for move in blk_pc.get_potential_moves():

                    # Makes the move
                    # updates pieces dict
                    if move in self._pieces:
                        self._pieces[move].move('captured')
                        self._pieces['captured'] = self._pieces[move]
                    self._pieces[move] = self._pieces[orig_loc]
                    self._pieces[move].move(move)
                    del self._pieces[orig_loc]

                    # updates potential moves, and in check
                    self.update_all_moves()
                    if self.flying_general():
                        self._in_check = 'b'

                    # See if move undoes check situation.
                    if self._in_check != 'b':
                        checkmate = False

                    # Undoes the move.
                    # Updates pieces dict
                    self._pieces[orig_loc] = self._pieces[move]
                    self._pieces[orig_loc].move(orig_loc)
                    del self._pieces[move]
                    if 'captured' in self._pieces:
                        self._pieces[move] = self._pieces['captured']
                        self._pieces[move].move(move)
                        del self._pieces['captured']

                    self.update_all_moves()

                    if not checkmate:
                        return
        else:  # No one in check
            return

        if checkmate:
            winnahs = {'r': 'b', 'b': 'r'}
            self._winner = winnahs[self._turn]
            return

    def update_all_moves(self):
        """Updates each piece according to it's type."""
        # I decided this was nicer than a huge string of elif's.
        update_dict = {
            'S': self.update_soldier_moves,
            'G': self.update_general_moves,
            'A': self.update_advisor_moves,
            'R': self.update_chariot_moves,
            'E': self.update_elephant_moves,
            'C': self.update_cannon_moves,
            'H': self.update_horse_moves,
        }

        for piece in [self._pieces[i] for i in self._pieces]:
            if piece.get_location() != 'captured':
                pc_type = piece.get_type()
                update_dict[pc_type](piece)

        self.update_potential_move_sets()
        self.set_in_check()

    def move_piece(self, loc1, loc2):
        """Makes a legal move. Returns False otherwise."""

        if self._winner is not None:
            return False

        # If there is even a piece there
        if loc1 in self._pieces:
            piece1 = self._pieces[loc1]
        else:
            return False

        if piece1.get_team() != self._turn:
            return False

        # If the piece is allowed to move there
        if loc2 not in piece1.get_potential_moves():
            return False

        # Makes the move
        # updates pieces dict
        self.next_turn()
        if loc2 in self._pieces:
            self._pieces[loc2].move('captured')
            self._pieces['captured'] = self._pieces[loc2]

        self._pieces[loc2] = self._pieces[loc1]
        self._pieces[loc2].move(loc2)
        del self._pieces[loc1]
        # updates potential moves, and in check

        self.update_all_moves()

        # This block undoes the move and returns false if the move puts the player's own self in check.
        # It also forces them to move out of check if they are already, which I assume is the rule of the game.
        if (self._in_check != self._turn and self._in_check is not None) or self.flying_general():
            # Undoes the move.
            # Updates pieces dict
            self.next_turn()
            self._pieces[loc1] = self._pieces[loc2]
            self._pieces[loc1].move(loc1)
            del self._pieces[loc2]
            if 'captured' in self._pieces:
                self._pieces[loc2] = self._pieces['captured']
                self._pieces[loc2].move(loc2)
                del self._pieces['captured']
            self.update_all_moves()

            return False

        if 'captured' in self._pieces:
            del self._pieces['captured']

        if self._in_check is not None:
            self.update_winner()

        self.update_board()

        return True


class XiangqiGame:
    """This is how you start a new game."""

    def __init__(self):
        self._board = Board()

    def show_board(self):
        self._board.show_board()

    def get_game_state(self):
        """Returns the state of the game."""

        board_state = self._board.get_winner()
        state_convert = {'r': 'RED_WON', 'b': 'BLACK_WON', None: 'UNFINISHED'}
        return state_convert[board_state]

    def is_in_check(self, team):
        return team[0].lower() == self._board.get_in_check()

    def make_move(self, move_from, move_to):
        """To make a move. Please use coordinates like 'b4'."""

        # If the game has been won already.
        if self._board.get_winner() is not None:
            return False

        # Converts user input coordinates to coordinates friendly to the board
        try:
            letters = 'abcdefghi'
            coord_conversion = {letters[i - 1]: i for i in range(1, 10)}
            loc1 = (int(move_from[1::]), coord_conversion[move_from[0]])
            loc2 = (int(move_to[1::]), coord_conversion[move_to[0]])
        except KeyError:
            return False

        return self._board.move_piece(loc1, loc2)

