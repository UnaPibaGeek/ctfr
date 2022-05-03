#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
    CTFR - 04.03.18.02.10.00 - Sheila A. Berta (UnaPibaGeek)
------------------------------------------------------------------------------
"""

## # LIBRARIES # ##
import re
import requests
import sys

## # CONTEXT VARIABLES # ##
version = 1.2

## # MAIN FUNCTIONS # ##

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, help="Target domain.")
    parser.add_argument('-o', '--output', type=str, help="Output file.")
    parser.add_argument('-s', '--silent', default=False, action='store_true', help="Don't show banner")
    return parser.parse_args()

def banner():
    global version
    b = '''
          ____ _____ _____ ____  
         / ___|_   _|  ___|  _ \ 
        | |     | | | |_  | |_) |
        | |___  | | |  _| |  _ < 
         \____| |_| |_|   |_| \_\\
    
     Version {v} - Hey don't miss AXFR!
    Made by Sheila A. Berta (UnaPibaGeek)
    '''.format(v=version)
    print(b)
    
def clear_url(target):
    return re.sub('.*www\.','',target,1).split('/')[0].strip()

def save_subdomains(subdomain,output_file):
    with open(output_file,"a") as f:
        f.write(subdomain + '\n')
        f.close()

def get_subdomain(target, subdomains, silent):
    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    if req.status_code != 200:
        if not silent: print("[X] Information not available!") 
        return

    for (key,value) in enumerate(req.json()):
        subdomains.append(value['name_value'])

    if not silent: print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

    subdomains = sorted(set(subdomains))
    return subdomains

def main():
    args = parse_args()
    silent = args.silent
    if not silent: banner()
    subdomains = []

    stdin = not sys.stdin.isatty()
    output = args.output
    if args.domain: 
        target = clear_url(args.domain)
        subdomains = get_subdomain(target, subdomains, silent)
    elif stdin:
        for line in sys.stdin:
            target = clear_url(line.rstrip())
            subdomains = get_subdomain(target, subdomains, silent)
    else:
        print("No domain given. either use stdin or -d flag")
        exit(1)

    for subdomain in subdomains:
        print("{s}".format(s=subdomain))
        if output is not None:
            save_subdomains(subdomain,output)

    if not silent: print("\n\n[!]  Done. Have a nice day! ;).")


if __name__ == '__main__':
    main()
    
