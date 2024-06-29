import requests
import argparse
import urllib3

urllib3.disable_warnings()

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domain', type=str, required=True)
	return parser.parse_args()

def subdomains(target):
    print('\n[+] certspotter + crt.sh\n')
    target = target.strip()
    data = set()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    try:
        r = requests.get(f'https://api.certspotter.com/v1/issuances?domain={target}&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert', headers=headers, timeout=(10), verify=False)
    except Exception:
        print('[!] could not connect to certspotter')
    
    try:
        for (key,value) in enumerate(r.json()):
            for name in value['dns_names']:
                if '*' not in name and target in name: data.add(name)
    except Exception as err:
        print(err)

    try:
        r = requests.get(f'https://crt.sh/?q=%.{target}&output=json', headers=headers, timeout=(10), verify=False)
    except Exception:
        print('[!] could not connect to crt.sh')

    try:
        for (key,value) in enumerate(r.json()):
            if '\n' in value['name_value']:
                for name in value['name_value'].split(sep='\n'):
                    if '*' not in name and target in name: data.add(name)
            else:
                if '*' not in value['name_value']: data.add(value['name_value'])
    except Exception as err:
        print(f'[!] {err}')

    return sorted(data)

if __name__ == '__main__':
    try:
        args = parse_args()
        print(*subdomains(args.domain), sep='\n')
    except KeyboardInterrupt:
        print('[!] Stopping')
