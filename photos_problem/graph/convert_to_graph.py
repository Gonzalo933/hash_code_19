import utils
import sys
import pdb
from functools import partial
from multiprocessing import Pool, current_process
import time
import tqdm


def main(file_path):
    # Read and load data from file
    photos_list = utils.read_file(file_path)
    horizontal_photos = list(filter(utils.is_horizontal, photos_list))
    # For debug
    # horizontal_photos = horizontal_photos[0:1000]

    N = len(horizontal_photos)
    # Using mixed format: https://gephi.org/users/supported-graph-formats/csv-format/
    lines_to_write = []
    do_work = partial(process_photo, photos_list=horizontal_photos)
    with Pool(processes=4) as p:
        # p.map(do_work, horizontal_photos)
        for res in tqdm.tqdm(
            p.imap_unordered(do_work, horizontal_photos), total=len(horizontal_photos)
        ):
            lines_to_write.append(res)
    # Write to file
    write_graph(lines_to_write)
    pdb.set_trace()


def write_graph(lines_to_write):
    with open(sys.argv[-1] + ".csv", "w") as f:
        for line in lines_to_write:
            if len(line) == 1:
                continue
            # Convert our list of ids to a string with the ids separated by commas
            str_line = ",".join(str(x) for x in line)
            f.write(str_line + "\n")


def process_photo(photo, photos_list):
    # Remove photo itself from photo_connected_to
    photos_without_current = photos_list.copy()
    photos_without_current.remove(photo)
    ids_connected = [photo["id"]]
    for tag in photo["tags"]:
        photo_connected_to = photos_that_have_tag(photos_without_current, tag)
        ids_connected += [p["id"] for p in photo_connected_to]
    # print(f"Progress: {photo['id'] / len(photos_list):.2f}%")
    return ids_connected
    # lines_to_write += ids_connected


def photos_that_have_tag(photos_list, tag):
    photo_has_tag_partial_func = partial(photo_has_tag, tag=tag)
    photos_with_given_tag = list(filter(photo_has_tag_partial_func, photos_list))
    return photos_with_given_tag


def photo_has_tag(photo, tag):
    return tag in photo["tags"]


if __name__ == "__main__":
    assert len(sys.argv) > 1, "File name to load required as argument"
    file_path = f"../datasets/{sys.argv[-1]}"
    main(file_path)
