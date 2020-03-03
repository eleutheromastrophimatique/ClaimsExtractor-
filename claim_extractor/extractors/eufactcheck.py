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
        max_page = int(pages_list[-2].contents[0])
        return max_page


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

        #title
        #Since the title always starts with claim followed by the title of the article we split the string based on ":"
        full_title = parsed_claim_review_page.find("div", class="page-title-head hgroup").find("h1").text.split(":")
        claim.set_title(full_title[1])

        #date
        full_date = parsed_claim_review_page.find("time").datetime.split("T")
        claim.set_date(full_date[0])

        #body
        body = parsed_claim_review_page.find("entry-content")
        claim.set_body(body.get_text())

        #related related_links
        div_tag = parsed_claim_review_page.find("entry-content")
        related_links = []
        for link in div_tag.findAll('a', href=True):
            related_links.append(link['href'])
        claim.set_refered_links(related_links)

        #claim.set_claim(claim.title) need to understand this

        #rating
        rating = full_title[0].strip()
        claim.set_alternate_name(rating)

        return [claim]
