import socket
import argparse
import re
import requests
from bs4 import BeautifulSoup

class UrlFetcher:
    @staticmethod
    def fetch(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()
                print(text)
            elif response.status_code in {301, 302}:
                print(f"Redirected to: {response.headers['Location']}")
            else:
                print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching URL: {url}. Exception: {e}")

class GoogleSearcher:
    @staticmethod
    def search(query):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('www.google.com', 80)
        sock.connect(server_address)
        sock.settimeout(5)
        request = f"GET /search?q={query.replace(' ', '+')} HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
        sock.sendall(request.encode())
        response = ''
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data.decode('latin-1')
        except socket.timeout:
            pass
        sock.close()

        links = re.findall(r'<a href="/url\?q=(.*?)&amp;', response)
        titles = re.findall(r'class="BNeawe vvjwJb AP7Wnd">(.*?)</div>', response)

        for i in range(10):
            if i < len(titles) and i < len(links):
                print("Title:", titles[i])
                print("Link:", links[i])
                print()
        
        user_input = int(input("Please enter the number of the site you want to be redirected to: "))
        UrlFetcher.fetch(links[user_input])

def main():
    parser = argparse.ArgumentParser(description='Simple CLI for HTTP Requests and Search')
    parser.add_argument('-u', '--url', help='Fetch content from URL')
    parser.add_argument('-s', '--search', help='Search term')

    args = parser.parse_args()

    if args.search:
        GoogleSearcher.search(args.search)
    elif args.url:
        UrlFetcher.fetch(args.url)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
