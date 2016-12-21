import argparse

parser = argparse.ArgumentParser(
    description="Prints words with the most anagrams, given list of words.")
parser.add_argument('input', default="", help="text file with list of line-delineated words")
parser.add_argument('threshold', default=5, help="minimum number of anagrams needed to be printed")
args = parser.parse_args()

threshold = int(args.threshold)

table = {}
with open(args.input) as file:
    words = [word.strip().lower() for word in file.readlines()]
for word in words:
    key = ''.join(sorted(word))
    table.setdefault(key, []).append(word)

for key in table:
    if len(table[key]) >= threshold:
        print(key, table[key], len(table[key]))