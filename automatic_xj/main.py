import yaml
from playwright.sync_api import sync_playwright

from Zabbix import *
playwright_config=yaml.safe_load()
if __name__=="__main__":

    with open("playwright_config.yaml", 'r') as file:
        playwright_config = yaml.safe_load(file)
        chrome_path = playwright_config['chrome_path']
    p=sync_playwright().start()
    browser = p.chromium.launch(headless=False,
                                executable_path=chrome_path)
    page=browser.new_page()

    zabbix = Zabbix(browser,'dwzyywzt')
    #先测试zabbix
    zabbix.login()

    input('3.....')
    browser.close()
    p.stop()