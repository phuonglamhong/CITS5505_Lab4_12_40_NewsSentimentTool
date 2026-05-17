'''
This file contains the Selenium test for the dashboard feature of the NewsSentiment application. 
It uses shared fixtures for WebDriver setup and login to ensure consistent testing across different test cases.
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This test verifies that the dashboard page loads correctly and displays the expected content for a logged-in user.
def test_dashboard(driver, login):
    # Log in using shared fixture
    login("testForm17@abc.com", "11111111")

    # Navigate to dashboard explicitly
    driver.get("http://127.0.0.1:5000/dashboard")

    wait = WebDriverWait(driver, 10)

    # Wait for the page to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    page = driver.page_source

    # The dashboard page ALWAYS contains this server-rendered title:
    assert "Dashboard · BrandPulse" in page

    # The topbar title is also server-rendered:
    assert "Dashboard" in page

    # The welcome message is server-rendered and includes the user's name
    assert "Welcome back" in page

    # Stat card labels are server-rendered and safe to assert
    assert "Total Articles" in page
    assert "Positive" in page
    assert "Neutral" in page
    assert "Negative" in page

    # Sidebar footer is static and server-rendered
    assert "BrandPulse © 2026" in page
