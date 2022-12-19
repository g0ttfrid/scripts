import urllib3
import time
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from unidecode import unidecode

urllib3.disable_warnings()

def parse_args():
    parser = ArgumentParser(usage='python3 getcontacts.py -t "Se7en Corp"', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-t', '--target', type=str, required=True, help='insert company')
    parser.add_argument('-f', '--format', type=str, help="\n"
    "linkedin (e.g. John Doe - Serial Killer - Se7en)\n"
    "firstname.lastname (e.g. john.doe)\n"
    "firstletterlastname (e.g. jdoe)")
    return parser.parse_args()

def linked(target, proxy=None):
    print(f'\n[+] Target: {target}')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    
    if proxy:
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    else:
        proxies = None

    data = set()
    cont = 0

    while True:
        time.sleep(3.0)

        try:
            r = requests.get(f'https://www.google.com/search?q=site:linkedin.com/in+"{target}"&num=50&start={cont}', headers=headers, proxies=proxies, timeout=(5), verify=False)
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f'\n[!] Error connection:\n{err}')
            break
        
        if 'encontrou nenhum documento correspondente.' in r.text:
            break
        
        try:
            bs = BeautifulSoup(r.text, 'html.parser')
            for link in bs.find_all('h3'):
                if ' Linked' in link.text: data.add(link.text)
        except AttributeError as err:
            print(f'\n[!] Error scrap:\n{err}')
            return None

        cont += 50
    
    return data

if __name__ == '__main__':
    try:
        args = parse_args()
        data = linked(args.target)
    except KeyboardInterrupt:
        print('\n[!] Stopping')
        
    if args.format == "linkedin" or args.format == None:
        print("[+] LinkedIn:")
        for i in data:
            line = i.strip()
            print(line)

    elif args.format == "firstname.lastname":
        print("\n[+] Firstname.Lastname (e.g. john.doe):")
        for i in data:
            line = i.strip()
            fullname = (line.split('-')[0]).lower()
            listname = fullname.split(' ')
            if len(listname[1]) < 4 and listname[2] :
                print(unidecode(f"{listname[0]}.{listname[2]}"))
            else:
                print(unidecode(f"{listname[0]}.{listname[1]}"))

    elif args.format == "firstletterlastname":
        print("\n[+] FirstletterLastname (e.g. jdoe):")
        for i in data:
            line = i.strip()
            fullname = (line.split('-')[0]).lower()
            listname = fullname.split(' ')
            if len(listname[1]) < 4 and listname[2] :
                print(unidecode(f"{listname[0][0]}{listname[2]}"))
            else:
                print(unidecode(f"{listname[0][0]}{listname[1]}"))

    else:
        print("[!] Output format not found!")
    
    
