from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import urllib.request  

# URL Format: https://philadelphia.craigslist.org/search/sss?query=barbell&sort=rel&search_distance=20&postal=19426&min_price=0&max_price=150

class craigslist_scrapper(object):
    def __init__(self, location, postal, max_price, radius, item):
        self.location = location
        self.postal = postal
        self.max_price = max_price
        self.radius = radius
        self.item = item
        # URL
        self.url = f'http://{location}.craigslist.org/search/sss?query={item}&sort=rel&search_distance={radius}&postal={postal}&max_price={max_price}'

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.delay = 3  # number of seconds waiting before elements load

    def load_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            # searchs for 'searchform', location in HTML containing data being extracted
            wait.until(EC.presence_of_element_located((By.ID, 'searchform')))
            print('Page is Ready...')
        except TimeoutException:
            print('Loading took too much time!')

    def extractPostInfo(self):
        # driver.find_element_by_... can be used to find various elements on webpage (see documentation for more info)
        # Documentation: https://selenium-python.readthedocs.io/locating-elements.html
        all_post = self.driver.find_elements_by_class_name('result-row')
        titles = []
        prices = []
        dates = []
        for post in all_post:
            title = post.text.split('$')
            if title[0] == '':
                title = title[1]
            else:
                title = title[0]
            title = title.split('\n')
            price = title[0]
            title = title[-1]

            title = title.split(' ')
            month = title[0]
            day = title[1]
            date = month + ' ' + day
            title = ' '.join(title[2:])
            
            prices.append(price)
            titles.append(title)
            dates.append(date)

        return prices, titles, dates

    def extractPostURL(self):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, 'lxml')
        # 'a' is used to specifiy link
        for link in soup.findAll('a', {'class': 'result-title hdrlnk'}):
            url_list.append(link['href'])
        return url_list

    def quit(self):
        self.driver.close()


item = input('What are you looking for?')
city = 'philadelphia'
postalCode = input('Postal Code?')
maxP = input('Max price?')
maxDistance = input('Radius?')

scrapper = craigslist_scrapper(city, postalCode, maxP, maxDistance, item)
scrapper.load_url()
prices, titles, dates = scrapper.extractPostInfo()
links = scrapper.extractPostURL()
scrapper.quit()

for i in range(0, len(prices)):
    print('Price...' + str(prices[i]))
    print('Title...' + titles[i])
    print('Date...' + dates[i])
    print('URL...' + links[i])
    print('------------------------------------------------')
