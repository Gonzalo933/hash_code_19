import sys
import numpy as np
import pdb
import itertools


def main(in_file, out_file):
    # Photos list is a list of dictionaries
    photos_list = read_input_file(in_file)
    # submission is a list of list of ids for every slide.
    # In each slide there can be either one or two ids
    submission = read_output_file(photos_list, out_file)

    # check no duplicate ids
    submitted_ids = []
    score = 0
    for slide_pair in pairwise(submission):
        if slide_pair[1] is None:
            break
        # Group all slides in groups of two
        # Then check if in each of those slides there are two vertical pictures and convert them
        # to a single horizontal one
        photo_1 = get_photos_from_id_list(photos_list, slide_pair[0])
        photo_2 = get_photos_from_id_list(photos_list, slide_pair[1])
        score += calculate_score(photo_1, photo_2)
        for photo_id in slide_pair[0]:
            if photo_id in submitted_ids:
                raise Exception(f"Using a duplicate id {photo_id}")
        submitted_ids += slide_pair[0]
    print(f"Score: {score}")


def get_photos_from_id_list(photos_list, photo_id):
    if len(photo_id) == 2:
        return convert_vertical_to_horizontal(
            photos_list[photo_id[0]], photos_list[photo_id[1]]
        )
    else:
        return photos_list[photo_id[0]]


def pairwise(iterable):
    # To iterate in groups of two
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def convert_vertical_to_horizontal(vertical_1, vertical_2):
    # Creates a horizontal pic from two verticals
    if vertical_1["orientation"] == "H" or vertical_2["orientation"] == "H":
        raise Exception("Cannot create a horizontal picture from horizontal pictures")
    if vertical_1["id"] == vertical_2["id"]:
        raise Exception("Using twice the same vertical to create a horizontal")
    return {
        "orientation": "H",
        "tags": vertical_1["tags"] + vertical_2["tags"],
        "id": [vertical_1["id"], vertical_2["id"]],
    }


def create_photo_from_str(photo_string, i):
    return {"orientation": photo_string[0], "tags": photo_string[2:], "id": i}


def read_input_file(file_path):
    # Read and load data from file
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    # First line are variables
    N = int(file_lines[0].rstrip())
    photos_list = [
        create_photo_from_str(photo_str.rstrip().split(" "), i)
        for i, photo_str in enumerate(file_lines[1:])
    ]
    assert N == len(photos_list)
    return photos_list


def read_output_file(photos_list, file_path):
    # Read and load data from file
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    # First line are the number of lines in the file
    N = int(file_lines[0].rstrip())
    submission = [
        read_line_output_file(photos_list, line, line_num + 2)
        for line_num, line in enumerate(file_lines[1:])
    ]
    if len(submission) != N:
        raise Exception(
            f"The number of lines in the first line  doesn't much the number of lines in the submission"
        )
    return submission


def read_line_output_file(photos_list, line, line_num):
    ids_list = list(map(int, line.rstrip().split(" ")))
    if len(ids_list) == 1 and photos_list[ids_list[0]]["orientation"] == "V":
        raise Exception(
            f"Vertical photos must be used in pairs. Found single vertical photo at line {line_num} -> {line}"
        )
    elif len(ids_list) == 2:
        if not is_vertical(photos_list[ids_list[0]]) or not is_vertical(
            photos_list[ids_list[1]]
        ):
            raise Exception(
                f"There are two pictures in a slide that are not both vertical. Line {line_num} -> {line}"
            )
    elif len(ids_list) > 2:
        raise Exception(
            "There is a slide with more than two pictures Line {line_num} -> {line}"
        )

    return ids_list


def is_horizontal(photo):
    return photo["orientation"] == "H"


def is_vertical(photo):
    return photo["orientation"] == "V"


def calculate_score(photo1, photo2):
    set_1 = set(photo1["tags"])
    set_2 = set(photo2["tags"])
    num_common_tags_1_and_2 = len(set_1.intersection(set_2))
    num_set_1_not_set_2 = len(set_1 - set_2)
    num_set_2_not_set_1 = len(set_2 - set_1)
    return min(num_common_tags_1_and_2, num_set_1_not_set_2, num_set_2_not_set_1)


if __name__ == "__main__":
    assert (
        len(sys.argv) > 2
    ), "File name to load required as argument and out file as second argument"
    in_file = f"{sys.argv[-2]}"
    out_file = f"{sys.argv[-1]}"
    main(in_file, out_file)
