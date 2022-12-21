import sys

from .hashes import detect_similar_images
from .pixiv import remove_duplicate_pixiv_images
from .sizes import detect_similar_sizes


try:
    directory = sys.argv[1]
except IndexError:
    directory = input("Enter images directory's location >> ")


split = "-" * 30
remove_duplicate_pixiv_images(directory)
print(split)
detect_similar_sizes(directory)
print(split)
detect_similar_images(directory)
print(split)
