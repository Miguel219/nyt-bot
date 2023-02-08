from typing import List

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement


class CustomSelenium(Selenium):

    def search_for(self, locator: str, term: str) -> bool:
        self.input_text(locator, term)
        self.press_keys(locator, "ENTER")

    def get_element_in_element(self, by: str, locator: str, element: WebElement) -> WebElement or None:
        try:
            return element.find_element(by, locator)
        except:
            return None

    def get_element(self, locator: str) -> WebElement or None:
        try:
            return self.get_webelement(locator)
        except:
            return None

    def get_elements(self, locator: str) -> List[WebElement] or None:
        try:
            return self.get_webelements(locator)
        except:
            return None
