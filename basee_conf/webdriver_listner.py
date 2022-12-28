import pytest
from selenium import webdriver


class WebDriveWrapper:
    @pytest.fixture(autouse=True, scope="function")
    def set_up_login(self):
        print("browser launch")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("https://demo.openemr.io/b/openemr")
        yield
        print("quit browser")
        self.driver.quit()
