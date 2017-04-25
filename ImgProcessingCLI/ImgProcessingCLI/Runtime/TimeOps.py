

def str_time_to_seconds(str_time):
    time_snip = str_time[str_time.index(" "):]
    hour_str = time_snip[:time_snip.index(":")]
    minute_second_str = time_snip[time_snip.index(":")+1:]
    minute_str = minute_second_str[:minute_second_str.index(":")]
    second_str = minute_second_str[minute_second_str.index(minute_str) + len(minute_str) + 1:]

    total_seconds = 0
    total_seconds += int(hour_str) * 3600
    total_seconds += int(minute_str) * 60
    total_seconds += int(second_str)

    return total_seconds

def get_time_img_taken(img):
    return img._getexif()[36867]

def get_second_img_taken(img):
    return str_time_to_seconds(get_time_img_taken(img))
