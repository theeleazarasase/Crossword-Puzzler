""" Source header """

import csv


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"

ACROSS = "\nAcross"
DOWN = "\nDown"
CONGRATULATIONS = "\nPuzzle solved! Congratulations!"
LETTER_WRONG = "Letter {} is wrong, it should be {}"
INVALID_OPTION = "Invalid option/arguments. Type 'H' for help."
GUESS= "Enter your guess (use _ for blanks): "
ALREADY_CORRECT = "This clue is already correct!"


RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"



class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)


    def change_guess(self, clue, new_guess):
        """
        INSERT DOCSTRING
        """
        # Check if the length of the guess matches the clue's answer length
        if len(new_guess) != len(clue.answer):
            raise RuntimeError("Error: The guess does not match the length of the answer.")

        # Check if the guess contains only valid characters
        if not all(char in GUESS_CHARS for char in new_guess.upper()):
            raise RuntimeError("Error: The guess contains invalid characters.")

        # Update the board with the new guess
        indices = clue.indices
        down_across = clue.down_across

        for i, char in enumerate(new_guess.upper()):
            if down_across == 'A':  # Update horizontally for across clues
                self.board[indices[0]][indices[1] + i] = char
            else:  # Update vertically for down clues
                self.board[indices[0] + i][indices[1]] = char

        print("Guess updated successfully.")

    def reveal_answer(self, clue):
        # Extract the necessary information from the clue
        indices = clue.indices
        down_across = clue.down_across
        answer = clue.answer

        # Iterate through each character in the answer
        for i, char in enumerate(answer.upper()):
            if down_across == 'A':  # For across clues, update horizontally
                self.board[indices[0]][indices[1] + i] = char
            else:  # For down clues, update vertically
                self.board[indices[0] + i][indices[1]] = char

        print("Answer revealed.")

    def find_wrong_letter(self, clue):

        """
        INSERT DOCSTRING
        """
        # Extract necessary information from the clue
        indices = clue.indices
        down_across = clue.down_across
        answer = clue.answer

        # Iterate through each character in the answer
        for i in range(len(answer)):
            # Determine the board position based on the clue orientation
            if down_across == 'A':
                board_char = self.board[indices[0]][indices[1] + i]
            else:  # down_across == 'D'
                board_char = self.board[indices[0] + i][indices[1]]

            # Compare the character on the board with the corresponding character in the answer
            if board_char.upper() != answer[i].upper():
                return i  # Return the index of the first discrepancy

        return -1  # If no discrepancies were found, return -1

    def is_solved(self):

        """
        INSERT DOCSTRING
        """

        # Iterate through all clues in the puzzle
        for clue_key, clue in self.clues.items():
            indices = clue.indices
            down_across = clue.down_across
            answer = clue.answer

            # Check each character of the clue's answer
            for i in range(len(answer)):
                # Determine the character on the board based on the clue orientation
                if down_across == 'A':
                    board_char = self.board[indices[0]][indices[1] + i]
                else:  # down_across == 'D'
                    board_char = self.board[indices[0] + i][indices[1]]

                # Compare the character on the board with the correct answer
                if board_char.upper() != answer[i].upper():
                    return False  # A discrepancy was found, so the puzzle is not solved

        return True  # No discrepancies were found, the puzzle is solved


