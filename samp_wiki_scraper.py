# written by Andosius
# ----------------------------------------------
# Tool to download all files from old SA:MP-Wiki
# ----------------------------------------------
# some parts are from
# https://www.thepythoncode.com/article/extract-all-website-links-python
#
# import all the packages required so no need to import in methods
# from my points of view it's bad practice which lets the code look messy


import os
import requests
from time import sleep
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from urllib.parse import unquote
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import colorama


# Define colors before usage, no matter what mode user is going to choose
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED


# constants
HEADERS = {'User-Agent': 'samp-wiki-scraper'}
PREFIX = "dump/"        # can be used for real path too
WIKIURL = "https://team.sa-mp.com/wiki-archive.html"
SLEEPING = 3


# styles and javascripts required
assets = [
    # styles and javascript files
    "skins/common/commonPrint.css",
    "skins/monobook/main.css",
    "skins/monobook/IE50Fixes.css",
    "skins/monobook/IE55Fixes.css",
    "skins/monobook/IE60Fixes.css",
    "skins/monobook/IE70Fixes.css",
    "skins/common/IEFixes.js",
    "skins/common/wikibits.js",
    "raw/gen.js",
    "raw/MediaWiki_Common.css",
    "raw/MediaWiki_Monobook.css",
    "raw/gen.css",

    # logos, gifs and other pictures
    "skins/common/images/poweredby_mediawiki_88x31.png",
    "skins/monobook/headbg.jpg",
    "skins/monobook/bullet.gif",
    "skins/monobook/discussionitem_icon.gif",
    "skins/monobook/external.png"
]


# all sets we need to log all links and remove the trash from the golden ones
internals = set()
externals = set()
critical = set()

# contains already scanned urls
crawled = set()



def collect_all_links(page_url: str):
    # create a set for all farmed urls on a single page
    urls = set()

    # get base domain name
    domain_name = urlparse(page_url).netloc

    # initialize soup and parse content for <a>-elements
    soup = BeautifulSoup(requests.get(page_url, headers=HEADERS).content, "html.parser")

    for a_tag in soup.findAll("a"):
        # search through href tags for pattern and apply some fixes
        href = a_tag.attrs.get("href")

        # skip empty hrefs or page internal redirects with no use
        if href == "" or href is None or href[0] == "#":
            continue

        # some formatting hotfixes
        url = href
        url = url.replace("http://localhost../", "https://team.sa-mp.com/")
        url = url.replace("../wiki/", "https://team.sa-mp.com/wiki/")
        url = url.replace("../upload/", "https://team.sa-mp.com/upload/")
        url = url.replace("../wiki-archive.html",
                          "https://team.sa-mp.com/wiki-archive.html")
        url = url.replace("http://wiki.sa-mp.com", "https://team.sa-mp.com")
        url = url.replace("https://wiki.sa-mp.com", "https://team.sa-mp.com")

        if url[0:5] == "wiki/":
            url = "https://team.sa-mp.com/" + url

        url = url.replace("http://", "https://")

        url = url.replace("https:/team", "https://team")

        # check if an url is not valid:
        if url[0:8] != "https://":
            print(f"{RED}[CRITICAL] {url}")
            critical.add(url)

        # skip if already in set, don't waste time
        if url in internals:
            continue

        # domain name does not include internal url base -> external list
        if domain_name not in url:
            if url not in externals:
                print(f"{YELLOW}[EXTERNAL] {url} added to set!")
                externals.add(url)
            continue

        # it cannot be anything else than an internal link so add it to list
        print(f"{GREEN}[INTERNAL] {url} added to set!")
        internals.add(url)

        # add to urls for return value
        urls.add(url)

    return urls


def crawl(url: str):
    # only crawl pages with .html at the end to avoid unnecessary errors
    if ".html" not in url:
        return

    print(f"{GRAY}[CRAWLING] {url}{RESET}")

    links = collect_all_links(url)

    for link in links:
        if link in crawled:
            continue

        crawled.add(url)
        crawl(link)
        sleep(SLEEPING)


