#!/usr/bin/env python3
import os
import sys
import pikepdf
from urllib import request
from urllib.parse import unquote

'''Use archiveweb
https://github.com/g0ttfrid/archiveweb
python3 archiveweb.py -t <target> -x pdf

python3 metadata-pdf.py <output_archiveweb>
'''

list_urls = sys.argv[1]

with open(list_urls) as f:
    urls = f.readlines()
    for i in urls:
        url = unquote(i.rstrip())
        
        try:
            filename = "temporary_file"
            request.urlretrieve(url, filename)
            with pikepdf.Pdf.open(filename) as pdf:
                print(f"\n[{url}]")
                docinfo = pdf.docinfo
                for key, value in docinfo.items():
                    print(f"{key} : {value}")
                os.remove(filename)
                print("\n")
        except:
            if os.path.exists(filename): os.remove(filename)
            pass
