import requests
from bs4 import BeautifulSoup


class Record:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        pass


class ApetitRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        self.difficulty = soup.find_all(class_="narocnost")[0]
        self.portions = soup.find_all(class_="porce")[0]
        self.time = soup.find_all(class_="priprava")[0]
        self.time.find_all("br")[0].clear()

        print(self.difficulty.get_text())
        print(self.portions.get_text())
        print(self.time.get_text())
        print()

        self.ingredients = soup.find_all(class_="ingredience-wrapper")[0].find_all("li")
        for item in self.ingredients:
            print(item.get_text())
        print()

        self.recipe = soup.find_all(class_="priprava-wrapper")[0].find_all("p")
        for item in self.recipe:
            print(item.get_text())


class VarechaRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        # print(soup.prettify())

        try:
            self.portions = soup.find_all(class_="info-number")[0]
            print(self.portions.get_text())
        except IndexError:
            pass
        try:
            self.time = soup.find_all(class_="info-number")[1]
            print(self.time.get_text())
        except IndexError:
            pass
        print()


        self.amounts = soup.find_all("table")[0].find_all(class_="recipe-ingredients__amount")
        self.ingredients = soup.find_all("table")[0].find_all(class_="recipe-ingredients__ingredient")
        for item in self.ingredients:
            item = item.find_all("a")[0]
            print(item.get_text())
        print()


        self.recipe = soup.find_all(class_="postup")[0]

        for item in self.recipe.find_all("span"):
            item = item.get_text() + ' ' + self.recipe.find_all("p")[int(item.get_text())-1].get_text()
            print(item)
        print()


def main():
    # record = ApetitRecord('https://www.apetitonline.cz/recept/smazena-mozzarella-s-pikantni-omackou')
    record = VarechaRecord("https://varecha.pravda.sk/recepty/bruschetta-s-marinovanym-lososom-a-horcicovou-penou/75893-recept.html")
    record.scrape_data()


if __name__ == '__main__':
    main()
