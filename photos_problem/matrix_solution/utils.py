def is_horizontal(photo):
    return photo["orientation"] == "H"


def is_vertical(photo):
    return not photo["orientation"] == "H"


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
