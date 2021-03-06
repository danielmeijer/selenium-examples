import os
import logging
import time

from pyvirtualdisplay import Display
from selenium import webdriver

logging.getLogger().setLevel(logging.INFO)


BASE_URL = os.environ['scrape_url']

def start_chrome():

    global display
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    logging.info('Initialized virtual display..')

    global chrome_options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.getcwd(),
        'download.prompt_for_download': False,
    })
    logging.info('Prepared chrome options..')

    global browser
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_window_size(1920, 1080)
    browser.get(BASE_URL)

    logging.info('Initialized chrome browser..')

def start_firefox():

    global display
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    logging.info('Initialized virtual display..')

    global firefox_profile
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('browser.download.folderList', 2)
    firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
    firefox_profile.set_preference('browser.download.dir', os.getcwd())
    firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    logging.info('Prepared firefox profile..')

    global browser
    browser = webdriver.Firefox(firefox_profile=firefox_profile)
    browser.set_window_size(1920, 1080)
    logging.info('Initialized firefox browser..')

    browser.get(BASE_URL)

def get_urls():
    
    start_chrome()

    browser.find_element_by_xpath('//*[@id="aceptar"]').click()
    time.sleep(5)

    elems = browser.find_elements_by_xpath("//a[@href]")
    print(elems)
    for elem in elems:
        url=elem.get_attribute("href")
        if url.startswith('http'):
            print(url)

    browser.quit()
    display.stop()


def take_screenshot():
    start_chrome()

    # Accept Cookies
    #browser.find_element_by_xpath('//*[@id="aceptar"]').click()
    #time.sleep(1)

    logging.info('Accessed %s ..', BASE_URL)

    logging.info('Page title: %s', browser.title)
    time.sleep(3)
    browser.save_screenshot('./output/chrome.png')
    logging.info('Screenshot taken')

    browser.quit()
    display.stop()


def take_screenshot_firefox():
    start_firefox()

    # Accept Cookies
    #browser.find_element_by_xpath('//*[@id="aceptar"]').click()
    #time.sleep(1)

    logging.info('Accessed %s ..', BASE_URL)

    logging.info('Page title: %s', browser.title)
    time.sleep(3)
    browser.save_screenshot('./output/firefox.png')
    logging.info('Screenshot taken')

    browser.quit()
    display.stop()


if __name__ == '__main__':

    get_urls()
    take_screenshot()
    take_screenshot_firefox()
