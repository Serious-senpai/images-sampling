import sys

import hashes
import pixiv
import sizes


try:
    directory = sys.argv[1]
except IndexError:
    directory = input("Enter images directory's location >> ")


split = "-" * 30
pixiv.remove_duplicate_pixiv_images(directory)
print(split)
sizes.detect_similar_sizes(directory)
print(split)
hashes.detect_similar_images(directory)
print(split)
