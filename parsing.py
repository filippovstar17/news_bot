"""
Инструкция по парсингу сайтов:
1. Заходим на вебсайт
2. F12 - network - dock
2.1. Если видим весь контент - Server site rendering - используем bs4
2.2. Если нет - Client site rendering - xhr ищем api
"""
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36 "
}


def bitcoin():
    """Получает котировки с сайта РБК Инвестиций и возвращает строку с курсом биткоина."""
    response = requests.get('https://www.rbc.ru/crypto/data/graph/166026/day/3', headers=headers)
    data = response.json()
    btc = str(format(data['result']['data'][-1][-1], '.2f'))
    response2 = requests.get('https://quote.ru/api/v1/ticker/72413', headers=headers)
    data2 = response2.json()
    usd = str(format(data2['data']['ticker']['lastPrice'], '.2f'))
    return f"Бирж. BTC: ${btc}\nБирж. BTC: ₽{str(format(float(btc)*float(usd), '.2f'))}"


def parsing_news():  # новости со ссылками
    """Получает новости с сайта Лента.ру и возвращает списки с пятью заголовками и ссылками."""
    response = requests.get('https://lenta.ru/', headers=headers)
    soap = BeautifulSoup(response.content, 'html.parser')
    titles = soap.findAll("h3", "card-mini__title")
    urls = soap.findAll("a", "card-mini _topnews")
    i = 0
    j = 0
    news_titles = []
    news_urls = []
    for data in titles:
        if i == 5:
            break
        else:
            news_titles.append(str(i + 1) + ". " + data.next)
            i += 1
    for data in urls:
        if j == 5:
            break
        else:
            if (data.attrs['href'])[:5] == "https":
                news_urls.append(f"{data.attrs['href']}")
            else:
                news_urls.append(f"https://lenta.ru{data.attrs['href']}")
            j += 1
    return news_titles, news_urls


def parsing_quotes():
    """Получает котировки с сайта РБК Инвестиций и возвращает список с курсом доллара и евро."""
    response = requests.get('https://quote.ru/api/v1/ticker/72413', headers=headers)
    data = response.json()
    usd = str(format(data['data']['ticker']['lastPrice'], '.2f'))

    response1 = requests.get('https://quote.ru/api/v1/ticker/72383', headers=headers)
    data1 = response1.json()
    eur = str(format(data1['data']['ticker']['lastPrice'], '.2f'))
    return [f"ЦБ РФ USD: ₽{usd}", f"ЦБ РФ EUR: ₽{eur}"]


def get_vk_photo_id():
    """Получает фото с альбома vk.com и выводит в консоль id фото."""
    response = requests.get('https://m.vk.com/album-184860963_00?rev=1', headers=headers)
    soap = BeautifulSoup(response.content, 'html.parser')
    info = soap.find_all("div", {"class": "PhotosPhotoItem__photo _image"})
    for item in info:
        print(f"photo{item['data-id']}")


def get_answer(termin):  # Поиск терминов
    new_termin = "+".join(termin.split())
    termin_for_wiki = "_".join(termin.split())
    response = requests.get(f"https://www.google.ru/search?q={new_termin}", headers=headers)
    soap = BeautifulSoup(response.text, "html.parser")
    text = soap.get_text("\n")
    res = text.split("\n")
    max_index = 0
    max_len = 0
    for x, item in enumerate(res):
        if item.startswith("ru.wikipedia.org"):
            index = res.index(item) + 1
            answer = res[index] + f"\nПодробнее: https://ru.wikipedia.org/wiki/{termin_for_wiki}"
            return answer
        if len(item) > max_len:
            max_len = len(item)
            max_index = x
    else:
        if res[max_index].startswith("This traffic"):
            return f"Превышено число запросов к серверу. Попробуйте позже или воспользуйтесь ссылкой ниже.\n" \
                   f"Поиск в Google: https://www.google.ru/search?q={new_termin}"
        else:
            return res[max_index] + f"\nПодробнее: https://www.google.ru/search?q={new_termin}"


if __name__ == '__main__':
    print()
