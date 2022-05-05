from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import json

CONFIG_PATH = "config/CONFIG.json"


class AmazonScraper:
    def __init__(self, data):
        """Parameter initialization"""
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(data["driver_path"], options=options)
        # self.driver = webdriver.Chrome(data['driver_path'])

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element_by_name("session_key")
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element_by_name("session_password")
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)

    def book_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""

        # go to Jobs
        jobs_link = self.driver.find_element_by_xpath(
            "//a[@data-test-global-nav-link='jobs']"
        )
        jobs_link.click()

        # search based on keywords and location and hit enter
        time.sleep(1.5)
        search_keywords = self.driver.find_element_by_xpath(
            "//*[contains(@id,'jobs-search-box-keyword')]"
        )
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element_by_xpath(
            "//*[contains(@id,'jobs-search-box-location-id')]"
        )
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)

    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # # find the total amount of results
        # total_results = self.driver.find_element_by_class_name(
        #     "display-flex.t-12.t-black--light.t-normal"
        # )
        # # total_results_int = int(total_results.text.split(" ", 1)[0].replace(".", ""))

        # time.sleep(1)
        # get number of last page
        last_page = 0
        pages = self.driver.find_elements_by_xpath(
            "//*[contains(@class,'artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view')]"
        )
        if len(pages) > 0:
            last_page = int(pages[-1].text)

        # get results from pages until the results counter match the number of jobs expected
        current_page = self.driver.current_url
        job_count = 0
        for page_number in range(25, last_page + 25, 25):
            time.sleep(3.5)
            results = self.driver.find_elements_by_xpath(
                "//*[contains(@class,'jobs-search-results__list-item occludable-update p0')]"
            )
            for result in results:
                job_count += 1
                hover = (
                    ActionChains(self.driver)
                    .move_to_element_with_offset(result, 10, 0)
                    .click()
                )
                hover.perform()
                time.sleep(0.2)
                self.extract_data(result)
                if job_count == self.quantity:
                    return
            self.driver.get(f"{current_page}&start={str(page_number)}")

    def extract_data(self, job_object):
        title = job_object.find_element_by_xpath(
            "//*[contains(@class,'disabled ember-view job-card-container__link job-card-list__title')]"
        ).text
        link = job_object.find_element_by_xpath(
            "//*[contains(@class,'jobs-details-top-card__job-title-link ember-view')]"
        ).get_attribute("href")
        company_info = job_object.find_element_by_xpath(
            "//*[contains(@class,'jobs-details-top-card__company-info t-14 t-black--light t-normal mt1')]"
        )
        company = company_info.find_elements_by_xpath(
            ".//*[contains(@class, 'jobs-details-top-card__company-url t-black--light t-normal ember-view')]"
        )
        location = company_info.find_elements_by_xpath(
            ".//*[contains(@class, 'jobs-details-top-card__bullet')]"
        )

        if len(company) > 0:
            company = company[0].text
        else:
            company = "Empresa não especificada"

        if location[0].text != "":
            location = " - ".join([local.text for local in location])
        else:
            location = "Local não especificado"

        self.jobs_list.append([title, company, location, link])

    def generate_csv(self):
        df = pd.DataFrame(
            self.jobs_list, columns=["Vaga", "Empresa", "Localização", "Link"]
        )
        df.to_csv(
            r"C://Users//lucas.oppi//AppData//Local//Programs//Python//Python38-32//arqs//Personal//Linkedin//jobs.csv",
            header=True,
            index=False,
        )

    def close_session(self):
        """This function closes the actual session"""

        print("Busca terminada!")
        self.driver.close()

    def get_jobs(self):
        """Apply to job offers"""
        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(3)
        self.job_search()
        time.sleep(3)
        self.find_offers()
        time.sleep(1)
        self.generate_csv()
        self.close_session()


if __name__ == "__main__":
    with open(CONFIG_PATH) as file:
        configs = json.load(file)
    bot = SearchJobsLinkedin(configs)
    bot.get_jobs()
