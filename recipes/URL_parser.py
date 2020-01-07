import requests
import json
from bs4 import BeautifulSoup
import re


class Record:
    def __init__(self, url):
        self.url = url
        self.record = {}

    def scrape_data(self):
        pass

    def print_data(self):

        print(json.dumps(self.record, indent=4, sort_keys=True, ensure_ascii=False))


class ApetitRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        # print(soup.prettify())

        self.record["name"] = soup.find_all(class_="title")[0].get_text()
        self.record["image"] = soup.find_all(class_="novinka-img")[0].find_all("img")[0].attrs['src']

        try:
            self.record["difficulty"] = soup.find_all(class_="narocnost")[0].get_text().split(": ")[1]
        except IndexError:
            pass
        try:
            portions = soup.find_all(class_="porce")[0].get_text().split()
            self.record["portions"] = ' '.join(portions[2:])
        except IndexError:
            pass
        try:
            time = soup.find_all(class_="priprava")[0]
            time.find_all("br")[0].clear()
            self.record["time"] = time.get_text().split(": ")[1].rstrip()
        except IndexError:
            pass

        ingredients = soup.find_all(class_="ingredience-wrapper")[0].find_all(["ul", "p"])
        # print(ingredients[2].find_next_sibling())

        dict = {}
        if ingredients[1].contents[0].name != "strong":
            group = "general"

        for item in ingredients[1:]:
            if item.contents[0].name == "strong":
                group = item.contents[0].contents[0]
            else:
                itemlist = item.find_all("li")
                dict[group] = list(map(lambda item: item.get_text(), itemlist))

        self.record["ingredients"] = {}
        for key, value in dict.items():
            search = list((map(lambda item:re.search(r"^([0-9/–,.-]*(?:\s?[mcdk]?[gl]\s)?\s?"
                                                     r"(?:malá)?(?:malé)?(?:velká)?(?:velké)?"
                                                     r"(?:menších)?(?:větších)?(?:menší)?(?:větší)?\s?"
                                                     r"(?:stroužek)?(?:stroužky)?(?:hrst)?(?:špetka)?(?:lžíce)?"
                                                     r"(?:lžička)?(?:lžičky)?(?:lžic)?(?:hrnek)?(?:hrnky)?(?:snítky)?"
                                                     r"(?:plátky)?)\s*(.*)"
                                                     , item), value)))
            amounts = list((map(lambda item: item.group(1).strip(), search)))
            value = list((map(lambda item: item.group(2), search)))
            self.record["ingredients"][key] = {key: value for key, value in zip(value, amounts)}

        recipe = soup.find_all(class_="priprava-wrapper")[0].find_all("p")
        section = [item.find_all("strong")[0].get_text() for item in recipe if item.next.name == "strong"]
        [item.find_all("strong")[0].clear() for item in recipe if item.next.name == "strong"]
        recipe = [item.get_text() for item in recipe]

        self.record["recipe"] = {key: value.replace(u'\xa0', u' ') for key, value in zip(section, recipe) if value != ''}


class VarechaRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        print(soup.prettify())

        self.record["name"] = soup.find_all(class_="intro")[0].find_all("h1")[0].get_text()
        image = soup.find_all(class_="recipe-photo")[0].find_all("img")[0].attrs['src']
        self.record["image"] = "https://varecha.pravda.sk" + image

        try:
            self.record["portions"] = soup.find_all(class_="info-number")[0].get_text()
        except IndexError:
            pass
        try:
            self.record["time"] = soup.find_all(class_="info-number")[1].get_text()
        except IndexError:
            pass

        self.record["ingredients"] = {}
        table_content = soup.find_all("table")[0].find_all(class_=["recipe-ingredients__group", "recipe-ingredients__amount",
                                               "recipe-ingredients__ingredient"])

        group = "general"
        if table_content[0].attrs["class"][0] != 'recipe-ingredients__group':
            self.record["ingredients"][group] = {}

        amount = ''
        for item in table_content:
            if item.attrs["class"][0] == 'recipe-ingredients__group':
                group = item.get_text()
                self.record["ingredients"][group] = {}
                continue
            elif item.attrs["class"][0] == 'recipe-ingredients__amount':
                amount = item.get_text().replace(u'\xa0', u' ')
            else:
                ingredient = item.find_all("a")[0].get_text()
                self.record["ingredients"][group][ingredient] = amount

        recipe = soup.find_all(class_="postup")[0].find_all(["span", "p"])
        recipe = [item for item in map(lambda item: item.get_text(), recipe)]
        self.record["recipe"] = {key: value.replace(u'\r\n', u' ') for key, value in zip(recipe[::2], recipe[1::2])}


class DobruchutRecord(Record):

    def scrape_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, features="html.parser")

        # print(soup.prettify())

        self.record["name"] = soup.find_all(class_="recipe-body")[0].find_all("h1")[0].get_text()
        self.record["image"] = soup.find_all(class_="main-image")[0].find_all("img")[1].attrs['src']

        try:
            self.record["difficulty"] = soup.find_all(class_="difficulty")[0].get_text().strip().replace(u'\n', u' ')
        except IndexError:
            pass
        try:
            self.record["portions"] = soup.find_all(class_="portions")[0].get_text().strip().replace(u'\n', u' ')
        except IndexError:
            pass
        try:
            self.record["time"] = soup.find_all(class_="total-time")[0].get_text().strip().replace(u'\n', u' ')
        except IndexError:
            pass

        ingredients = soup.find_all(class_="substances-list")[0]
        groups = ingredients.find_all(class_="title-red-small")
        ingredients = ingredients.find_all(class_=["title-red-small", "item"])

        self.record["ingredients"] = {}
        group = "general"
        if len(groups) <= 0:
            self.record["ingredients"][group] = {}

        for item in ingredients:
            if item.name == 'h3':
                group = item.get_text()
                self.record["ingredients"][group] = {}
                continue
            else:
                ingredient = item.find_all(class_="title")[0].get_text()
                amount = item.find_all(class_="amount")[0].get_text().strip().replace(u'\n', u' ').replace(u'\t', u'')
                if amount == "ks":
                    amount = ''
                self.record["ingredients"][group][ingredient] = amount


        procedure = soup.find_all(class_="procedure-list")[0].find_all("div")
        if procedure[0].attrs:
            section = procedure[1].find_all(class_="num")
            recipe = procedure[1].find_all(class_="text")
        else:
            section = procedure[0].find_all(class_="num")
            recipe = procedure[0].find_all(class_="text")

        self.record["recipe"] = {key.get_text(): value.get_text() for key, value in zip(section, recipe)}



def main():
    # record = ApetitRecord('https://www.apetitonline.cz/recept/chrestovy-quiche')
    # record = ApetitRecord('https://www.apetitonline.cz/recept/bifteki-se-salatem-a-rozmarynovymi-bramborami')
    record = VarechaRecord("https://varecha.pravda.sk/recepty/bruschetta-s-marinovanym-lososom-a-horcicovou-penou/75893-recept.html")
    # record = DobruchutRecord("https://dobruchut.aktuality.sk/recept/43534/tekvicove-gnocchi-s-hubovou-omackou/")
    # record = DobruchutRecord("https://dobruchut.aktuality.sk/recept/69575/luxusne-hokkaido-s-hubami-na-smotane/")

    record.scrape_data()
    record.print_data()


if __name__ == '__main__':
    main()
