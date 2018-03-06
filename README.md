# CTFR
Do you miss AXFR technique? This tool allows to get the subdomains from a HTTP**S** website in a few seconds.  
How it works? CTFR does not use neither dictionary attack nor brute-force, it just abuses of Certificate Transparency logs.  
For more information about CT logs, check www.certificate-transparency.org.

## Getting Started
Please, follow the instructions below for installing and run CTFR.

### Pre-requisites
Make sure you have installed the following tools:
```
Python 3.0 or later.
pip3 (sudo apt-get install python3-pip).
```

### Installing
```
git clone https://github.com/UnaPibaGeek/ctfr.git
cd ctfr
pip3 install -r requirements.txt
```

### Running
```
python3 ctfr.py --help
```

## Usage
Parameters and examples of use.

### Parameters
```
-d [target domain] (required)
-o [Output file] (optional)
```
