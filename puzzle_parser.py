# puzzle_parser.py
# Job: turn plain-English puzzle text into a list of rules (constraints).

# Words for "third from left" style sentences
ORDINALS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
}

# Different ways a puzzle can say "next to"
NEXT_WORDS = ["next to", "beside", "adjacent", "neighbour", "neighbor"]


def clean_words(sentence):
    """Remove punctuation and return a list of words."""
    return sentence.replace(",", " ").replace(".", " ").split()


def get_names(sentence):
    """Return the names (single capital letters) in the order they appear."""
    names = []
    for word in clean_words(sentence):
        if len(word) == 1 and word.isupper():
            names.append(word)
    return names


def contains_any(text, phrase_list):
    """True if any phrase from the list appears in the text."""
    for phrase in phrase_list:
        if phrase in text:
            return True
    return False


def parse_puzzle(text):
    """
    Read the whole puzzle text.
    Returns: people (list), constraints (list), unknown (list of sentences)
    """
    # Keep only non-empty lines
    lines = []
    for line in text.split("\n"):
        if line.strip() != "":
            lines.append(line.strip())

    if len(lines) == 0:
        return [], [], []

    people = get_names(lines[0])      # first line lists the people
    total = len(people)
    constraints = []
    unknown = []

    for line in lines[1:]:
        low = line.lower()
        names = get_names(line)
        has_not = "not" in clean_words(low)
        understood = False

        # ----- Rules about TWO people -----
        if len(names) >= 2:
            first = names[0]
            second = names[1]

            if contains_any(low, NEXT_WORDS):
                if has_not:
                    constraints.append(("NOT_NEXT_TO", first, second))
                else:
                    constraints.append(("NEXT_TO", first, second))
                understood = True

            elif "immediate left of" in low and not has_not:
                constraints.append(("NEXT_TO", first, second))
                constraints.append(("LEFT_OF", first, second))
                understood = True

            elif "immediate right of" in low and not has_not:
                constraints.append(("NEXT_TO", first, second))
                constraints.append(("LEFT_OF", second, first))
                understood = True

            elif "left of" in low:
                if has_not:
                    # "A is not to the left of B" -> A is right of B
                    constraints.append(("LEFT_OF", second, first))
                else:
                    constraints.append(("LEFT_OF", first, second))
                understood = True

            elif "right of" in low:
                if has_not:
                    constraints.append(("LEFT_OF", first, second))
                else:
                    constraints.append(("LEFT_OF", second, first))
                understood = True

        # ----- Rules about ONE person -----
        if len(names) >= 1 and not understood:
            person = names[0]

            if "extreme left" in low:
                if has_not:
                    constraints.append(("NOT_AT_SEAT", person, 0))
                else:
                    constraints.append(("AT_SEAT", person, 0))
                understood = True

            elif "extreme right" in low:
                if has_not:
                    constraints.append(("NOT_AT_SEAT", person, total - 1))
                else:
                    constraints.append(("AT_SEAT", person, total - 1))
                understood = True

            else:
                # "third from left" / "second from right"
                for word in clean_words(low):
                    if word in ORDINALS:
                        number = ORDINALS[word]
                        if "from left" in low or "from the left" in low:
                            seat = number - 1
                        elif "from right" in low or "from the right" in low:
                            seat = total - number
                        else:
                            continue
                        if has_not:
                            constraints.append(("NOT_AT_SEAT", person, seat))
                        else:
                            constraints.append(("AT_SEAT", person, seat))
                        understood = True
                        break

        if not understood:
            unknown.append(line)

    return people, constraints, unknown