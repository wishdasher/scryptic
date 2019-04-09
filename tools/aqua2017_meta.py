# Finding potential material for puzzle writing

with open('words.txt', 'r') as f:
    words = f.readlines()

words = [x.strip().lower() for x in words]

letters_map = {}

def letters(word):
    return ''.join(sorted(word))

for word in words:
    hashed = letters(word)
    if hashed in letters_map:
        letters_map[hashed].append(word)
    else:
        letters_map[hashed] = [word]

NUMS = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'fifteen',
    'sixteen',
    'seventeen',
    'eighteen',
    'nineteen',
    'twenty',
    'thirty',
    'forty',
    'fifty',
    'sixty',
    'seventy',
    'eighty',
    'ninety',
    'hundred']

print('NOTE! Returned words may not contain desired letters in the same order')
desired = input('Enter desired letters: ')

for num in NUMS:
    combined = num + desired
    if letters(combined) in letters_map:
        print('answer! for ' + num)
        print(letters_map[letters(combined)])
