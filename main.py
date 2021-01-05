from bs4 import BeautifulSoup
import requests


class SiteMap:
    def __init__(self):
        self.home_url = "https://www.dentists.com"
        self.file = open("sitemap.txt", "w")
        self.soup = lambda url: BeautifulSoup(requests.get(self.home_url + url).text, "html.parser")
        
    def write_get(self, url=""):
        self.soup(url)
        self.file.write(self.home_url + url + "\n")

    def main(self):
        self.write_get()
        states = self.soup("").find("div", class_="states-list-wrap")
        states = list(map(lambda x: x.get("href"), states.find_all("a")))
        for s in states:
            self.write_get(s)
            self.state(s)

    def state(self, state):
        print(state)
        cities = self.soup(state).find("div", id="states")
        cities = list(map(lambda x: x.get("href"), cities.find_all("a")))
        for c in cities:
            self.write_get(c)
            self.city(c)

    def city(self, city):
        print(city)

        def get_offices(url):
            return list(map(
                lambda x: x.get("href"), self.soup(url)
                .find("div", id="search-results-cont")
                .find_all("a", class_="office_title")
            ))

        offices = get_offices(city)

        def get_next_page(page):
            return self.soup(page).find("a", class_="pagination-button float-right").get("href")

        try:
            next_page = get_next_page(city)
        except:
            next_page = None
        while next_page:
            self.write_get(next_page)
            try:
                offices.extend(get_offices(next_page))
                next_page = get_next_page(next_page)
            except:
                break
        for o in offices:
            self.write_get(o)
            self.office(o)

    def office(self, office):
        office_data = self.office_dentist_data(office)
        dentists = list(map(
            lambda x: x.find("a").get("href"),
            self.soup(office).find_all("div", class_="dentist-info-block")
        ))
        for data in office_data:
            self.file.write(self.home_url + data + "\n")
        for d in dentists:
            self.write_get(d)
            self.dentist(d)

    def dentist(self, dentist):
        dentist_data = self.office_dentist_data(dentist)
        for data in dentist_data:
            self.file.write(self.home_url + data + "\n")

    def office_dentist_data(self, url):
        soup = self.soup(url)
        review = soup.find("a", class_="review-link").get("href")
        appointment_email = list(map(
            lambda x: x.get("href"),
            soup.find_all("a", class_="request-appointment")
        ))
        appointment_email.append(review)
        return appointment_email


if __name__ == "__main__":
    sitemap = SiteMap()
    sitemap.main()
