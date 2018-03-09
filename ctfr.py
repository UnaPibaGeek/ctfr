#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
    CTFR - 04.03.18.02.10.00 - Sheila A. Berta (UnaPibaGeek)
------------------------------------------------------------------------------
"""

## # LIBRARIES # ##
import json
import requests
import dns.resolver

## # CONTEXT VARIABLES # ##
version = 1.1

## # MAIN FUNCTIONS # ##

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
    parser.add_argument('-o', '--output', type=str, help="Output file.")
    parser.add_argument('-r', '--resolve', action='store_true', help="Perform DNS Name Resolution.")

    return parser.parse_args()

def banner():
    global version
    from pyfiglet import figlet_format
    b = figlet_format("        CTFR") + \
    '''     Version {v} - Hey don't miss AXFR!
    Made by Sheila A. Berta (UnaPibaGeek)
    '''.format(v=version)
    print(b)

def save_subdomains(subdomains,output_file):
    with open(output_file,"a") as f:
        for subdomain in subdomains:
	        f.write(subdomain + '\n')

def main():
    banner()
    args = parse_args()

    subdomains = []
    target = args.domain
    output = args.output
    resolve = args.resolve

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    if req.status_code != 200:
        print("[-] Error! Invalid domain or information not available!") 
        exit(1)

    json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

    for (key,value) in enumerate(json_data):
        subdomains.append(value['name_value'])

    
    print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

    subdomains = sorted(set(subdomains))

   # Perform DNS resolution
    if resolve is not False:
        resolver = dns.resolver.Resolver()
        for subdomain in subdomains:
          try:
            response = resolver.query(subdomain,"A")
            ips = []            
            for ip in response:
            	ips.append(str(ip))
          except KeyboardInterrupt:
          	print("[*] Caught Keyboard Interrupt! Exiting...\n")
          	exit(1)
          except:
            ips = ''
          # Join all returned IPs into string
          ips = ','.join(ips)
          print("{s}:{i}".format(s=subdomain,i=ips))
          

    # Print domains without performing DNS resolution
    else:
        for subdomain in subdomains:
            print("{s}".format(s=subdomain))
    
    # Save domains to output file    
    if output is not None:
        save_subdomains(subdomains,output)

	print("\n\n[!]  Done. Have a nice day! ;).")

main()
    