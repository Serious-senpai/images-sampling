import os
import time
from os.path import join
from typing import Dict, List, Optional

import imagehash
from PIL import Image

from pixiv import PIXIV_PHONE_PATTERN, PIXIV_DESKTOP_PATTERN


def detect_similar_images(directory: str) -> None:
    # A mapping of images to their hashes
    hashes: Dict[str, List[str]] = {}

    filenames = os.listdir(directory)

    start = time.perf_counter()
    for index, filename in enumerate(filenames):
        location = join(directory, filename)
        hash = imagehash.average_hash(Image.open(location), hash_size=512)
        try:
            hashes[hash].append(filename)
        except KeyError:
            hashes[hash] = [filename]

        if index and index % 100 == 99:
            print(f"Completed hashing {index + 1} images")

    end = time.perf_counter()
    print(f"Completed hashing after {end - start:.3f} seconds")

    remove_count = 0
    for hash, filenames in hashes.items():
        if len(filenames) > 1:
            protect: Optional[int] = None
            for index, filename in enumerate(filenames):
                if PIXIV_DESKTOP_PATTERN.match(filename):
                    protect = index
                elif PIXIV_PHONE_PATTERN.match(filename) and protect is None:
                    protect = index

            if protect is None:
                protect = 0

            for index, filename in enumerate(filenames):
                if index == protect:
                    continue

                location = join(directory, filename)
                os.remove(location)
                print(f"Removed {filename} - duplicate in " + ", ".join(filenames))
                remove_count += 1

    print(f"Removed {remove_count} images")
