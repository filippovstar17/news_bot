import json

data = ""


def init():
    with open("dan.json", "r", encoding="UTF-8") as read_file:
        global data
        data = json.load(read_file)


def get_data():
    return data


def write(new_data):
    with open('dan.json', 'w', encoding="UTF-8") as outfile:
        json.dump(new_data, outfile, ensure_ascii=False, indent=4)


init()
