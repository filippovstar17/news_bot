import json
import sys
import time
from datetime import datetime, timedelta

import config


def update():
    with open("dan.json", "r") as read_file:
        global day, month, year
        data = json.load(read_file)
        day = int(data["users"][config.BASE_ID]["dmb"]["day"])
        month = int(data["users"][config.BASE_ID]["dmb"]["month"])
        year = int(data["users"][config.BASE_ID]["dmb"]["year"])
        return day, month, year


day, month, year = update()


def dmb():
    first = str(round(((((datetime.now() - datetime(year, month, day)).total_seconds())
                        / timedelta(days=364).total_seconds()) * 100), 6))

    if float(first) <= 100:
        second = "Прошло: " + str(datetime.now() - datetime(year, month, day))[:-7]
        third = "Осталось: " + str(timedelta(days=364) - (datetime.now() - datetime(year, month, day)))[:-7]
    else:
        first = 100
        second = "Прошло после дембеля: "
        third = str((datetime.now() - datetime(year, month, day) - timedelta(days=364)))[:-7]

    return f"{first}%\n{second}\n{third}"


if __name__ == "__main__":
    while True:
        try:
            print(dmb())
            time.sleep(1)

        except KeyboardInterrupt:
            sys.exit()
