import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture
def setup_teardown():
    """Setup and teardown for Chrome WebDriver."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()


# ✅ Test 1: Form page should load correctly
def test_form_page_loads(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    assert "Registeration Form" in driver.page_source or "Registration Form" in driver.title


# ✅ Test 2: Submit form with valid details and verify success message
def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    # Fill form
    driver.find_element(By.NAME, "username").send_keys("Kiran")
    driver.find_element(By.NAME, "email").send_keys("kiran@example.com")
    driver.find_element(By.NAME, "year").send_keys("3")

    # Submit
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(2)

    # Verify redirect to /submit
    assert "/submit" in driver.current_url, "Did not navigate to /submit after submission"

    # Verify content on the result page
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Submission Successful" in body_text or "Dear" in body_text
    assert "Kiran" in body_text
    assert "3" in body_text


# ✅ Test 3: Missing username should reload form page
def test_missing_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "year").send_keys("2")

    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(1)

    # Expect to stay on the same form page
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Registeration Form" in body_text or "Registration Form" in driver.title
