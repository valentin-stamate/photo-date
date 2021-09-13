from datetime import datetime
import re

date_matched_1 = re.compile(r'([0-9]{4})([0-9]{2})([0-9]{2})')  # e.g. 20210518
date_matched_2 = re.compile(r'([0-9]{4})([^0-9])([0-9]{2})([^0-9])([0-9]{2})')  # e.g. 2012.06.13

time_matched_1 = re.compile(r'([0-9]{2})([0-9]{2})([0-9]{2})')  # e.g. 175604
time_matched_2 = re.compile(r'([0-9]{2})([^0-9])([0-9]{2})([^0-9])([0-9]{2})')  # e.g. 17.06.32

date_regex_list = [date_matched_1, date_matched_2]
time_regex_list = [time_matched_1, time_matched_2]


def list_to_str(lis):
    list_str = ''

    for el in lis:
        list_str += el

    return list_str


def date_list_to_str(buckets: ()) -> str:
    if len(buckets) == 5:
        return f"{buckets[0]}/{buckets[2]}/{buckets[4]}"

    if len(buckets) == 3:
        return f"{buckets[0]}/{buckets[1]}/{buckets[2]}"
    else:
        print("List length error")


def time_list_to_str(buckets) -> str:
    if len(buckets) == 5:
        return f"{buckets[0]}:{buckets[2]}:{buckets[4]}"

    if len(buckets) == 3:
        return f"{buckets[0]}:{buckets[1]}:{buckets[2]}"
    else:
        print("List length error")


def filename_to_datetime(name: str) -> datetime or None:
    name_copy = name
    date, time = None, '08:00:00'

    # date
    for time_regex in date_regex_list:
        found_list = time_regex.findall(name)

        if len(found_list) == 0:
            continue

        name = name.replace(list_to_str(found_list[0]), '')
        date = date_list_to_str(found_list[0])
        break

    # time
    for date_regex in time_regex_list:
        found_list = date_regex.findall(name)

        if len(found_list) == 0:
            continue

        time = time_list_to_str(found_list[-1])
        break

    if date is None:
        return None

    try:
        return datetime.strptime(f"{date} {time}", '%Y/%m/%d %H:%M:%S')
    except:
        print(f"Invalid date format for {name_copy}. Date extracted: {date} {time}")
        return None


# TESTING
if __name__ == '__main__':
    pattern = 'WhatsApp Image 2021-09-13 at 12.06.17'
    print(filename_to_datetime(pattern))
