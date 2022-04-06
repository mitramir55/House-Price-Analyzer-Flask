from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time



class WebDriver:
    location_data = {}

    def __init__(self):

        self.PATH = "chromedriver.exe"
        self.options = Options()
    #   Try adding this line if you get the error of chrome chrashed
    #   self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
        self.location_data["Reviews"] = []
        self.location_data["Popular Times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}


        def get_location_data(self):

            try:
                avg_rating = self.driver.find_element_by_class_name("section-star-display")
                total_reviews = self.driver.find_element_by_class_name("section-rating-term")
                address = self.driver.find_element_by_css_selector("[data-item-id='address']")
                phone_number = self.driver.find_element_by_css_selector("[data-tooltip='Copy phone number']")
                website = self.driver.find_element_by_css_selector("[data-item-id='authority']")
            except:
                pass

            try:
                self.location_data["rating"] = avg_rating.text
                self.location_data["reviews_count"] = total_reviews.text[1:-1]
                self.location_data["location"] = address.text
                self.location_data["contact"] = phone_number.text
                self.location_data["website"] = website.text
            except:
                pass


            
        def scrape(self, url):
            try:
                self.driver.get(url)
            except Exception as e:
                self.driver.quit()
                continue
            time.sleep(10)

            self.get_location_data()
            time.sleep(5)
            self.driver.quit()

            return(self.location_data)

url = "your_location_url"
x = WebDriver()
print(x.scrape(url))