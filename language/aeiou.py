import argparse
import re

parser=argparse.ArgumentParser(
    description='''Does things with a list of words and vowels.''')
parser.add_argument('input', default="", help='text file with list of line-delineated words')
# parser.add_argument('option', default=0, help='which operation do you want')
args=parser.parse_args()

with open(args.input) as file:
	words = [word.strip().lower() for word in file.readlines()]

vowel_list = ['a','e','i','o','u']

def is_vowel(char):
	return char in vowel_list

def has_all_vowels(word):
	return all(vowel in word for vowel in vowel_list)

def has_any_vowels(word):
	return any(vowel in word for vowel in vowel_list)

def get_vowels(word):
	return ''.join([char for char in word if is_vowel(char)])

def in_order(word):
	if not has_all_vowels(word):
		return False
	pattern = re.compile('.*a.*e.*i.*o.*u.*')
	return pattern.match(word)

def vowel_seq_len(word):
	max_count = 0
	count = 0
	for char in word:
		if is_vowel(char):
			count += 1
			max_count = max(max_count, count)
		else:
			count = 0
	return max_count

def max_mode_vowel(word):
	key = ''.join(sorted(word))
	max_count = 0
	count = 0
	for i in range(len(key)):
		if i != 0:
			if key[i] == key[i-1]:
				count += 1
				max_count = max(max_count, count)
			else:
				count = 0
	return max_count

# prints all words with at least one of each vowel
#result = [word for word in words if has_all_vowels(word)]
# prints words that contain all of aeiou in order
#result2 = [word for word in result if in_order(word)]
# prints words that do not contain any of aeiou
#result3 = [word for word in words if not has_any_vowels(word)]
# prints words with vowel sequences of (int) or more
#result4 = [word for word in words if vowel_seq_len(word) >= 5]
# prints words with (int) or more of the same vowel
#result5 = [word for word in words if max_mode_vowel(word) >= 4]
print(result)