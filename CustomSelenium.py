from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import By, WebElement
from webdriver_manager.chrome import ChromeDriverManager


class CustomSelenium(Chrome):

    def __init__(self):
        super().__init__(service=ChromeService(ChromeDriverManager().install()))

    def input_text(self, locator: str, term: str) -> WebElement:
        element = self.find_element(by=By.XPATH, value=locator)
        element.send_keys(term)
        return element

    def search_for(self, locator: str, term: str) -> WebElement:
        element = self.input_text(locator, term)
        element.send_keys(Keys.ENTER)
        return element

    def click_element(self, locator: str) -> WebElement:
        element = self.find_element(by=By.XPATH, value=locator)
        element.click()
        return element

    def get_element_in_element(self, by: str, locator: str, element: WebElement) -> WebElement or None:
        try:
            return element.find_element(by, locator)
        except:
            return None

    def get_element(self, locator: str) -> WebElement or None:
        try:
            return self.find_element(by=By.XPATH, value=locator)
        except:
            return None

    def get_elements(self, locator: str) -> List[WebElement]:
        try:
            return self.find_elements(by=By.XPATH, value=locator)
        except:
            return []
