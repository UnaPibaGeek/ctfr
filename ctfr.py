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
import socket  # Import the library to resolve IP addresses

## # CONTEXT VARIABLES # ##
version = 1.2

## # MAIN FUNCTIONS # ##

def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
        parser.add_argument('-o', '--output', type=str, help="Output file.")
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

def save_subdomains(subdomain, ip, output_file):
        with open(output_file,"a") as f:
                f.write(f"{subdomain} - {ip}\n")
                f.close()

def resolve_ip(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.error:
        return "N/A"

def main():
    banner()
    args = parse_args()

    subdomains = []
    target = clear_url(args.domain)
    output = args.output

    try:
        req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

        req.raise_for_status()  # Throw an exception if the request was not successful

        json_data = req.json()

        for (key, value) in enumerate(json_data):
            subdomain = value['name_value']
            ip = resolve_ip(subdomain)
            subdomains.append((subdomain, ip))

        print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

        subdomains = sorted(set(subdomains))

        for subdomain, ip in subdomains:
            print("[-]  {s} - {ip}".format(s=subdomain, ip=ip))
            if output is not None:
                save_subdomains(subdomain, ip, output)

        print("\n\n[!]  Done. Have a nice day! ;).")

    except requests.exceptions.HTTPError as e:
        print(f"[X] HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"[X] Request error occurred: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"[X] JSON decoding error occurred: {e}")
        print("[X] Unable to parse JSON response. Please check the response manually.")
        print("[X] Response content:")
        print(req.text)

if __name__ == "__main__":
    main()
