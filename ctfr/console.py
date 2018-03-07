import argparse
from pyfiglet import figlet_format
from ctfr import get_domains


def print_banner():
    """ Render and print the banner """

    banner = []
    banner.append("____ _____ _____ ____")
    banner.append("/ ___|_   _|  ___|  _ \\")
    banner.append("| |     | | | |_  | |_) |")
    banner.append("| |___  | | |  _| |  _ < ")
    banner.append("\____| |_| |_|   |_| \_\\")
    banner.append("Version {v} - Hey don't miss AXFR!")
    banner.append("Made by Sheila A. Berta (UnaPibaGeek)")
    print('\r\n'.join(map(lambda x: x.center(35), banner)))


def main():
    """ main function for the program """

    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str,
                        required=True, help="Target domain.")
    parser.add_argument('-o', '--output', type=str, help="Output file.")

    args = parser.parse_args()

    hosts = get_hostnames(args.domain)

    print("[!] ---- TARGET: {d} ---- [!] \n".format(d=args.domain))
    for host in hosts:
        print("[-]  {s}".format(s=host))

    if args.output is not None:
        with open(args.output,"w+") as f:
            f.write('\n'.join(hosts))
            f.close()

    print("\n[!]Done")
