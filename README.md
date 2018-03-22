# CTFR
Do you miss AXFR technique? This tool allows to get the subdomains from a HTTP**S** website in a few seconds.  
How it works? CTFR does not use neither dictionary attack nor brute-force, it just abuses of Certificate Transparency logs.  
For more information about CT logs, check www.certificate-transparency.org and [crt.sh](https://crt.sh/).

## Getting Started
Please, follow the instructions below for installing and run CTFR.

### Pre-requisites
Make sure you have installed the following tools:
```
Python 3.0 or later.
pip3 (sudo apt-get install python3-pip).
```

### Installing
```bash
$ git clone https://github.com/UnaPibaGeek/ctfr.git
$ cd ctfr
$ pip3 install -r requirements.txt
```

### Running
```bash
$ python3 ctfr.py --help
```


## Usage
Parameters and examples of use.

### Parameters
```
-d --domain [target_domain] (required)
-o --output [output_file] (optional)
```

### Examples
```bash
$ python3 ctfr.py -d starbucks.com
```
```bash
$ python3 ctfr.py -d facebook.com -o /home/shei/subdomains_fb.txt
```

### Use through a proxy
Just uncomment and modify variables 'http' and 'https' from 'proxies' array:
```
	proxies = {
#		Uncomment 'http' and 'https' variables if you need:
#		'http': 'http://username:password@hostname:port',
#		'https': 'http://username:password@hostname:port',
	}
```

### With Docker
I think it's a little bit crazy to use Docker for running such a little python script, but if you want to do it anyway, you can download [this lightweight (97.8MB) Docker image](https://hub.docker.com/r/johnpaulada/ctfr/) made by John Paulada.

The instructions are there.

## Screenshots
![CTFR-ST](http://www.semecayounexploit.com/CTFR/CTFR-ST.png)

![CTFR-FB](http://www.semecayounexploit.com/CTFR/CTFR-FB.png)



## Author
* *Sheila A. Berta - [(@UnaPibaGeek)](https://www.twitter.com/UnaPibaGeek).*

### Proxy support
* *Javier L. Ceron - [(@neohitokiri)](https://www.twitter.com/neohitokiri).*
