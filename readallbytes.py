#!/usr/bin/env python3
import base64
from os import urandom
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

'''
inspired by
- https://github.com/FortyNorthSecurity/RandomScripts/blob/main/Cobalt%20Scripts/shellcode_formatter.py
- scripts Sektor7
'''

def parse_args():
	parser = ArgumentParser(usage='python3 readallbytes.py -b shellcode.bin -f csharp', formatter_class=RawTextHelpFormatter)
	parser.add_argument('-b', '--bin', required=True, help="Binary file")
	parser.add_argument('-f', '--format', type=str, required=True, help="\n"
	"shellcode = Standard shellcode format\n"
	"base64 = Binary blob base64 encoded\n"
	"csharp = C# formatted shellcode\n"
	"nim = Nim formatted shellcode\n"
	"xor = Xor encrypt shellcode")
	return parser.parse_args()

def xor(data):
	
	key = base64.b64encode(urandom(16)).decode('utf-8')
	print(f"key: {key}")
	print(f"len: {len(data)}\n")
	l = len(key)
	output_str = ""

	for i in range(len(data)):
		current = data[i]
		current_key = key[i % len(key)]
		output_str += chr(current ^ ord(current_key))
	
	output_str = '{ 0x' + ',0x'.join(hex(ord(x))[2:] for x in output_str) + ' };'
	return output_str

def formatter(bin, format):
	try:
		data = open(bin, "rb").read()
	except:
		print('[!] Error while opening the file!')
		sys.exit()

	try:
		binary_code = ''
		for byte in data:
			binary_code += "\\x" + hex(byte)[2:].zfill(2)
	except:
		print('[!] Error formatting the file!')
	
	if format == "shellcode":
		print("[+] Standard shellcode format:\n")
		print(binary_code)
	elif format == "base64":
		print("[+] Binary blob base64 encoded:\n")
		encoded_raw = base64.b64encode(data)
		print(encoded_raw.decode('ascii'))
	elif format == "csharp":
		print("[+] C# formatted shellcode:\n")
		sc = "0" + ",0".join(binary_code.split("\\")[1:])
		csharp = f"byte[] buf = new byte[{len(data)}] {{ {sc} }};"
		print(csharp)
	elif format == "nim":
		print("[+] Nim formatted shellcode:\n")
		sc = "0" + ",0".join(binary_code.split("\\")[1:])
		nim = f"var buf: array[{len(data)}, byte] = [byte {sc}]"
		print(nim)
	elif format == "xor":
		print("[+] Xor encrypt shellcode:\n")
		print(xor(data))
	else:
		print("[!] Output format not found!")

if __name__ == '__main__':
	args = parse_args()
	formatter(args.bin, args.format)
