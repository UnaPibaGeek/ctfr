#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
    CTFR - 011.01.19.15.25.00 - Sheila A. Berta (UnaPibaGeek)
------------------------------------------------------------------------------

# ## LIBRARIES ## #
"""
import re
import json
import requests
from requests import Session
import argparse

try:
    from bs4 import BeautifulSoup
    bs4_present = True
except ImportError:
    bs4_present = False

# ## CONTEXT VARIABLES ## #
version = 2.0

# ## MAIN FUNCTIONS ## #


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
    parser.add_argument('-a', '--alt', action='store_true', help="Alternate domains. Takes longer to complete.")
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
    return re.sub('.*www\.', '', target, 1).split('/')[0].strip()


def save_subdomains(subdomain, output_file):
    with open(output_file, "a") as f:
        f.write(subdomain + '\n')
        f.close()


def grab_alt_detail(alternate_domains, subdomains, cert_ids, existing_domains, new_domains, output):
    if alternate_domains and bs4_present:
        print("\n[!] ---- ADDITIONAL DOMAIN SEARCH ---- [!] \n")
        print("  (this could take quite a while for sites with hundreds of subdomains...)\n")

        cert_queue = set()
        sub_queue = dict()
        for subdomain in subdomains:
            sub_queue[subdomain] = 0
        for cid in cert_ids:
            if cid['min_cert_id'] > sub_queue[cid['name_value']]:
                sub_queue[cid['name_value']] = cid['min_cert_id']
        for subdomain in sub_queue.keys():
            cert_queue.add(sub_queue[subdomain])
        cert_queue = sorted(cert_queue)
        additional_domains = set()
        for cert in cert_queue:
            with Session() as rsess:
                crt_id_url = "https://crt.sh/?id={}".format(cert)
                headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                         "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                           "referer": crt_id_url}
                req = rsess.get(crt_id_url, headers=headers)
                rawhtml = req.text
                soup = BeautifulSoup(rawhtml, features="html.parser")
                body = soup.html.body
                crt_links = body.select('a')
                cen_url = raw_url = None
                for link in crt_links:
                    try:
                        crt_tmp = link.attrs['href']
                        if crt_tmp.startswith('//censys.io/certificates/'):
                            cen_url = "https:{}".format(crt_tmp)
                            raw_url = "{}/raw".format(cen_url)
                            break
                        else:
                            continue
                    except KeyError:
                        continue
                if cen_url is not None:
                    # first_ref = "https://censys.io/certificates/{}".format(cert)
                    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                             "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                               "referer": cen_url}
                    # first_url = "https://censys.io/certificates/{}/raw".format(cert)
                    req = rsess.get(raw_url, headers=headers)
                    rawhtml = req.text
                    soup = BeautifulSoup(rawhtml, features="html.parser")
                    json_chunk = soup.select_one('code[class="json"]')
                    try:
                        jsontxt = json_chunk.text
                    except AttributeError:
                        continue
                    json_data = json.loads(jsontxt)
                    try:
                        for name in json_data['parsed']['names']:
                            if name in existing_domains:
                                continue
                            new_domains.add(name)
                            if name not in subdomains:
                                subdomains.append(name)
                                additional_domains.add(name)
                                print("[-]  {s}".format(s=name))
                                if output is not None:
                                    save_subdomains(name, output)
                                    existing_domains.add(name)
                    except KeyError:
                        pass

        additional_domains = sorted(additional_domains)

        print("\n[!] ---- ADDITIONAL DOMAINS FOUND: {d} ---- [!]".format(d=len(additional_domains)))

    elif alternate_domains and not bs4_present:
        print("BeautifulSoup 4 not installed. Ignoring any -a/--alt switches.")
        print("If you wish to parse additional details, try 'pip install beautifulsoup4' and run script again.")
    return new_domains


def main():
    banner()
    args = parse_args()

    subdomains = list()
    cert_ids = list()

    target = clear_url(args.domain)
    output = args.output
    alternate_domains = args.alt
    existing_domains = set()
    new_domains = set()

    if output is not None:
        try:
            with open(output, "r") as f:
                file_domains = f.readlines()
                for fd in file_domains:
                    existing_domains.add(fd.strip())
            print("Found", len(existing_domains), "domains in the", target, "file. Appending any new ones we find.")
        except FileNotFoundError:
            pass

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    if req.status_code != 200:
        print("[X] Information not available!")
        exit(1)

    json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

    # json.loads seems to now return a list, which resulted in nesting and broke the 'for' loop.
    # rewrote with a try/except loop to maintain compatibility with previous versions.
    try:
        for (key, value) in enumerate(json_data):
            subdomains.append(value['name_value'])
            cert_ids.append(value)
    except TypeError:
        json_data = json.loads('{}'.format(req.text.replace('}{', '},{')))
        for (key, value) in enumerate(json_data):
            subdomains.append(value['name_value'])
            cert_ids.append(value)

    print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

    subdomains = sorted(set(subdomains))

    for subdomain in subdomains:
        if subdomain in existing_domains:
            continue
        print("[-]  {s}".format(s=subdomain))
        new_domains.add(subdomain)
        if output is not None:
            save_subdomains(subdomain, output)
            existing_domains.add(subdomain)

    print("\n[!] ---- NEW DOMAINS FOUND: {d} ---- [!] \n".format(d=len(new_domains)))

    new_domains = grab_alt_detail(alternate_domains, subdomains, cert_ids, existing_domains, new_domains, output)

    print("\n\n[!] ---- TOTAL NEW DOMAINS FOUND: {d} ---- [!]".format(d=len(new_domains)))
    print("\n[!]  Done. Have a nice day! ;).")


try:
    main()
except KeyboardInterrupt:
    print("Keyboard Interrupt detected, exiting program.  Have a great day!")
