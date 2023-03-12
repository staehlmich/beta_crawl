#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15:44:58 2023

@author: michaelstaehli
"""
import json
import os
from datetime import datetime as dt

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Crawler:
    """
    Class to crawl and scrape products and prices from Coop pages.

    """
    def __init__(self, url:str):
        """
        :param url: Parameter url has to end on "=".
        """
        self.url = url
        self.number = 0
        self.ua_str = UserAgent().chrome
        self.products = pd.DataFrame()
        self.columns = ['id', 'title', 'href',
            'ratingAmount', 'ratingValue', 'brand',
             'price', 'priceContext', 'priceContextHiddenText',
             'priceContextPrice', 'priceContextAmount', 'udoCat',
             'productAriaLabel', 'declarationIcons', 'timestamp']

    def _get_number_of_pages(self):
        """
        Method to get the number of last pagination page.
        :return:
        """
        page = requests.get(self.url, headers={"User-Agent": self.ua_str})
        soup = BeautifulSoup(page.content, "html.parser")
        number = pd.to_numeric(
            soup.find_all('a', class_='pagination__page')[-1].text)
        return number

    def _scrape_products(self, url):
        """
        Method to scrape all pages from url.
        :return: pandas dataframe
        """

        page = requests.get(url, headers={"User-Agent": self.ua_str})
        soup = BeautifulSoup(page.content, "html.parser")

        meta_json = str(soup.find_all("meta")[15])
        meta_json = meta_json.replace('<meta data-pagecontent-json=\'',
                                      '').replace('\'/>', '')
        data = json.loads(meta_json)

        # Get prices from all products
        df = pd.DataFrame.from_dict(data['anchors'][0]['json']['elements'], orient='columns')
        return df

    def scrape_product(self):
        """
        Method to scrape all pages from a single product from today.
        :return: Dataframe with scraped products.
        """
        # Get total number of pages
        self.number = self._get_number_of_pages()

        for i in range(self.number):
            new_url = self.url+str(i+1)
            df = self._scrape_products(new_url)
            self.products = pd.concat([self.products, df])
            self.products.reset_index(drop=True, inplace=True)
        self.products['timestamp'] = dt.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        self.products = self.products[self.columns]

    def df_to_excel(self, product:str, path: str):
        """
        Method to write scraped products to an excel-file.
        :param product: name of the product.
        :return:
        """
        date_today = dt.today().strftime("%Y-%m-%d")
        self.products.to_excel(f"{path}/{product}_coop_{date_today}.xlsx")

def main():
    # Set Working Directory
    os.chdir(os.path.dirname(__file__))

    with open('urls.json') as json_file:
        data = json.load(json_file)
        for product, url in data.items():
            c = Crawler(url)
            c.scrape_product()
            c.df_to_excel(product,"./output")

if __name__ == '__main__':
    main()