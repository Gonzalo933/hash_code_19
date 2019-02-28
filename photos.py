import sys
import os.path
from enum import Enum
import copy
import numpy as np


def is_horizontal(photo):
    return photo["orientation"] == "H"


def write_file(photos_list):
    with open(sys.argv[-1] + ".out", "w") as f:
        f.write(str(len(photos_list)) + "\n")
        for photo in photos_list:
            f.write(str(photo["id"]) + "\n")


def main(file_path):
    # Read and load data from file
    photos_list = read_file(file_path)
    # Get list of tags usage
    all_tags = []
    for p in photos_list:
        all_tags += p["tags"]
    unique, counts = np.unique(all_tags, return_counts=True)
    tags_count = dict(zip(unique, counts))
    photos_without_vertical = list(filter(is_horizontal, photos_list))
    most_tags = np.argmax([len(photo["tags"]) for photo in photos_list])
    print(f"most tags={most_tags}")
    solution = branch_and_bound(photos_without_vertical.copy(), most_tags)
    write_file(solution)
    import pdb

    pdb.set_trace()


def score(photo1, photo2):
    set_1 = set(photo1["tags"])
    set_2 = set(photo2["tags"])
    num_common_tags_1_and_2 = len(set_1.intersection(set_2))
    num_set_1_not_set_2 = len(set_1 - set_2)
    num_set_2_not_set_1 = len(set_2 - set_1)
    return min(num_common_tags_1_and_2, num_set_1_not_set_2, num_set_2_not_set_1)


def branch_and_bound(photos_list, best_index):
    solution = [photos_list.pop(best_index)]
    current_score = 0
    total_photos = len(photos_list)
    while len(photos_list) > 0:
        scores = []
        for photo in photos_list:
            scores.append(score(solution[-1], photo))
        # Choose best score
        best_index = np.argmax(scores)
        current_score += np.max(scores)
        solution.append(photos_list.pop(best_index))
        print(f"Score={current_score}, Photo={len(solution)}/{(total_photos)}")
        # if len(solution) >= 500:
        #    break
    return solution


def read_photo(photo_string, i):
    return {
        "orientation": photo_string[0],
        "selected": False,
        "tags": photo_string[2:],
        "id": i,
    }


def read_file(file_path):
    # Read and load data from file
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    # First line are variables
    N = int(file_lines[0].rstrip())
    photos_list = [
        read_photo(photo_str.rstrip().split(" "), i)
        for i, photo_str in enumerate(file_lines[1:])
    ]
    assert N == len(photos_list)
    return photos_list


if __name__ == "__main__":
    assert len(sys.argv) > 1, "File name to load required as argument"
    file_path = f"{sys.argv[-1]}"
    main(file_path)
