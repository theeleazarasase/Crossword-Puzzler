""" Source header """

from crossword import Crossword
import sys

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
"\nAcross"
"\nDown"
"\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
"Invalid option/arguments. Type 'H' for help."
"Enter your guess (use _ for blanks): "
"This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")


def input(prompt=None):
    """
        DO NOT MODIFY: Uncomment this function when submitting to Codio
        or when using the run_file.py to test your code.
        This function is needed for testing in Codio to echo the input to the output
        Function to get user input from the standard input (stdin) with an optional prompt.
        Args:
            prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
        Returns:
            str: The user input received from stdin.
    """

    if prompt:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


# DEFINE YOUR FUNCTIONS
def load_crossword_puzzle():
    while True:
        filename = input(PUZZLE_PROMPT)
        try:
            puzzle = Crossword(filename)
            return puzzle
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)


def display_clues(puzzle, c):
    down_clues = []
    across_clues = []
    for key, clue in puzzle.clues.items():
        if key[2] == "A":
            across_clues.append(clue)
        if key[2] == "D":
            down_clues.append(clue)
    down_clues.sort()
    across_clues.sort()
    print("\nAcross")
    if c == 0:
        for clue in across_clues:
            print(clue)
    else:
        for i in range(c):
            try:
                print(across_clues[i])
            except IndexError:
                break
    print("\nDown")
    if c == 0:
        for clue in down_clues:
            print(clue)
    else:
        for i in range(c):
            try:
                print(down_clues[i])
            except IndexError:
                break


def commands(puzzle, user_input):
    """
    Validates user input commands for the crossword puzzle game.

    Parameters:
        crossword (Crossword): The current state of the crossword puzzle.
        user_input (str): Space-separated arguments input by the user.

    Returns:
        dict or None: A dictionary containing the valid command and its arguments, or None if the input is invalid.
    """

    user_input = user_input.split()
    if user_input[0] == "H" or user_input[0] == "S" or user_input[0] == "Q":
        if len(user_input) != 1:
            return
        else:
            return user_input[0], None

    elif user_input[0] == "C":
        try:
            if len(user_input) != 2:
                return
            if int(user_input[1]) <= 0:
                return
        except ValueError:
            return
        else:
            return user_input[0], int(user_input[1])
    elif user_input[0] == "G" or user_input[0] == "R" or user_input[0] == "T":
        try:
            if len(user_input) != 4:
                return
            if int(user_input[1]) < 0:
                return
            if int(user_input[2]) < 0:
                return

            if user_input[3] == "A" or user_input[3] == "D":
                tup = tuple((int(user_input[1]), int(user_input[2]), user_input[3]))
                if tup in puzzle.clues:
                    return str(user_input[0]), tup
            else:
                return
        except ValueError:
            return
        except IndexError:
            return


def main():
    puzzle = load_crossword_puzzle()  # Load the puzzle
    display_clues(puzzle, 0)  # Display all clues initially
    print(puzzle)  # Print the initial state of the puzzle
    print(HELP_MENU)  # Show the help menu

    while True:  # Game loop
        try:
            user_input = input("\nEnter option: ")
            user_commands = commands(puzzle, user_input)
            command = user_commands[0]

            if user_commands == None:
                print("Invalid option/arguments. Type 'H' for help.")
                continue

            if command == "C":
                try:
                    c = user_commands[1]
                    display_clues(puzzle, c)
                except TypeError:
                    print("Invalid option/arguments. Type 'H' for help.")

            elif command == "G":
                c = user_commands[1]
                clues = puzzle.clues[c]
                while True:
                    try:
                        new_guess = input('Enter your guess (use_ for blanks)')
                        new_guess = new_guess.upper()
                        puzzle.change_guess(clues, new_guess)
                        break
                    except RuntimeError as error:
                        print(error)
                print(puzzle)


            elif command == "R":
                c = user_commands[1]
                clues = puzzle.clues[c]
                puzzle.reveal_answer(clues)
                print(puzzle)

            elif command == "T":
                c = user_commands[1]
                clues = puzzle.clues[c]
                index = puzzle.find_wrong_letter(clues)
                correct = clues.answer[index]
                if index == -1:
                    print("This clue is already correct!")
                else:
                    print(f"Letter {index + 1} is wrong, it should be {correct}")

            elif command == "H":
                print(HELP_MENU)

            elif command == "Q":
                break  # Exit the game loop

            elif command == "S":
                puzzle = load_crossword_puzzle()  # Corrected function name
                display_clues(puzzle, 0)
                print(puzzle)
                print(HELP_MENU)

            if puzzle.is_solved() == True:
                print("\nPuzzle solved! Congratulations!")
                break

        except TypeError:
            print("There is typeerror")


if __name__ == '__main__':
    main()
