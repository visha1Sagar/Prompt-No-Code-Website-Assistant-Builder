import requests
import argparse
from termcolor import colored
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin

class WebCrawler:
    def __init__(self, url, max_depth):
        self.url = url
        self.max_depth = max_depth
        self.subdomains = set()
        self.links = set()
        self.jsfiles = set()
        
        
    def print_banner(self):
        print("-" * 80)
        print(colored(f"Recursive Web Crawler starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'cyan', attrs=['bold']))
        print("-" * 80)
        print(f"[*] URL".ljust(20, " "), ":", self.url)
        print(f"[*] Max Depth".ljust(20, " "), ":", self.max_depth)
        print("-" * 80)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', help="Specify the URL, provide it along http/https", required=True)
    parser.add_argument('-d', '--depth', dest='depth', type=int, default=1, help="Specify the recursion depth limit")
    return parser.parse_args()











if __name__ == "__main__":
    args = get_args()
    web_crawler = WebCrawler(args.url, args.depth)
    web_crawler.print_banner()
    web_crawler.start_crawling()
    web_crawler.print_results()