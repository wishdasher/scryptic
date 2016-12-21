import argparse
import os
import urllib2
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    description="Downloads manga images from mangareader.net")
parser.add_argument('-o', '--output', default='manga', help="output destination folder")
args = parser.parse_args()

name = raw_input("Enter manga name: ")
name_clean = name.strip().lower().replace(' ', '-')
chapter = raw_input("Enter chapter number: ")
dest_dir = name_clean + os.path.sep + chapter

dest_dir = os.path.join(args.output, dest_dir)

print("The destination directory is: " + dest_dir)

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

page = 1

while True:
    url = "http://www.mangareader.net/" + name_clean + "/" + chapter + "/" + str(page)
    # print("Retrieving from url: " + url)
    try:
        html = urllib2.urlopen(url)
    except:
        print("Page at " + url + " not found, exiting")
        break

    soup = BeautifulSoup(html.read())
    if len(soup.find_all('img')) == 0:
        print("No images found for url: " + url)
        break

    for tag in soup.find_all('img'):
        # assuming one image in source code
        source = tag.get('src')
        print("Retrieving source image: " + source)

    page_name = 'page' + str(page) + os.path.splitext(source)[1]
    dest = os.path.join(dest_dir, page_name)
    req = urllib2.Request(source)
    req.add_header('User-agent', 'Mozilla 5.10')
    file = urllib2.urlopen(req)

    with open(dest, 'wb') as output:
        output.write(file.read())

    file.close()

    page += 1
