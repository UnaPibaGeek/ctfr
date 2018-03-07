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

## # CONTEXT VARIABLES # ##
version = 1.1

## # MAIN FUNCTIONS # ##

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
	parser.add_argument('-o', '--output', type=str, help="Output file.")
	return parser.parse_args()

def banner():
	global version
	from pyfiglet import figlet_format
	b = figlet_format("        CTFR") + \
	'''     Version {v} - Hey don't miss AXFR!
    Made by Sheila A. Berta (UnaPibaGeek)
	'''.format(v=version)
	print(b)

def save_subdomains(subdomain,output_file):
	with open(output_file,"a") as f:
		f.write(subdomain + '\n')
		f.close()

def main():
	banner()
	args = parse_args()

	subdomains = []
	target = args.domain
	output = args.output

	req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

	if req.status_code != 200:
		print("[X] Error! Invalid domain or information not available!") 
		exit(1)

	json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

	for (key,value) in enumerate(json_data):
		subdomains.append(value['name_value'])

	
	print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

	subdomains = sorted(set(subdomains))

	for subdomain in subdomains:
		print("[-]  {s}".format(s=subdomain))
		if output is not None:
			save_subdomains(subdomain,output)

	print("\n\n[!]  Done. Have a nice day! ;).")


main()
	
