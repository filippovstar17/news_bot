import asyncio
import os

import python_weather


async def get_weather(city):
    async with python_weather.Client(format=python_weather.METRIC) as client:
        weather = await client.get(city)

        description = weather.current.description.title()
        if description == "Sunny":
            description = "Солнечно"
        elif description == "Partly Cloudy":
            description = "Переменная облачность"
        elif description == "Cloudy":
            description = "Облачно"
        elif description == "Very Cloudy":
            description = "Очень облачно"
        elif description == "Fog" or description == "Mist":
            description = "Туман"
        elif description == "Light Showers" or description == "Light Shower":
            description = "Небольшие кратковременные ливни"
        elif description == "Light Rain":
            description = "Небольшой дождь"
        elif description == "Light Snow":
            description = "Небольшой снегопад"
        elif description == "Snow Shower":
            description = "Снегопад"
        elif description == "Heavy Snow":
            description = "Сильный снегопад"
        elif description == "Heavy Showers" or description == "Heavy Shower":
            description = "Сильные кратковременные дожди"
        elif description == "Heavy Rain":
            description = "Ливень"
        elif description == "Light Snow Showers" or description == "Light Snow Shower":
            description = "Кратковременные небольшие снегопады"
        elif description == "Light Freezing Drizzle":
            description = "Легкая изморозь"
        elif description == "Light Sleet Showers" or description == "Light Sleet Shower":
            description = "Кратковременный небольшой мокрый снег"
        elif description == "Light Sleet":
            description = "Небольшой мокрый снег"
        elif description == "Rain And Snow Shower":
            description = "Дождь со снегом"
        elif description == "Thundery Showers" or description == "Thundery Shower":
            description = "Грозовые дожди"
        elif description == "Thundery Heavy Rain":
            description = "Грозовые ливни"
        elif description == "Thundery Snow Showers" or description == "Thundery Snow Shower":
            description = "Грозовые снегопады"
        elif description == "Heavy Snow Showers" or description == "Heavy Snow Shower":
            description = "Сильные ливни со снегом"
        elif description == "Clear":
            description = "Ясно"
        elif description == "Overcast":
            description = "Пасмурно"
        else:
            pass

        return f"Погода {city}:\n" \
               f"Температура воздуха: {weather.current.temperature} °C\n" \
               f"{description} {repr(weather.current.type)}\n" \
               f"Ветер: {round(weather.current.wind_speed / 3.6, 2)} м/с"


if __name__ == "__main__":
    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print(asyncio.run(get_weather("Архангельск")))
