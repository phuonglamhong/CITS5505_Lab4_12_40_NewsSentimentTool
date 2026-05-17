'''
This file contains the Selenium test for the login functionality of the NewsSentiment application.
It uses shared fixtures for WebDriver setup and login to ensure consistent testing across different test cases.
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This test verifies that a user can successfully log in with valid credentials and is redirected to the dashboard page.
def test_login(driver, login):
    login("testForm17@abc.com", "11111111")
    print(driver.page_source)
    assert "Dashboard" in driver.page_source
