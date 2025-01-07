"""
Module for managing browser tabs and WebDriver operations using Selenium.
"""
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = None


def get_driver():
    """Global webdriver"""
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        driver = webdriver.Chrome(options=chrome_options)
    return driver


def pick_website_pane(driver: webdriver, target: str) -> bool:
    """
    Switches to the browser tab that matches the target URL or title of the pane.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        target (str): The target URL/title to find in open browser tabs.

    Returns:
        bool: True if a tab with the target URL/title is found and switched to, False otherwise.
    """
    window_handles = driver.window_handles

    for handle in window_handles:
        driver.switch_to.window(handle)
        if isinstance(target, str):
            if target.lower() in driver.title.lower():
                return True  # Successfully switched to the new window
        else:
            if target in driver.current_url:
                return True  # Successfully switched to the new window

    return False  # No window with the target URL or title found


def close_website_panes(driver: webdriver, target=None):
    """
    Closes browser windows based on the provided target, or all windows if no target is specified.
    Searches for the target in both window titles and URLs.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        target (str, optional): The target to match against window title or URL.
                                If None, all windows will be closed.
    """
    handles_to_close = []

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if target is None or (target and (re.search(target, driver.title) or re.search(target, driver.current_url))):
            print(f"Marking for closure: Title '{driver.title}', URL '{driver.current_url}'")
            handles_to_close.append(handle)

    for handle in handles_to_close:
        driver.switch_to.window(handle)
        driver.close()

    if driver.window_handles:
        driver.switch_to.window(driver.window_handles[0])
    else:
        print("All windows closed.")
        driver = None
