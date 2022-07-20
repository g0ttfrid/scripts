#!/usr/bin/env python3
import os
import sys
import pikepdf
from wget import download
from urllib.parse import unquote

'''Use archiveweb
https://github.com/g0ttfrid/archiveweb
python3 archiveweb.py -t <target> -x pdf

python3 metadata-pdf.py <output archiveweb>
'''

list_urls = sys.argv[1]

with open(list_urls) as f:
    urls = f.readlines()
    for i in urls:
        url = unquote(i.rstrip())
        filename = "temporary_file"
        
        try:
            download(url, filename)
        except:
            pass
        
        try:
            pdf = pikepdf.Pdf.open(filename)
            docinfo = pdf.docinfo
            print(f"\n[{url}]")
            for key, value in docinfo.items():
                print(f"{key} : {value}")
            os.remove(filename)
            print("\n")
        except:
            pass
