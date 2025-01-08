import re
import warnings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests

from .estates import ufs

_capitals = ufs.values()


def get_data(cep:str) -> dict:
    """
    Fetch a capital's data from the API https://viacep.com.br/
    :param cep: To be searched
    :return: Capital's data
    """
    warnings.warn("Massive use for validation of local databases may automatically block your access for an indefinite period")
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    response.raise_for_status()
    return response.json()


def get_capital(cep:str) -> str:
    """
    Try to find the capital of a given CEP with the API https://viacep.com.br/
    :param cep: To be searched
    :return: Capital
    """
    warnings.warn("Massive use for validation of local databases may automatically block your access for an indefinite period")
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    response.raise_for_status()
    return ufs[response.json()["uf"]]


def get_capital_weather(capital:str, existing_capitals=True) -> str:
    """
    Scrape for the weather of a capital in https://previsao.inmet.gov.br/
    :param capital: To be searched
    :param existing_capitals: True will raise an ValueError case the capital is invalid
    :return: Weather forecast
    """
    if existing_capitals and capital not in _capitals:
        raise ValueError(f"invalid option string '{capital}': capital should be in {_capitals}")
    capital = capital.replace(" ", "-")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=old")
    driver = webdriver.Chrome(options=options)
    driver.get("https://previsao.inmet.gov.br/")
    delay = 3
    elem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.ID, capital)))
    temp = elem.get_attribute("textContent")
    driver.close()
    temp = re.sub(" +", " ", temp)
    while True:
        if "\n \n" not in temp and "\n\n" not in temp: break
        temp = temp.replace("\n \n", "\n").replace("\n\n", "\n")
    return temp.replace("\n ", "\n").replace(" \n", "\n").replace("Tendência:", "")
