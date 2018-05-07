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
from struct import unpack
from socket import AF_INET, inet_pton

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

# Reference link: https://stackoverflow.com/questions/691045/how-do-you-determine-if-an-ip-address-is-private-in-python
# Determine if resolved IPs are private 
def lookup(ip):
    f = unpack('!I',inet_pton(AF_INET,ip))[0]
    private = (
        [ 2130706432, 4278190080 ], # 127.0.0.0,   255.0.0.0   http://tools.ietf.org/html/rfc3330
        [ 3232235520, 4294901760 ], # 192.168.0.0, 255.255.0.0 http://tools.ietf.org/html/rfc1918
        [ 2886729728, 4293918720 ], # 172.16.0.0,  255.240.0.0 http://tools.ietf.org/html/rfc1918
        [ 167772160,  4278190080 ], # 10.0.0.0,    255.0.0.0   http://tools.ietf.org/html/rfc1918
    ) 
    for net in private:
        if (f & net[1]) == net[0]:
            return True
    return False

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
        for hostname in subdomains:
          try:
            dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
            dns.resolver.default_resolver.nameservers = ['209.244.0.3', '209.244.0.4','64.6.64.6','64.6.65.6', '8.8.8.8', '8.8.4.4','84.200.69.80', '84.200.70.40', '8.26.56.26', '8.20.247.20', '208.67.222.222', '208.67.220.220','199.85.126.10', '199.85.127.10', '81.218.119.11', '209.88.198.133', '195.46.39.39', '195.46.39.40', '96.90.175.167', '193.183.98.154','208.76.50.50', '208.76.51.51', '216.146.35.35', '216.146.36.36', '37.235.1.174', '37.235.1.177', '198.101.242.72', '23.253.163.53', '77.88.8.8', '77.88.8.1', '91.239.100.100', '89.233.43.71', '74.82.42.42', '109.69.8.51']
            query = resolver.query(hostname,"A")
            ips = []            
            for ip in query:
            	ips.append(str(ip))
            	if lookup(str(ip)):
            		print("[!] Private IP address detected - {}:{} ".format(hostname,ip))
            
            # Domain Fronting check
            for i in query.response.answer:
                for j in i.items:
                    target =  j.to_text()
                    if not target.startswith("*"): 
                        if 'cloudfront' in target:
                            print("{0}:CloundFront Frontable domain found ({1})").format(hostname,target)
                        elif 'appspot.com' in target:
                            print("{0}:Google Frontable domain found ({1})").format(hostname,target)
                        elif 'msecnd.net' in target:
                            print("{0}:Azure Frontable domain found ({1})").format(hostname,target)
                        elif 'aspnetcdn.com' in target:
                            print("{0}:Azure Frontable domain found ({1})").format(hostname,target)
                        elif 'azureedge.net' in target:
                            print("{0}:Azure Frontable domain found ({1})").format(hostname,target)
                        elif 'a248.e.akamai.net' in target:
                           print("{0}:Akamai Frontable domain found ({1})").format(hostname,target)
                        elif 'secure.footprint.net' in target:
                            print("{0}:Level 3 Frontable domain found ({1})").format(hostname,target)
                        elif 'cloudflare' in target:
                            print("{0}:Cloudflare Frontable domain found ({1})").format(hostname,target)
                        elif 'unbouncepages.com' in target:
                            print("{0}:Unbounce Frontable domain found ({1})").format(hostname,target)
                        elif 'amazonaws.com' in target:
                            print("{0}:Amazon AWS Frontable domain found ({1})").format(hostname,target)
                        elif 'fastly' in target:
                            print("{0}:Fastly Frontable domain found ({1})").format(hostname,target)
          
          except KeyboardInterrupt:
          	print("[*] Caught Keyboard Interrupt! Exiting...\n")
          	exit(1)
          
          except Exception as e:
            ips = ''
          # Join all returned IPs into string
          ips = ','.join(ips)
          print("{s}:{i}".format(s=hostname,i=ips))


    # Print domains without performing DNS resolution
    else:
        for hostname in subdomains:
            print("{s}".format(s=hostname))
    
    # Save domains to output file    
    if output is not None:
        save_subdomains(subdomains,output)

	print("\n\n[!]  Done. Have a nice day! ;).")

main()
    