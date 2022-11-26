import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import colorama
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value,
                     OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100)


user_agent = user_agent_rotator.get_random_user_agent()


px = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
headers = {'User-Agent': user_agent}
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED


url = "http://metapress.htb/"

domain_name = urlparse(url).netloc

allLinks = set()
visited = set()
external_urls = set()


def is_valid(url):

    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def getUrls(url):
    if (is_valid(url)):
        visited.add(url)
        if len(allLinks) == len(visited):
            return

        body = requests.get(url, headers=headers)
        soup = BeautifulSoup(body.content.decode(), 'html.parser')

        a = soup.find_all("a")
        link = soup.find_all("link")
        scripts = soup.find_all("script")

        for href in a:
            if 'href' in href.attrs:

                href = href['href']
                href = urljoin(url, href)
                allLinks.add(href)

        for lhref in link:
            if 'href' in lhref.attrs:
                href = urljoin(url, lhref['href'])
                allLinks.add(href)

        for l in [link['src'] for link in scripts if 'src' in link.attrs]:
            allLinks.add(l)


getUrls(url)


for url in allLinks.copy():
    if domain_name not in url:
        # external link
        if url not in external_urls:
            external_urls.add(url)
            print(f"{GRAY}[!] External link: {url}{RESET}")
            continue
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    if ".png" in url:
        continue
    getUrls(url)


for i in allLinks:
    print(f"{GREEN} {i}{RESET}")

i = len(allLinks)
e = len(external_urls)
a = len(external_urls) + len(visited)

print("[+] Total Internal links:", f'{RED}{i}{RESET}')
print("[+] Total External links:", f'{RED}{e}{RESET}')
print("[+] Total URLs:", f'{RED}{a}{RESET}')
