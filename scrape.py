#!/usr/bin/env python3

import pdb

from bs4 import BeautifulSoup

def main():
    with open("economic-opportunity.html", "r") as f:
        soup = BeautifulSoup(f, "lxml")
        grants = []
        for grantee in soup.find_all("section", {"class": "single-accordion"}):
            grantee_dict = {"grantee": grantee.find("h3").text.strip(),
                            "description": grantee.find("p", {"class": "single-accordion__description"}).text.strip()}
            for key, val in zip(grantee.find_all("dt"), grantee.find_all("dd")):
                grantee_dict[key.text] = val.text
            grants.append(grantee_dict)
        pdb.set_trace()


if __name__ == "__main__":
    main()
