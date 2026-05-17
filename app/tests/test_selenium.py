"""
Selenium tests for the NewsSentiment application.
Requires live server at http://127.0.0.1:5000

Run: python -m pytest app/tests/test_selenium.py -v
Before running:
    1. python run.py
    2. Ensure theboss@outlook.com / 88888888 exists
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "theboss@outlook.com"
TEST_PASSWORD = "88888888"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def login(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "#login-form input[type='submit']").click()
    time.sleep(2)


# Test 1 — Welcome page loads
def test_welcome_page_loads(driver):
    driver.get(BASE_URL)
    time.sleep(1)
    assert "News Sentiment" in driver.page_source


# Test 2 — Login page has email and password fields
def test_login_page_has_fields(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(1)
    assert driver.find_element(By.NAME, "email").is_displayed()
    assert driver.find_element(By.NAME, "password").is_displayed()


# Test 3 — Login redirects to dashboard or welcome
def test_login_success(driver):
    login(driver)
    assert driver.current_url in [f"{BASE_URL}/", f"{BASE_URL}/dashboard"] or "Welcome" in driver.page_source


# Test 4 — Dashboard shows stat cards
def test_dashboard_stats(driver):
    driver.get(f"{BASE_URL}/dashboard")
    time.sleep(1)
    assert "Total Articles" in driver.page_source


# Test 5 — Upload page accessible
def test_upload_page(driver):
    driver.get(f"{BASE_URL}/upload")
    time.sleep(1)
    assert driver.find_element(By.NAME, "brand").is_displayed()


# Test 6 — Competitor page loads
def test_competitor_page(driver):
    driver.get(f"{BASE_URL}/competitor")
    time.sleep(2)
    assert "Competitor" in driver.page_source


# Test 7 — Discussion page loads
def test_discussion_page(driver):
    driver.get(f"{BASE_URL}/comments")
    time.sleep(1)
    assert "Discussion" in driver.page_source


if __name__ == "__main__":
    pytest.main([__file__, "-v"])