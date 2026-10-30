# main.py
# Job: connect everything. Run this file:  python main.py

from puzzle_parser import parse_puzzle
from solver import solve_puzzle
from display import show_rules, show_solutions

EXAMPLE = """Five friends A, B, C, D, E sit in a row facing north.
A sits at the extreme left.
B sits next to A.
C does not sit next to B.
D sits to the left of E.
E sits at the extreme right."""


def type_puzzle():
    """Let the user type a puzzle. An empty line ends the input."""
    print("Type your puzzle. First line = the people. Then one rule per line.")
    print("Press Enter on an empty line when finished.\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def load_from_file():
    """Read the puzzle from a text file."""
    name = input("File name (example: puzzle.txt): ").strip()
    try:
        file = open(name, "r", encoding="utf-8")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print("File not found:", name)
        return ""


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please type y or n.")


def main():
    print("=== SEATING ARRANGEMENT PUZZLE SOLVER ===")
    print("1. Type a puzzle")
    print("2. Load a puzzle from a file")
    print("3. Run the built-in example")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        text = type_puzzle()
    elif choice == "2":
        text = load_from_file()
    else:
        text = EXAMPLE
        print("\n" + EXAMPLE)

    people, constraints, unknown = parse_puzzle(text)

    if len(people) == 0:
        print("No people found. The first line must list names like: A, B, C, D")
        return

    circular = ask_yes_no("\nIs the table circular?")

    # In a circle, left/right and fixed seat numbers have no meaning
    if circular:
        kept = []
        for rule in constraints:
            if rule[0] in ("NEXT_TO", "NOT_NEXT_TO"):
                kept.append(rule)
            else:
                print("Ignoring (not valid for a circle):", rule)
        constraints = kept

    show_rules(people, constraints, unknown)

    # Safety step: let the user confirm the rules
    if not ask_yes_no("\nAre these rules correct? Solve now?"):
        print("Okay. Fix your puzzle text and run again.")
        return

    solutions = solve_puzzle(people, constraints, circular)
    show_solutions(solutions, circular)


main()