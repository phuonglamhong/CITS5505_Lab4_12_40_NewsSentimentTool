'''
This file contains the Selenium test for the text analysis feature of the NewsSentiment application. 
It uses shared fixtures for WebDriver setup and login to ensure consistent testing across different test cases.
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This test verifies that the text analysis page loads correctly and displays the expected results 
# after submitting text for analysis.
def test_analyze(driver, login):
    # Log in using the shared fixture
    login("testForm17@abc.com", "11111111")

    # Navigate to upload page
    driver.get("http://127.0.0.1:5000/upload")

    wait = WebDriverWait(driver, 10)

    # Enter text for analysis
    sample_text = "This is a wonderful day and I feel great about everything."
    wait.until(EC.presence_of_element_located((By.ID, "content"))).send_keys(sample_text)

    # Submit the form
    wait.until(EC.element_to_be_clickable((By.ID, "submit"))).click()

    # Wait for analysis page to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    page = driver.page_source

    # Verify the analysis page loaded
    assert "NewsSentiment — Analysis" in page

    # Verify single-text analysis fields
    assert "Overall Sentiment:" in page
    assert "Polarity:" in page
    assert "Subjectivity:" in page
    assert "Confidence:" in page

    # Verify the analyzed text appears
    assert sample_text in page
