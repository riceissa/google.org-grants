#!/usr/bin/env python3

import pdb

import sys
import requests
from bs4 import BeautifulSoup

CAUSE_URLS = ["https://www.google.org/our-work/education/",
              "https://www.google.org/our-work/economic-opportunity/",
              "https://www.google.org/our-work/inclusion/",
              "https://www.google.org/our-work/crisis-response/"]


def main():
    fieldnames = ["FIXME"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for cause_url in CAUSE_URLS:
        for grant in cause_grants(cause_url):
            writer.writerow(grant)


def cause_grants(cause_url):
        soup = BeautifulSoup(requests.get(cause_url), "lxml")
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
        pdb.set_trace()


def grant_info(grant_url):
    soup = BeautifulSoup(requests.get(grant_url).content, "lxml")
    grantee_dict = {"grantee": soup.find("h1").text.strip()}
    for key, val in zip(grantee.find_all("dt"), grantee.find_all("dd")):
        grantee_dict[key.text] = val.text
    return grantee_dict


if __name__ == "__main__":
    main()
