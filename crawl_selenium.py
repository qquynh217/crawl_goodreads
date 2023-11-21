from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

path = "./chromedriver.exe"


def getId(link):
    slug = link.split("show/")[1]
    id = None
    if "-" in slug:
        id = slug.split("-")[0]
    else:
        id = slug.split(".")[0]
    return id


def getElementText(driver, by, selector):
    res = None
    try:
        res = driver.find_element(by, selector).text
    except:
        pass
    return res


def getBookInfo(link, score):
    # set up driver
    service = Service(executable_path=path)
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options, service=service)
    # driver = webdriver.Chrome(service=service)
    driver.get(link)
    try:
        # get detail button
        detail_button = driver.find_element(
            By.CSS_SELECTOR,
            "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > div > button",
        )
        driver.execute_script("arguments[0].click();", detail_button)
    except:
        pass
    # get show all awards button
    try:
        awards_button = driver.find_element(
            By.CSS_SELECTOR,
            "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > span > div > div:nth-child(1) > dd > div > div.TruncatedContent__gradientOverlay > div > button",
        )
        driver.execute_script("arguments[0].click();", awards_button)
    except:
        pass
    # get show more genre
    try:
        genre_button = driver.find_element(
            By.XPATH, '//div[@data-testid="genresList"]'
        ).find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].click();", genre_button)
    except:
        pass
    book = {}
    book["link"] = link
    book["score"] = score
    # id
    book["id"] = getId(link)
    # title
    book["title"] = getElementText(driver, By.XPATH, '//h1[@data-testid="bookTitle"]')
    # author
    book["author"] = getElementText(
        driver,
        By.CSS_SELECTOR,
        "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookPageMetadataSection__contributor > h3 > div > span:nth-child(1) > a:nth-child(1) > span",
    )
    # rating count
    rating_count = getElementText(
        driver, By.XPATH, '//span[@data-testid="ratingsCount"]'
    )
    book["rating_count"] = rating_count.split(" ")[0] if rating_count != None else None
    # review_count
    review_count = getElementText(
        driver, By.XPATH, '//span[@data-testid="reviewsCount"]'
    )
    book["review_count"] = review_count.split(" ")[0] if review_count != None else None
    # pages
    pages = getElementText(driver, By.XPATH, '//p[@data-testid="pagesFormat"]')
    book["pages"] = pages.split(" ")[0] if pages != None else None
    # rating
    book["rating"] = getElementText(driver, By.CLASS_NAME, "RatingStatistics__rating")
    # first_published
    first_published = getElementText(
        driver, By.XPATH, '//p[@data-testid="publicationInfo"]'
    )
    book["first_published"] = (
        first_published.replace("First published ", "")
        if first_published != None
        else None
    )
    # genre
    listGenre = []
    try:
        listGenre = driver.find_elements(
            By.CLASS_NAME, "BookPageMetadataSection__genreButton"
        )
    except:
        pass
    book["genre"] = (
        ", ".join([item.text for item in listGenre]) if len(listGenre) > 0 else None
    )
    # series
    try:
        book["series"] = (
            driver.find_element(By.CLASS_NAME, "BookPageTitleSection__title")
            .find_element(By.TAG_NAME, "h3")
            .text
        )
    except:
        book["series"] = None
        pass
    # awards
    book["awards"] = getElementText(
        driver,
        By.CSS_SELECTOR,
        "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > span > div > div:nth-child(1) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small.TruncatedContent__text--expanded",
    )
    # get date_publised and publisher
    published = getElementText(
        driver,
        By.CSS_SELECTOR,
        "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(2) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small",
    )
    book["date_published"] = None
    book["publisher"] = None
    if published != None:
        try:
            book["date_published"] = published.split("by")[0].strip()
            book["publisher"] = published.split("by")[1].strip()
        except:
            print(published)
            pass
    # language and isbn
    try:
        edition = driver.find_element(By.CLASS_NAME, "EditionDetails").find_elements(
            By.CLASS_NAME, "DescListItem"
        )
        if len(edition) == 4:
            isbn = getElementText(
                driver,
                By.CSS_SELECTOR,
                "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(3) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small",
            )
            book["isbn"] = isbn.split(" ")[0]
            book["isbn10"] = None
            if len(isbn.split(" ")) > 2:
                book["isbn10"] = isbn.split(" ")[2].replace(")", "")

            book["language"] = getElementText(
                driver,
                By.CSS_SELECTOR,
                "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(4) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small",
            )
        else:
            book["language"] = getElementText(
                driver,
                By.CSS_SELECTOR,
                "#__next > div.PageFrame.PageFrame--siteHeaderBanner > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(3) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small",
            )
            book["isbn"] = None
            book["isbn10"] = None
    except:
        book["language"] = None
        book["isbn10"] = None
        book["isbn"] = None
        pass

    driver.quit()
    return book


print(getBookInfo("https://www.goodreads.com/book/show/206731.The_Tibetan_Book_of_Living_and_Dying",None))
