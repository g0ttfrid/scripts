#!/usr/bin/env python3
import base64
import hashlib
from Crypto.Cipher import AES
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
	"xor = Xor encrypt shellcode\n"
	"aes = AES encrypt shellcode")
	return parser.parse_args()

def pad(s):
	return s + bytes((AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size), encoding='utf-8')

def aesenc(plaintext):
	key = urandom(16)
	k = hashlib.sha256(key).digest()
	iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	plaintext = pad(plaintext)
	cipher = AES.new(k, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(bytes(plaintext))

	print('AESkey[] = { 0x' + ',0x'.join(hex(x)[2:] for x in key) + ' };')
	output = 'payload[] = { 0x' + ',0x'.join(hex(x)[2:] for x in ciphertext) + ' };'
	
	return output

def xor(data):
	key = base64.b64encode(urandom(16)).decode('utf-8')
	print(f"key: {key}")
	print(f"len: {len(data)}\n")
	l = len(key)
	output = ""

	for i in range(len(data)):
		current = data[i]
		current_key = key[i % len(key)]
		output += chr(current ^ ord(current_key))
	
	output = '{ 0x' + ',0x'.join(hex(ord(x))[2:] for x in output) + ' };'
	
	return output

def formatter(bin, format):
	try:
		data = open(bin, "rb").read()
	except:
		print('[!] Error while opening the file!')
		exit()

	try:
		binary_code = ''
		for byte in data:
			binary_code += "\\x" + hex(byte)[2:].zfill(2)
	except:
		print('[!] Error formatting the bytes!')
		exit()
	
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
	elif format == "aes":
		print("[+] AES encrypt shellcode:\n")
		print(aesenc(data))
	else:
		print("[!] Output format not found!")
		exit()

if __name__ == '__main__':
	try:
		args = parse_args()
		formatter(args.bin, args.format)
	except KeyboardInterrupt:
		print('[!] Stopping') 
