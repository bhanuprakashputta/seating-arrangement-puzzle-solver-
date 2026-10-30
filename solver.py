# solver.py
# Job: try every seating using backtracking and keep the ones that obey all rules.


def find_seat(arrangement, name):
    """Return the seat number of a person, or None if not seated yet."""
    for seat in range(len(arrangement)):
        if arrangement[seat] == name:
            return seat
    return None


def are_neighbours(seat_a, seat_b, total, circular):
    """True if two seats are next to each other."""
    gap = abs(seat_a - seat_b)
    if gap == 1:
        return True
    if circular and gap == total - 1:      # first and last seat touch in a circle
        return True
    return False


def is_valid(arrangement, constraints, circular):
    """Check the CURRENT (maybe partly filled) seating against every rule."""
    total = len(arrangement)

    for rule in constraints:
        kind = rule[0]
        seat_a = find_seat(arrangement, rule[1])

        # Rules with a person and a seat number
        if kind == "AT_SEAT":
            if seat_a is not None and seat_a != rule[2]:
                return False
            continue
        if kind == "NOT_AT_SEAT":
            if seat_a is not None and seat_a == rule[2]:
                return False
            continue

        # Rules with two people
        seat_b = find_seat(arrangement, rule[2])
        if seat_a is None or seat_b is None:
            continue                         # not both seated yet, skip for now

        if kind == "NEXT_TO":
            if not are_neighbours(seat_a, seat_b, total, circular):
                return False
        elif kind == "NOT_NEXT_TO":
            if are_neighbours(seat_a, seat_b, total, circular):
                return False
        elif kind == "LEFT_OF":
            if seat_a > seat_b:
                return False

    return True


def place_next(arrangement, people, constraints, solutions, seat, circular):
    """Backtracking: fill seat number 'seat', then move on to the next one."""
    # Base case: every seat is filled
    if seat == len(people):
        solutions.append(arrangement.copy())
        return

    for person in people:
        if person in arrangement:
            continue                          # already seated
        arrangement[seat] = person            # 1. place
        if is_valid(arrangement, constraints, circular):
            place_next(arrangement, people, constraints, solutions, seat + 1, circular)  # 2. go deeper
        arrangement[seat] = None              # 3. undo


def solve_puzzle(people, constraints, circular=False):
    """Start the search and return the list of all valid seatings."""
    arrangement = [None] * len(people)
    solutions = []

    if circular:
        # Fix the first person at seat 0 so rotations are not counted as new answers
        arrangement[0] = people[0]
        if is_valid(arrangement, constraints, circular):
            place_next(arrangement, people, constraints, solutions, 1, circular)
    else:
        place_next(arrangement, people, constraints, solutions, 0, circular)

    return solutions