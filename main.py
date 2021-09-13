import os
from datetime import datetime
import piexif

from scripts.date_and_time import date_list_to_str, filename_to_datetime


def change_metadata(path, date_time):
    file_name = os.path.basename(path)

    exif_dict = piexif.load(path)

    date_time_str = date_time.strftime("%Y:%m:%d %H:%M:%S")

    exif_dict['0th'][piexif.ImageIFD.DateTime] = date_time_str
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_time_str
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_time_str

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, path)

    os.utime(path, (datetime.timestamp(date_time), datetime.timestamp(date_time)))

    print(f'Image: %-70s modified | New datetime: %s' % (file_name, date_time_str))


def visit(file_path: str):
    name = os.path.basename(file_path)
    new_date_time = filename_to_datetime(name)

    if not new_date_time:
        print(f"Image: %-70s not modified" % name)
        return False

    change_metadata(file_path, new_date_time)


def change_recursive(root: str):
    dir_list = os.listdir(root)

    for d in dir_list:
        file_or_dir = os.path.join(root, d)

        if os.path.isdir(file_or_dir):
            change_recursive(file_or_dir)
        else:
            visit(file_or_dir)


def main():
    directory = input("Insert the path to your photos: ")
    change_recursive(directory)


if __name__ == '__main__':
    main()

