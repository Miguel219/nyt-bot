import os
import re
import time
from datetime import datetime
from typing import Tuple
from urllib.parse import urlparse

import pandas as pd
from dateutil.relativedelta import relativedelta
from selenium.webdriver.remote.webelement import By

from CustomSelenium import CustomSelenium


class BotException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NYTBot:
    def __init__(self,
                 term: str,
                 section: str,
                 months_number: int,
                 output_excel: str,
                 output_pictures: str
                 ):
        self.seh = CustomSelenium()
        self.url = "https://www.nytimes.com/"
        self.term = term
        self.section = section
        self.months_number = months_number
        self.output_excel = output_excel
        self.output_pictures = output_pictures

    def get_dates(self, months_number: int) -> Tuple[str, str]:
        if months_number == 0:
            months_number = 1
        endDate = datetime.now()
        startDate = endDate - relativedelta(months=months_number)
        return startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y')

    def count_term_in_string(self, term: str, text: str) -> int:
        return text.lower().count(term.lower())

    def contains_any_amount_of_money(self, text: str) -> bool:
        format1 = '[$]([0-9]+([.][0-9]+)?)'
        format2 = '[$]([0-9]?[0-9]?[0-9]?([,][0-9]{{3}})*([.][0-9]+)?)'
        format3 = '([0-9]+([.][0-9]+)?)(( dollars)|( USD))'
        format4 = '([0-9]?[0-9]?[0-9]?([,][0-9]{{3}})*([.][0-9]+)?)(( dollars)|( USD))'
        if re.search("({})|({})|({})|({})".format(format1, format2, format3, format4), text):
            return True
        else:
            return False

    # Search Term
    def search_term(self):
        try:
            self.seh.click_button(
                "xpath: //*[@data-test-id='search-button']")
            self.seh.search_for(
                "xpath: //*[@data-testid='search-input']", self.term)
        except:
            raise BotException('Error searching for a term')

    # Set date range
    def set_date_range(self):
        try:
            startDate, endDate = self.get_dates(self.months_number)
            self.seh.click_button(
                "xpath: //*[@data-testid='search-date-dropdown-a']")
            self.seh.click_button("xpath: //*[@value='Specific Dates']")
            self.seh.input_text(
                "xpath: //*[@data-testid='DateRange-startDate']", startDate)
            self.seh.input_text(
                "xpath: //*[@data-testid='DateRange-endDate']", endDate)
            self.seh.click_button(
                "xpath: //*[@data-testid='search-date-dropdown-a']")
            time.sleep(1)
        except:
            raise BotException('Error setting date range')

    # Set section
    def set_section(self):
        if self.section != 'Any':
            try:
                self.seh.click_button(
                    "xpath: //div[@data-testid='section']//button[@data-testid='search-multiselect-button']")
                self.seh.click_element(
                    "xpath: //*[contains(@value, '{}')]".format(self.section))
                time.sleep(1)
            except:
                raise BotException('Error setting section')

    # Sort by newest
    def sort_by_newest(self):
        try:
            self.seh.click_element(
                "xpath: //*[contains(text(), 'Sort by Newest')]")
            time.sleep(1)
        except:
            raise BotException('Error sorting by newest')

    # Show all results
    def show_all_results(self):
        locator = "xpath: //button[@data-testid='search-show-more-button']"
        try:
            while True:
                self.seh.click_button(locator)
                time.sleep(1)
        except Exception as e:
            print(e)

    # Get all information
    def get_all_information(self):
        self.results = []
        results = self.seh.get_elements(
            "xpath: //ol[@data-testid='search-results']//li[@data-testid='search-bodega-result']")
        for element in results:
            row = {}
            data = element.text.split('\n')

            # Title
            row['title'] = data[2]

            # Date
            row['date'] = data[0]

            # Description
            row['description'] = (
                data[3]
                if data[3].find('PRINT EDITION') == -1
                else ''
            )

            # Picture
            picture = self.seh.get_element_in_element(
                By.CLASS_NAME, 'css-rq4mmj', element)
            if picture:
                # Save picture filename
                row['picture_filename'] = os.path.basename(
                    urlparse(picture.get_attribute('src')).path)

                # Save picture
                with open('{}/{}'.format(self.output_pictures, row['picture_filename']), 'wb') as file:
                    file.write(picture.screenshot_as_png)
            else:
                row['picture_filename'] = ''

            # Count Search Phrases
            row['count_search_phrases'] = (
                self.count_term_in_string(self.term, row['title']) +
                self.count_term_in_string(self.term, row['description'])
            )

            # Contains any amount of money
            row['contains_any_amount_of_money'] = (
                self.contains_any_amount_of_money(row['title']) or
                self.contains_any_amount_of_money(row['description'])
            )

            # Append results
            self.results.append(row)

    # Save data
    def save_data(self):
        print('Saving {} results'.format(len(self.results)))
        dataframe = pd.DataFrame(self.results)
        dataframe.to_excel(self.output_excel)

    # Run Bot
    def run(self):
        try:
            self.seh.open_available_browser(
                self.url, browser_selection='Chrome')
            self.search_term()
            self.set_date_range()
            self.set_section()
            self.sort_by_newest()
            self.show_all_results()
            self.get_all_information()
            self.save_data()
        finally:
            self.seh.close_all_browsers()
