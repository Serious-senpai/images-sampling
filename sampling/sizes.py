import os
from os.path import getsize, join
from typing import Dict, List


__all__ = ("detect_similar_sizes",)


def detect_similar_sizes(directory: str) -> None:
    # A mapping of images to their sizes
    sizes: Dict[int, List[str]] = {}
    for filename in os.listdir(directory):
        location = join(directory, filename)
        size = getsize(location)
        try:
            sizes[size].append(filename)
        except KeyError:
            sizes[size] = [filename]

    for size, filenames in sizes.items():
        if len(filenames) > 1:
            print(f"Warning: {len(filenames)} images with the same size {size / 1024:.2f} KB: " + ", ".join(filenames))
