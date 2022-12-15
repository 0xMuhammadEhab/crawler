import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import colorama
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

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


url = "http://testphp.vulnweb.com/"

domain_name = urlparse(url).netloc

queue = []
visited = set()
external_urls = set()


def is_valid(url):

    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def getUrls(url):
    if (is_valid(url)):
        visited.add(url)
        if len(queue) == len(visited):
            return
        try:
            body = requests.get(url, headers=headers, timeout=3)
            soup = BeautifulSoup(body.content.decode(), 'html.parser')
            a = soup.find_all("a")
            link = soup.find_all("link")
            scripts = soup.find_all("script")

            for href in a:
                if 'href' in href.attrs:

                    href = href['href']
                    href = urljoin(url, href)
                    if href not in queue:
                        queue.append(href)

            for lhref in link:
                if 'href' in lhref.attrs:
                    href = urljoin(url, lhref['href'])
                    if href not in queue:
                        queue.append(href)

            for l in [link['src'] for link in scripts if 'src' in link.attrs]:
                if l not in queue:
                    queue.append(l)

        except requests.exceptions.RequestException as err:
            print("[!!] OOps: Something Else", f'{RED}{err} in {url}')
        except requests.exceptions.HTTPError as errh:
            print("{RED}{RESET}[!!] Http Error:", f'{RED}{errh} in {url}')
        except requests.exceptions.ConnectionError as errc:
            print("{RED}{RESET}[!!] Error Connecting:",f'{RED}{errc} in {url}')
        except requests.exceptions.Timeout as errt:
            print("{RED}{RESET}[!!] Timeout Error: ", f'{RED}{errt} in {url}')


getUrls(url)


for url in queue:
    if domain_name not in url:
        # external link
        if url not in external_urls:
            external_urls.add(url)
            print(f"{GRAY}[!] External link: {url}{RESET}")
            continue
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    if ".png" in url or ".jpg" in url or "jpeg" in url or ".ico" or woff2 or woff in url:
        visited.add(url)
        continue
    getUrls(url)


for i in queue:
    print(f"{GREEN} {i}{RESET}")

i = len(queue)
e = len(external_urls)
a = len(external_urls) + len(queue)

print("[+] Total Internal links:", f'{RED}{i}{RESET}')
print("[+] Total External links:", f'{RED}{e}{RESET}')
print("[+] Total URLs:", f'{RED}{a}{RESET}')
