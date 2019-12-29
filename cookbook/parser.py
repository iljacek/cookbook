import requests
from bs4 import BeautifulSoup
import re


class Record:
    def __init__(self, url):
        self.url = url
        self.record = {}

    def scrape_data(self):
        pass

    def print_data(self):

        print(self.record)



class ApetitRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        # print(soup.prettify())

        self.record["difficulty"] = soup.find_all(class_="narocnost")[0].get_text().split(": ")[1]

        portions = soup.find_all(class_="porce")[0].get_text().split()
        self.record["portions"] = ' '.join(portions[2:])

        time = soup.find_all(class_="priprava")[0]
        time.find_all("br")[0].clear()
        self.record["time"] = time.get_text().split(": ")[1].rstrip()

        ingredients = soup.find_all(class_="ingredience-wrapper")[0].find_all(["ul", "p"])
        # print(ingredients[2].find_next_sibling())

        dict = {}
        itemlist = ingredients[1].find_all("li")
        dict["general"] = list(map(lambda item: item.get_text(), itemlist))
        for i, j in zip(ingredients[2::2], ingredients[3::2]):
            itemlist = j.find_all("li")
            dict[i.get_text()] = list(map(lambda item: item.get_text(), itemlist))

        self.record["ingredients"] = {}
        for key, value in dict.items():
            search = list((map(lambda item: re.search(r"^((?:špetka)?[0-9/–-]*(?:\s?[mcdk]?[gl])?)\s?(.*)", item), value)))
            amounts = list((map(lambda item: item.group(1), search)))
            value = list((map(lambda item: item.group(2), search)))
            self.record["ingredients"][key] = [{key: value} for key, value in zip(value, amounts)]

        recipe = soup.find_all(class_="priprava-wrapper")[0].find_all("p")
        section = [item.find_all("strong")[0].get_text() for item in recipe]
        [item.find_all("strong")[0].clear() for item in recipe]
        recipe = [item.get_text() for item in recipe]

        self.record["recipe"] = [{key: value.replace(u'\xa0', u' ')} for key, value in zip(section, recipe) if value != '']


class VarechaRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        # print(soup.prettify())

        try:
            self.record["portions"] = soup.find_all(class_="info-number")[0].get_text()
        except IndexError:
            pass
        try:
            self.record["time"] = soup.find_all(class_="info-number")[1].get_text()
        except IndexError:
            pass

        # get list with amounts
        amounts = soup.find_all("table")[0].find_all(class_="recipe-ingredients__amount")
        amounts = [item for item in map(lambda item: item.get_text(), amounts)]

        # list with ingredients
        ingredients = soup.find_all("table")[0].find_all(class_="recipe-ingredients__ingredient")
        ingredients = [item for item in map(lambda item: item.find_all("a")[0].get_text(), ingredients)]

        # fill ingredient group
        self.record["ingredients"] = {}
        self.record["ingredients"]["general"] = [{key: value.replace(u'\xa0', u' ')} for key, value in zip(ingredients, amounts)]


        recipe = soup.find_all(class_="postup")[0].find_all(["span", "p"])
        recipe = [item for item in map(lambda item: item.get_text(), recipe)]
        self.record["recipe"] = [{key: value.replace(u'\r\n', u' ')} for key, value in zip(recipe[::2], recipe[1::2])]


def main():
    # record = ApetitRecord('https://www.apetitonline.cz/recept/chrestovy-quiche')
    record = VarechaRecord("https://varecha.pravda.sk/recepty/bruschetta-s-marinovanym-lososom-a-horcicovou-penou/75893-recept.html")
    record.scrape_data()
    record.print_data()


if __name__ == '__main__':
    main()
