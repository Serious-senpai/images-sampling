import os
import re
from os.path import getsize, join
from typing import Dict, List, Set


__all__ = (
    "remove_duplicate_pixiv_images",
    "PIXIV_PHONE_PATTERN",
    "PIXIV_DESKTOP_PATTERN",
)
PIXIV_PHONE_PATTERN = re.compile(r"illust_(\d+)_.+")
PIXIV_DESKTOP_PATTERN = re.compile(r"(\d+)_p\d.+")


def remove_duplicate_pixiv_images(directory: str) -> None:
    # A mapping of images to their Pixiv IDs
    images: Dict[str, List[str]] = {}
    for filename in os.listdir(directory):
        match = PIXIV_PHONE_PATTERN.match(filename) or PIXIV_DESKTOP_PATTERN.match(filename)
        if match is not None:
            pixiv_id = match.group(1)
            try:
                images[pixiv_id].append(filename)
            except KeyError:
                images[pixiv_id] = [filename]

    remove_count = 0
    for pixiv_id, filenames in images.items():
        if len(filenames) > 1:
            # Multiple images with the same ID

            filenames.sort()
            # Set of images' sizes in bytes
            sizes: Set[int] = set()
            for filename in filenames:
                location = join(directory, filename)
                size = getsize(location)
                if size in sizes:
                    # There has already been an image with the same size
                    os.remove(location)
                    remove_count += 1
                    print(f"Removed {filename} ({size / 1024:.2f} KB, detected ID {pixiv_id})")
                else:
                    sizes.add(size)

    print(f"Removed {remove_count} images")
