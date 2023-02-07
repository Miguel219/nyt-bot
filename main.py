from typing import List, Tuple
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement, By
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time

URL = "https://www.nytimes.com/"

TERM = "soccer"

SECTION = "Any"
SECTION = "Briefing"

MONTHS_NUMBER = 0

OUTPUT = "output/data.xlsx"


browser_lib = Selenium()


def open_the_website(url: str) -> bool:
    try:
        browser_lib.open_available_browser(url)
        return False
    except:
        return True


def input_text(locator: str, term: str) -> bool:
    try:
        browser_lib.input_text(locator, term)
        return False
    except:
        return True


def search_for(locator: str, term: str) -> bool:
    try:
        error = input_text(locator, term)
        browser_lib.press_keys(locator, "ENTER")
        return error
    except:
        return True


def click_button(locator: str) -> bool:
    try:
        browser_lib.click_button(locator)
        return False
    except:
        return True


def click_element(locator: str) -> bool:
    try:
        browser_lib.click_element(locator)
        return False
    except:
        return True


def get_element_in_element(by: str, locator: str, element: WebElement) -> WebElement or None:
    try:
        return element.find_element(by, locator)
    except:
        return None


def get_element(locator: str) -> WebElement or None:
    try:
        return browser_lib.get_webelement(locator)
    except:
        return None


def get_elements(locator: str) -> List[WebElement] or None:
    try:
        return browser_lib.get_webelements(locator)
    except:
        return None


def get_dates(months_number: int) -> Tuple[str, str]:
    if months_number == 0:
        months_number = 1
    endDate = datetime.now()
    startDate = endDate - relativedelta(months=months_number)
    return startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y')


def count_term_in_string(term: str, text: str) -> int:
    return text.lower().count(term.lower())


def main():
    try:
        # Search Term
        open_the_website(URL)
        error = click_button("xpath: //*[@data-test-id='search-button']")
        error = search_for("xpath: //*[@data-testid='search-input']", TERM)
        if error:
            raise 'Error searching for a term'

        # Set date range
        startDate, endDate = get_dates(MONTHS_NUMBER)
        error = click_button(
            "xpath: //*[@data-testid='search-date-dropdown-a']")
        error = click_button("xpath: //*[@value='Specific Dates']")
        error = input_text(
            "xpath: //*[@data-testid='DateRange-startDate']", startDate)
        error = input_text(
            "xpath: //*[@data-testid='DateRange-endDate']", endDate)
        error = click_button(
            "xpath: //*[@data-testid='search-date-dropdown-a']")
        if error:
            raise 'Error setting date range'
        time.sleep(1)

        # Set section
        if SECTION != 'Any':
            error = click_button(
                "xpath: //div[@data-testid='section']//button[@data-testid='search-multiselect-button']")
            error = click_element(
                "xpath: //*[contains(@value, '{}')]".format(SECTION))
            if error:
                raise 'Error setting section'
            time.sleep(1)

        # Sort by newest
        error = click_element("xpath: //*[contains(text(), 'Sort by Newest')]")
        if error:
            raise 'Error sorting by newest'
        time.sleep(1)

        # Show all results
        error = click_button(
            "xpath: //button[@data-testid='search-show-more-button']")
        while not error:
            time.sleep(1)
            error = click_button(
                "xpath: //button[@data-testid='search-show-more-button']")

        # Get all information
        rows = []
        results = get_elements(
            "xpath: //ol[@data-testid='search-results']//li[@data-testid='search-bodega-result']")
        for element in results:
            row = {}
            data = element.text.split('\n')
            row['title'] = data[2]
            row['date'] = data[0]
            row['description'] = (
                data[3]
                if data[3].find('PRINT EDITION') == -1
                else ''
            )
            picture = get_element_in_element(
                By.CLASS_NAME, 'css-rq4mmj', element)
            row['picture_filename'] = picture.get_attribute(
                'src') if picture else ''
            row['count_search_phrases'] = (
                count_term_in_string(TERM, row['title']) +
                count_term_in_string(TERM, row['description'])
            )
            rows.append(row)

        # Save data
        print('Saving {} rows of {} results'.format(len(rows), len(results)))
        dataframe = pd.DataFrame(rows)
        dataframe.to_excel(OUTPUT)
    finally:
        browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()
