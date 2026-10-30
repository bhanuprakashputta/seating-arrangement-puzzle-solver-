# display.py
# Job: show rules and answers in a friendly way.


def rule_to_text(rule):
    """Turn a rule tuple into a readable sentence."""
    kind = rule[0]
    if kind == "NEXT_TO":
        return rule[1] + " sits next to " + rule[2]
    if kind == "NOT_NEXT_TO":
        return rule[1] + " does NOT sit next to " + rule[2]
    if kind == "LEFT_OF":
        return rule[1] + " sits somewhere to the left of " + rule[2]
    if kind == "AT_SEAT":
        return rule[1] + " sits at seat " + str(rule[2] + 1)
    if kind == "NOT_AT_SEAT":
        return rule[1] + " does NOT sit at seat " + str(rule[2] + 1)
    return str(rule)


def show_rules(people, constraints, unknown):
    print("\nPeople:", ", ".join(people))
    print("\nRules I understood:")
    for number, rule in enumerate(constraints, start=1):
        print("  " + str(number) + ". " + rule_to_text(rule))

    if len(unknown) > 0:
        print("\n!! I could NOT understand these sentences:")
        for sentence in unknown:
            print("   - " + sentence)


def show_solutions(solutions, circular):
    print("\n" + "=" * 40)
    if len(solutions) == 0:
        print("No valid arrangement exists.")
        print("Tip: a rule may have been misread. Check the rules list above.")
        return

    print("Number of solutions:", len(solutions))
    print("=" * 40)

    for number, solution in enumerate(solutions, start=1):
        print("\nSolution " + str(number) + ":")
        print("  Seat   : " + "  ".join(str(i + 1) for i in range(len(solution))))
        print("  Person : " + "  ".join(solution))
        if circular:
            print("  (circle: last seat is next to the first seat)")

    # If more than one solution, show what is the SAME in all of them
    if len(solutions) > 1:
        print("\nFacts true in ALL solutions:")
        found_any = False
        for seat in range(len(solutions[0])):
            same = True
            for solution in solutions:
                if solution[seat] != solutions[0][seat]:
                    same = False
            if same:
                print("  Seat " + str(seat + 1) + " is always " + solutions[0][seat])
                found_any = True
        if not found_any:
            print("  (none)")