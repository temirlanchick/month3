import requests
from parsel import Selector
from pprint import pprint
MAIN_URL = "https://www.house.kg/snyat"


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error")


def get_title(selector):
    title = selector.css("title::text").get()
    return title


if __name__ == "__main__":
    html = get_html(f"{MAIN_URL}/search/all")
    selector = Selector(html)
    print(get_title(selector))
    house = selector.css("div.table-view-list div.list-item")