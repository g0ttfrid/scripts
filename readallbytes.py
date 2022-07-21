#!/usr/bin/env python3
import base64
import argparse

# https://github.com/FortyNorthSecurity/RandomScripts/blob/main/Cobalt%20Scripts/shellcode_formatter.py

def parse_args():
    parser = argparse.ArgumentParser(usage='python3 readallbytes.py  -f shellcode.bin')
    parser.add_argument('-b', '--bin', required=True, help="Binary file")
    parser.add_argument('-f', '--format', type=str, required=True, help="blob_b64 / shellcode / cs_shellcode / cs_b64")
    return parser.parse_args()

def formatter(bin, format):
    try:
        with open(bin, "rb") as f:
            data = f.read()
    except IOError:
        print('[!] Error while opening the file!')  

    encoded_raw = base64.b64encode(data)
    binary_code = ''
    for byte in data:
        binary_code += "\\x" + hex(byte)[2:].zfill(2)
    cs_shellcode = "0" + ",0".join(binary_code.split("\\")[1:])
    encoded_cs = base64.b64encode(cs_shellcode.encode())
    
    if format == "blob_b64":
        print("[+] Binary Blob base64 encoded:\n")
        print(encoded_raw.decode('ascii'))
    elif format == "shellcode":
        print("[+] Standard shellcode format:\n")
        print(binary_code)
    elif format == "cs_shellcode":
        print("[+] C# formatted shellcode:\n")
        print(cs_shellcode)
    elif format == "cs_b64":
        print("[+] Base64 encoded C# shellcode:\n")
        print(encoded_cs.decode('ascii'))
    else:
        print("[!] output format not found!")

if __name__ == '__main__':
    args = parse_args()
    formatter(args.bin, args.format)
