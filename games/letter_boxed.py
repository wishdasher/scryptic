import sys

groups = sys.argv[2].split(",")
letters = set("".join(groups))

assert len(groups) == 4 and all(len(group) == 3 for group in groups)
assert len(letters) == 12

print(groups)
print(letters)

def correct_letters(w):
    return all(letter in letters for letter in w)

def side_constraint(w):
    index = -1
    for letter in w:
        next_index = next(i for i, side in enumerate(groups) if letter in side)
        if next_index == index:
            return False
        else:
            index = next_index
    return True

with open(sys.argv[1]) as f:
    all_words = [w.strip() for w in f.readlines()]
    words = [w for w in all_words if correct_letters(w) and side_constraint(w) and len(w) > 6] # length is just a heuristic

def find_solution(w1, w2):
    if len(set("".join(w1 + w2))) == 12:
        if w1[0] == w2[-1]:
            return (w2, w1)
        elif w2[0] == w1[-1]:
            return (w1, w2)
    return None

solutions = [find_solution(w1, w2) for w1 in words for w2 in words if find_solution(w1, w2)  != None]

for sol in solutions:
    print(sol)
