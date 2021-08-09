import os
import re
from datetime import datetime
import piexif


def format_date(date: str):
    if len(date) == 8:
        return f"{date[0:4]}/{date[4:6]}/{date[6:8]}"

    if len(date) == 15:
        return f"{date[0:4]}/{date[4:6]}/{date[6:8]} {date[9:11]}:{date[11:13]}:{date[13:15]}"


def whatsapp_matched_photo(name: str) -> datetime or None:
    if not re.match(r'^IMG(.)(([0-9]+){8})(.)WA(([0-9]+){4,})\.([a-z]+)$', name):
        return None

    pattern = re.compile(r'(([0-9]+){8})')

    string_date = pattern.search(name).group(1)
    string_date = format_date(string_date) + " 08:00:00"

    return datetime.strptime(string_date, '%Y/%m/%d %H:%M:%S')


def normal_matched_photo(name: str) -> datetime or None:
    pattern = re.compile(r'((([0-9]+){8})(.)(([0-9]+){6}))')

    if not pattern.search(name):
        return None

    string_date = pattern.search(name).group(1)
    string_date = format_date(string_date)

    return datetime.strptime(string_date, '%Y/%m/%d %H:%M:%S')


def get_date_from_filename(name: str) -> datetime:

    new_date = whatsapp_matched_photo(name)

    if new_date:
        return new_date

    new_date = normal_matched_photo(name)

    if new_date:
        return new_date


def change_photo_date_taken(file_path: str):
    exif_dict = piexif.load(file_path)

    new_date = get_date_from_filename(os.path.basename(file_path))

    if not new_date:
        print(f"File: {os.path.basename(file_path)} not modified")
        return False

    new_date_str = new_date.strftime("%Y:%m:%d %H:%M:%S")

    exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date_str
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date_str
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date_str

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_path)

    os.utime(file_path, (datetime.timestamp(new_date), datetime.timestamp(new_date)))

    print(f"File: {os.path.basename(file_path)} modified. New date: {new_date_str}")


def change_recursive(root: str):
    dir_list = os.listdir(root)

    for d in dir_list:
        file_or_dir = os.path.join(root, d)

        if os.path.isdir(file_or_dir):
            change_recursive(file_or_dir)
        else:
            change_photo_date_taken(file_or_dir)


def main(name):
    directory = 'photos'

    change_recursive(directory)


if __name__ == '__main__':
    main('PyCharm')

