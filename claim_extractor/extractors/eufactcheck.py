# -*- coding: utf-8 -*-
import re
from typing import List

from bs4 import BeautifulSoup
from tqdm import tqdm

from claim_extractor import Claim, Configuration
from claim_extractor.extractors import FactCheckingSiteExtractor, caching, find_by_text


class EufactcheckFactCheckingSiteExtractor(FactCheckingSiteExtractor):

    def __init__(self, configuration: Configuration):
        super().__init__(configuration)
        self.date_regexp = re.compile("^([0-9]{4})/([0-9]{2})/([0-9]{2})*") #date:annee, mois, jour

    def retrieve_listing_page_urls(self) -> List[str]:
        return ["https://eufactcheck.eu/fact-checks/page/1/"]

    def find_page_count(self, parsed_listing_page: BeautifulSoup) -> int:
        pages_list = parsed_listing_page.find("paginator").children
        print("________________" + pages_list[-1])

        return 0

#    def find_page_count(self, parsed_listing_page: BeautifulSoup) -> int:
#        count = 26
#        url = "https://eufactcheck.eu/page/" + str(count + 1)
#        result = caching.get(url, headers=self.headers, timeout=10)
#        if result:
#            while result:
#                count += 1
#                url = "https://eufactcheck.eu/page/" + str(count)
#                result = caching.get(url, headers=self.headers, timeout=10)
#                if result:
#                    parsed = BeautifulSoup(result, self.configuration.parser_engine)
                    # ???
#                    articles = parsed.find("articles").findAll("article")
#                    if not articles or len(articles) == 0:
#                        break
#        else:
#            count -= 1

#        return count


    def retrieve_urls(self, parsed_listing_page: BeautifulSoup, listing_page_url: str, number_of_pages: int) \
            -> List[str]:
        urls = self.extract_urls(parsed_listing_page)
        return urls


    def extract_urls(self, parsed_listing_page: BeautifulSoup):
        urls = list()
        return urls


    def extract_claim_and_review(self, parsed_claim_review_page: BeautifulSoup, url: str) -> List[Claim]:
        claim = Claim()
        claim.set_url(url)
        claim.set_source("eufactcheck")
        return [claim]
