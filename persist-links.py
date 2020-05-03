#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
import requests

# this code will tell 'the internet archive . org to keep good blog posts for us!

def persist(url_to_persist: str) -> None:
    # tell the internet archive to save a website for us
    ia_url = f"https://web.archive.org/save/{url_to_persist}"
    resp = requests.get(ia_url)
    assert resp.status_code == 200, resp.text
    assert "Saving page now" in resp.text, resp.text
    print("done")


def get_links(url: str) -> None:
    # url: e.g. https://github.com/kmille/linux-accept-queue/blob/master/README.md
    resp = requests.get(url)
    assert resp.status_code == 200, resp.text
    bs = BeautifulSoup(resp.text, 'html.parser')
    links = [x.get('href', "github") for x in bs.findAll("a")]
    links = [link for link in links if link.startswith("http")]
    links = [link for link in links if "github" not in link]
    while 1:
        for i, link in enumerate(links):
            print(f"{i:2}  {link}")
        index = input("Wich link to persist? ")
        persist(links[int(index)])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f"ERROR: {sys.argv[0]} <url>")
        sys.exit(1)
    #url = "https://github.com/kmille/linux-accept-queue/blob/master/README.md"
    url = sys.argv[1]
    links = get_links(sys.argv[1])
