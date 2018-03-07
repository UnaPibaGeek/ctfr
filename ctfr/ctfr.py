import json
import requests

def get_hostnames(domain):
	""" query crt.sh and return an array with the list of hostnames"""
	
	hostnames = []
	try: 
		req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=domain))

		if req.status_code != 200:
			raise Exception("Invalid domain or information not available!")

		json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

		for cert in json_data:
			host = cert.get("name_value")
			if host not in hostnames:
				hostnames.append(host)
	except:
		return hostnames

	return hostnames
