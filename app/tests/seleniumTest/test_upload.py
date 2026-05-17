'''
This file contains the Selenium test for the manual text upload feature of the NewsSentiment application.
It uses shared fixtures for WebDriver setup and login to ensure consistent testing across different test cases.
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# This test verifies that a user can manually enter text for analysis and receive sentiment results on the analysis page.
def test_manual_upload(driver, login):
    login("testForm17@abc.com", "11111111")

    driver.get("http://127.0.0.1:5000/upload")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "content"))).send_keys("This is a great day!")
    wait.until(EC.element_to_be_clickable((By.ID, "submit"))).click()

    assert "Sentiment" in driver.page_source