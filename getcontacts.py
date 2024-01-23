import urllib3
import time
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from unidecode import unidecode
from fake_useragent import UserAgent
from urllib.parse import unquote

urllib3.disable_warnings()

def parse_args():
    parser = ArgumentParser(usage='python3 getcontacts.py -t "Se7en Corp"', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-t', '--target', type=str, required=True, help='insert company')
    parser.add_argument('-p', '--proxy', type=str, help='insert proxy (e.g. 127.0.0.1:8080)')
    parser.add_argument('-f', '--format', type=str, help="\n"
    "linkedin (e.g. John Doe - Serial Killer - Se7en Corp)\n"
    "firstname.lastname (e.g. john.doe)\n"
    "firstname_lastname (e.g. john_doe)\n"
    "firstnamelastname (e.g. johndoe)\n"
    "firstletterlastname (e.g. jdoe)")
    return parser.parse_args()

def linked(target, proxy=None):
    print(f'\n[+] Target: {target}')
        
    if proxy:
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    else:
        proxies = None

    data = set()
    cont = 0

    while True:
        ua = UserAgent()
        headers = {"Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": f"{ua.random}", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "X-Client-Data": "CNzeygE=", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Priority": "u=0, i", "Referer": "https://www.google.com.br"}

        try:
            r = requests.get(f'https://www.google.com.br/search?q=site:linkedin.com/in+"{target}"&num=50&start={cont}&cr=countryBR&tbs=ctr:countryBR,lr:lang_1pt&source=lnt&lr=lang_pt', headers=headers, proxies=proxies, timeout=(5), verify=False)
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f'[!] Error connection:\n{err}')
            break
        
        if 'o encontrou nenhum document' in r.text:
            break

        bs = BeautifulSoup(r.text, 'html.parser')
        for link in bs.find_all('a'):
            if 'linkedin.com' in link.text: 
                link_href = link.get('href')
                h3_text = link.find('h3').text if link.find('h3') else "Nenhum título encontrado"
                data.add(unquote(f"{h3_text} ({link_href})"))

        time.sleep(5.0)
        cont += 50
    
    return data

def generate_formats(data, format_type):
    print(f"[+] {format_type}:")

    for i in data:
        full = unidecode((i.split(' - ')[0]).lower())
        names = list(filter(lambda word: len(word) > 3 and word.isalnum(), full.split(' ')))
        c = 1
        while c < len(names):
            if format_type == "firstname.lastname":
                output.add(f"{names[0]}.{names[c]}")
            elif format_type == "firstname_lastname":
                output.add(f"{names[0]}_{names[c]}")
            elif format_type == "firstnamelastname":
                output.add(f"{names[0]}{names[c]}")
            elif format_type == "firstletterlastname":
                output.add(f"{names[0][0]}{names[c]}")
            c += 1

    return output

def logger(target, list):
    with open(f'{target}.txt', 'w', encoding='utf-8') as f:
        for line in list:
            f.write(f'{line}\n')

if __name__ == '__main__':
    try:
        args = parse_args()
        if args.proxy:
            data = linked(args.target, args.proxy)
        else:
            data = linked(args.target)

        output = set()

        if data:
            if args.format in ["firstname.lastname", "firstname_lastname", "firstnamelastname", "firstletterlastname"]:
                output = generate_formats(data, args.format)
            elif args.format == "linkedin" or args.format == None:
                print("[+] LinkedIn:")
                for i in data:
                    line = i.strip()
                    output.add(line)
            else:
                print("[!] Output format not found. \n[+] LinkedIn:")
                for i in data:
                    line = i.strip()
                    output.add(line)
                
            logger(args.target, output)
            print(*output, sep="\n")

        else:
            print(f'[!] Users not found\n')
    
    except KeyboardInterrupt:
        print('\n[!] Stopping')
