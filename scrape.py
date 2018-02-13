#!/usr/bin/env python3

import pdb

import csv
import sys
import requests
from bs4 import BeautifulSoup

CAUSE_URLS = ["https://www.google.org/our-work/education/",
              "https://www.google.org/our-work/economic-opportunity/",
              "https://www.google.org/our-work/inclusion/",
              "https://www.google.org/our-work/crisis-response/"]

HEADERS = {'User-Agent': 'Mozilla/5.0 '
           '(X11; Linux x86_64) AppleWebKit/537.36 '
           '(KHTML, like Gecko) '
           'Chrome/63.0.3239.132 Safari/537.36'}


def main():
    fieldnames = ["grantee", "description", "Funding began in",
                  "Total funding", "Focus", "Region of Impact"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for cause_url in CAUSE_URLS:
        for grant in cause_grants(cause_url):
            writer.writerow(grant)


def cause_grants(cause_url):
    soup = BeautifulSoup(requests.get(cause_url, headers=HEADERS).content,
                         "lxml")
    grants = []

    grant_urls = []
    prefix = cause_url.split('/')[-2]
    for link in soup.find_all("a"):
        if str(link.get("href")).startswith("/our-work/" + prefix + "/"):
            grant_url = "https://www.google.org" + link.get("href")
            if grant_url not in grant_urls:
                grant_urls.append(grant_url)

    for grant_url in grant_urls:
        grants.append(grant_info(grant_url))

    for grantee in soup.find_all("section", {"class": "single-accordion--static"}):
        grantee_dict = {"grantee": grantee.find("h3").text.strip(),
                        "description": grantee.find("p",
                            {"class": "single-accordion__description"})
                            .text.strip()}
        for key, val in zip(grantee.find_all("dt"), grantee.find_all("dd")):
            grantee_dict[key.text] = val.text
        grants.append(grantee_dict)
    # pdb.set_trace()
    return grants


def grant_info(grant_url):
    soup = BeautifulSoup(requests.get(grant_url, headers=HEADERS).content,
                         "lxml")
    grantee_dict = {"grantee": soup.find("h1").text.strip()}
    for key, val in zip(soup.find_all("dt"), soup.find_all("dd")):
        grantee_dict[key.text] = val.text
    return grantee_dict


if __name__ == "__main__":
    main()
