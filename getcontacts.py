import urllib3
import time
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings()

def search(dork, proxy=None):
    print(f'\n\n[+] dork: {dork.rstrip()}')
    print('+ Google dorks')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    if proxy:
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    else:
        proxies = None

    cont = 0

    while True:
        time.sleep(3.0)

        try:
            r = requests.get(f'https://www.google.com/search?q=site:linkedin.com/in+"{dork}"&num=50&start={cont}', headers=headers, proxies=proxies, timeout=(5), verify=False)
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f'\n[!] Error connection:\n{err}')
            break
        
        if 'encontrou nenhum documento correspondente.' in r.text:
            break
        
        try:
            bs = BeautifulSoup(r.text, 'html.parser')
            for link in bs.find_all('h3'):
                if ' Linked' in link.text: print(link.text)
        except AttributeError as err:
            print(f'\n[!] Error scrap:\n{err}')
            return None

        cont += 50
    
if __name__ == '__main__':
    try:
        search('<target>')
    except KeyboardInterrupt:
        print('[!] Stopping')
