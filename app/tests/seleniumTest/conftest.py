'''
This file contains shared fixtures for Selenium tests, such as the WebDriver setup and login helper function.
'''
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This fixture initializes the Selenium WebDriver and ensures it is properly closed after tests.
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
# This fixture provides a reusable login function that can be called in any test that requires authentication.
@pytest.fixture
def login(driver):
    def _login(email, password):
        driver.get("http://127.0.0.1:5000/login")
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.NAME, "submit"))).click()

    return _login

