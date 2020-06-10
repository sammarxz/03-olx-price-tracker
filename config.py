from selenium import webdriver


DIRECTORY = 'reports'
NAME = 'macbook'
REGION = 'grande-recife'
CATEGORY = 'computadores-e-acessorios'
BASE_URL = 'https://pe.olx.com.br/'


def get_firefox_web_driver(options):
    return webdriver.Firefox(firefox_options=options)


def get_web_driver_options():
    return webdriver.FirefoxOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore--certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')
