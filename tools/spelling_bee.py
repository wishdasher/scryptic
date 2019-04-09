import sys
import re

letters = sys.argv[2]

assert len(letters) == 7 and len(set(letters)) == 7

pattern = re.compile("^[" + letters + "]{4,}$")

print(pattern)

with open(sys.argv[1]) as f:
    words = [w.strip() for w in f.readlines() if pattern.match(w.strip()) and letters[0] in w and len(w.strip()) >= 4]

print("\n".join(words))
