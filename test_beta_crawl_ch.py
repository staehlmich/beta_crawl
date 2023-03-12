import pytest
from beta_crawl_ch import Crawler

def test_url():
    url = 'https://www.coop.ch/de/lebensmittel/brot-backwaren/c/m_0115?q=%3AtopRated&sort=mostlyBought&pageSize=60&page='
    c = Crawler(url)
    assert c.url[-1] == "="

def test_page_getter():
    url = 'https://www.coop.ch/de/lebensmittel/brot-backwaren/c/m_0115?q=%3AtopRated&sort=mostlyBought&pageSize=60&page='
    c = Crawler(url)
    assert c._get_number_of_pages() >= 0

def test_column_len():
    url = 'https://www.coop.ch/de/lebensmittel/brot-backwaren/c/m_0115?q=%3AtopRated&sort=mostlyBought&pageSize=60&page=1'
    c = Crawler(url)
    assert len(c.columns) == 15

