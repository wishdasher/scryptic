import argparse
from collections import OrderedDict
import string
import pyperclip

parser = argparse.ArgumentParser(
    description="Modifies lists. Input comes from clipboard or file. Output is printed.")

parser.add_argument('-c', action='store_true', help="copy to clipboard")
parser.add_argument('-d', action='store_true', help="remove duplicates")
parser.add_argument('-l', action='store_true', help="lowercase all items")
parser.add_argument('-p', action='store_true', help="remove punctuation")
parser.add_argument('-r', action='store_true', help="reverse the list, applied after sort if applicable")
parser.add_argument('-s', action='store_true', help="sort the list alphabetically")
parser.add_argument('-u', action='store_true', help="uppercase all items")
parser.add_argument('-w', action='store_true', help="remove whitespace")
parser.add_argument('-x', action='store_true', help="clean, same as removing punctuation and whitespace")

parser.add_argument('-i', '--input', help="specify an input text file")

args = parser.parse_args()

if args.x:
    args.p = True
    args.w = True
if args.l and args.u:
    raise Exception("Cannot set both lowercase and uppercase flags")

# get contents
if args.input:
    with open(args.input) as file:
        content = file.readlines()
else:
    try:
        content = pyperclip.paste()
    except:
        raise Exception("Nothing found on clipboard")

items =  content.split('\n')

# options that modify items in the list
if args.p:
    translator = str.maketrans({key: None for key in string.punctuation})
    items = [s.translate(translator) for s in items]

if args.w:
    items = [s.strip() for s in items]

if args.l:
    items = [s.lower() for s in items]

if args.u:
    items = [s.upper() for s in items]

items = list(filter(bool, items)) # remove empty strings

# options that delete items from the list
if args.d:
    items = list(OrderedDict.fromkeys(items))

# options that change the order of items in the list
if args.s:
    items.sort()

if args.r:
    items.reverse()

# output options
if args.c:
    pyperclip.copy('\n'.join(items))

for item in items:
    print(item)
