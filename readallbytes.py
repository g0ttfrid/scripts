#!/usr/bin/env python3
import base64
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

# https://github.com/FortyNorthSecurity/RandomScripts/blob/main/Cobalt%20Scripts/shellcode_formatter.py

def parse_args():
    parser = ArgumentParser(usage='python3 readallbytes.py -b shellcode.bin -f csharp', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-b', '--bin', required=True, help="Binary file")
    parser.add_argument('-f', '--format', type=str, required=True, help="shellcode = Standard shellcode format\n"
    "blob_b64 = Binary blob base64 encoded\n"
    "csharp = C# formatted shellcode\n"
    "csharp_b64 = Base64 encoded C# shellcode")
    return parser.parse_args()

def formatter(bin, format):
    try:
        with open(bin, "rb") as f:
            data = f.read()
    except:
        print('[!] Error while opening the file!')  

    try:
        encoded_raw = base64.b64encode(data)
        binary_code = ''
        for byte in data:
            binary_code += "\\x" + hex(byte)[2:].zfill(2)
        cs = "0" + ",0".join(binary_code.split("\\")[1:])
        csharp = f"static byte[] buf = new byte[{cs.count('x')}] {{ {cs} }};"
        encoded_cs = base64.b64encode(csharp.encode())
    except:
        print('[!] Error formatting the file!')
    
    if format == "shellcode":
        print("[+] Standard shellcode format:\n")
        print(binary_code)
    elif format == "blob_b64":
        print("[+] Binary blob base64 encoded:\n")
        print(encoded_raw.decode('ascii'))
    elif format == "csharp":
        print("[+] C# formatted shellcode:\n")
        print(csharp)
    elif format == "csharp_b64":
        print("[+] Base64 encoded C# shellcode:\n")
        print(encoded_cs.decode('ascii'))
    else:
        print("[!] Output format not found!")

if __name__ == '__main__':
    args = parse_args()
    formatter(args.bin, args.format)
