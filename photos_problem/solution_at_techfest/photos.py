import sys
import os.path
from enum import Enum
import copy
import numpy as np


def is_horizontal(photo):
    return photo["orientation"] == "H"


def is_vertical(photo):
    return not photo["orientation"] == "H"


def write_file(photos_list):
    with open(sys.argv[-1] + ".out", "w") as f:
        f.write(str(len(photos_list)) + "\n")
        for photo in photos_list:
            if type(photo["id"]) == list:
                for id in photo["id"]:
                    f.write(str(id) + " ")
                f.write("\n")
            else:
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
    horizontal_photos = list(filter(is_horizontal, photos_list))
    vertical_photos = list(filter(is_vertical, photos_list))
    if not len(vertical_photos) % 2:
        vertical_photos = vertical_photos[1:]
    new_horizontals = merge_vertical_photos(vertical_photos.copy(), 0)
    photos_list = horizontal_photos + new_horizontals
    grouped_photos = []
    group_size = 100
    for i in range(0, len(photos_list), group_size):
        grouped_photos.append(photos_list[i : i + group_size])
    final_solution = []
    current_score = 0
    group_num = 0
    for group in grouped_photos:
        most_tags = np.argmax([len(photo["tags"]) for photo in group])
        solution, solution_score = branch_and_bound(group.copy(), most_tags)
        final_solution += solution
        current_score += solution_score
        group_num += 1
        print(f"group={group_num}/{len(grouped_photos)}")
        print(f"Solution score {current_score}")
    print(f"most tags={most_tags}")
    write_file(final_solution)
    import pdb

    pdb.set_trace()


def merge_vertical_photos(vertical_photos, best_index):
    solution = []
    flag = True
    while len(vertical_photos) > 0:
        scores = []
        vertical_first = vertical_photos.pop(best_index)
        flag = True
        for index, photo in enumerate(vertical_photos):
            current_score = score(vertical_first, photo)
            if current_score == 0:
                # MERGE
                solution.append(merge_photos(vertical_first, photo))
                vertical_photos.pop(index)
                best_index = 0
                flag = False
                break
            scores.append(current_score)
        # Choose best score
        if flag and len(vertical_photos) > 0:
            best_index = np.argmin(scores)
            solution.append(merge_photos(vertical_first, photo))
            vertical_photos.pop(best_index)
            best_index = 0
        # print(f"Score={current_score}, Photo={len(solution)}/{(total_photos)}")
    return solution


def merge_photos(photo_1, photo_2):
    return {
        "tags": photo_1["tags"] + list(set(photo_2["tags"]) - set(photo_1["tags"])),
        "id": [photo_1["id"], photo_2["id"]],
        "orientation": "H",
    }


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
        # print(f"Score={current_score}, Photo={len(solution)}/{(total_photos)}")
        # if len(solution) >= 500:
        #    break
    return solution, current_score


def read_photo(photo_string, i):
    return {"orientation": photo_string[0], "tags": photo_string[2:], "id": i}


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
