'''
This file contains the Selenium test for the logout functionality of the NewsSentiment application.
It uses shared fixtures for WebDriver setup and login to ensure consistent testing across different test cases.
''' 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# This test verifies that a logged-in user can successfully log out and is redirected to the login page.
def test_logout(driver, login):
    login("testForm17@abc.com", "11111111")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-blue-100"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    ).click()

    assert "Log in" in driver.page_source