def create_directory(line: str, prefix=True):
    # remove link to get pure structure
    link = line.replace("https://team.sa-mp.com/", "")
    data = link.split("/")

    # create path from list elements
    if prefix is True:
        path = PREFIX + "/".join(data[0:-1])
    else:
        if len(data) > 1:
            path = "/".join(data[0:-1])
        else:
            path = link

    # 90% sure it's not needed but does it really hurt?
    path = path.replace("\n", "")

    # in some cases it detects an index.php - just prevent problems
    if path == "" or ".php" in path:
        return

    # create all folders given in path - be careful modifying PREFIX!
    if os.path.isdir(path) is False:
        os.makedirs(path)


def print_complete_msg():
    print("|--------------------------------|")
    print("|            COMPLETED           |")
    print("|--------------------------------|")


def main():
    print("> Please provie a number for the action you want to choose: ")
    print("* 1) Search all links from original SA:MP Wiki")
    print("* 2) Create folder structure from internals.txt file")
    print("* 3) Download all contents")
    print("NOTE: All these options can take a very long time",
          "- keep that in mind.")

    decision = None

    while type(decision) is not int:
        try:
            decision = int(input("Selection (1-3): "))
        except ValueError:
            print("ERROR: Please choose between 1, 2 and 3!")

        if type(decision) == int:
            if bool(1 <= decision <= 3) is False:
                decision = None
                print("ERROR: Please choose between 1, 2 and 3!")

    # User input: 1
    if decision == 1:
        crawl(WIKIURL)

        internals_file = open("internals.txt", "a")
        for link in internals:
            internals_file.write(link + "\n")
        internals_file.close()

        externals_file = open("externals.txt", "a")
        for link in externals:
            externals_file.write(link + "\n")
        externals_file.close()

        others_file = open("others.txt", "a")
        for link in critical:
            others_file.write(link + "\n")
        others_file.close()

        print_complete_msg()

    # User input: 2
    elif decision == 2:
        # take data from internals.txt file because there are all links
        internals_file = open("internals.txt", "r")
        lines = internals_file.readlines()

        # scan, format and create directory path for makedirs()
        for line in lines:
            create_directory(line)

        internals_file.close()

        # create directory structure for hardcoded elements
        for asset in assets:
            create_directory(asset)

        print_complete_msg()

    # User input: 3
    elif decision == 3:
        # create directory "logs" in current directory for all output files
        create_directory("logs", False)

        error_file = open("logs/download_errors.txt", "a")
        success_file = open("logs/download_success.txt", "a")
        skipped_file = open("logs/download_skipped.txt", "a")

        # take data from internals.txt file because there are all links
        internals_file = open("internals.txt", "r")
        lines = internals_file.readlines()
        internals_file.close()

        for asset in assets:
            lines.insert(0, "https://team.sa-mp.com/" + asset)

        for line in lines:

            # format url-path to my desires for saving location
            path = unquote(line.replace("https://team.sa-mp.com/", ""))
            path = path.replace("\n", "")
            path = PREFIX + path

            # remove \n for cleaner outputs :)
            line = line.replace("\n", "")

            # links with # inside are most likely not a real page ;)
            if "#" in line:
                print(f"{GRAY}{line} probably not a page - skipped!{RESET}")
                skipped_file.write(f"{line}\n")
                continue

            # skip file if it exists
            if os.path.isfile(path):
                print(f"{GRAY}{line} already exists - skipped!{RESET}")
                skipped_file.write(f"{line}\n")
                continue

            # SHORT BREAK to
            sleep(SLEEPING)

            # try to get page data in byte format
            try:
                print(f"{YELLOW}Downloading {line}...{RESET}")
                rq = Request(line)
                rq.add_header('User-Agent', 'samp-wiki-scraper')
                resource = urlopen(rq)
                content = resource.read()
            except HTTPError:
                print(f"{RED}{line} could not be downloaded!{RESET}")
                error_file.write(f"{line}\n")
                continue

            # original script contained UnicodeError tracking - changed from
            # utf-8 to reading and writing bytes what works just fine
            # so no error handling needed, hopefully...
            file = open(path, "wb")

            file.write(content)

            file.close()

            print(f"{GREEN}Download completed!{RESET}")
            success_file.write(f"{line}\n")

        error_file.close()
        success_file.close()
        skipped_file.close()

        print_complete_msg()


if __name__ == "__main__":
    main()
