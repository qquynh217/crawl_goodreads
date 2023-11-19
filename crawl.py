from bs4 import BeautifulSoup
import requests
from crawl_selenium import getBookInfo
import csv

startPage = 1
endPage = 3

listBookUrl = "https://www.goodreads.com/list/show/1.Best_Books_Ever?page="
baseUrl = "https://www.goodreads.com"
field_names = [
    "id",
    "title",
    "link",
    "series",
    "author",
    "rating_count",
    "review_count",
    "pages",
    "score",
    "date_published",
    "first_published",
    "genre",
    "publisher",
    "isbn",
    "language",
    "awards",
    "isbn10",
    "rating",
]


def getListBookLink(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.content, "html.parser")
    response.close()
    titles = doc.find_all("a", class_="bookTitle")
    list = [item["href"] for item in titles]
    items = doc.find_all("tr")
    score = [item.find_all("a")[3].text.split(" ")[1] for item in items]
    return [list, score]


log_f = open("log.txt", "a")
error_f = open("exception.txt", "a")
for page in range(startPage, endPage):
    count = 1
    [list, scores] = getListBookLink(listBookUrl + str(page))

    fileName = "data/page-" + str(page) + ".csv"
    log_f.write(">> Page " + str(page) + "\n")
    with open(fileName, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        # for link in list:
        for i in range(len(list)):
            link = list[i]
            print(count)
            try:
                book = getBookInfo(baseUrl + link, scores[i])
                writer.writerows([book])
                log_f.write(str(count) + ". " + link + "\n")
                if book["title"] == None or book["date_published"] == None:
                    error_f.write(str(count) + ". " + link + "\n")
            except:
                error_f.write(str(count) + ". " + link + "\n")
                pass
            count += 1

        # print(fileName)
    file.close()
    print("Complete page " + str(page) + " -------")
log_f.close()
