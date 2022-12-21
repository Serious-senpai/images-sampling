import itertools
import os
import time
from os.path import join
from typing import Dict, List, Optional

import imagehash
from PIL import Image

from .pixiv import PIXIV_PHONE_PATTERN, PIXIV_DESKTOP_PATTERN


def detect_similar_images(directory: str) -> None:
    # A mapping of images to their hashes
    hashes: Dict[imagehash.ImageHash, List[str]] = {}

    filenames = os.listdir(directory)

    start = time.perf_counter()
    for index, filename in enumerate(filenames):
        location = join(directory, filename)
        hash = imagehash.average_hash(Image.open(location), hash_size=256)
        try:
            hashes[hash].append(filename)
        except KeyError:
            hashes[hash] = [filename]

        if index and index % 100 == 99:
            print(f"Hashed {index + 1}/{len(filenames)} images")

    end = time.perf_counter()
    print(f"Completed hashing after {end - start:.3f} seconds")

    print("Removing images with the same hash")
    remove_count = 0

    _hashes: Dict[imagehash.ImageHash, List[str]] = {}
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

            _hashes[hash] = [protect]
        else:
            _hashes[hash] = filenames

    hashes = _hashes
    print(f"Removed {remove_count} images")

    print("Checking for slightly different images")

    # O(n^2) algorithm, maybe some improvements?
    for hash_first, hash_second in itertools.combinations(hashes.keys(), 2):
        if hash_second - hash_first <= 32:
            # Now each hash only corresponds to 1 image
            assert len(hashes[hash_first]) == len(hashes[hash_second]) == 1
            first = hashes[hash_first][0]
            second = hashes[hash_second][0]

            print(f"Possible duplicate: {first} and {second}")
