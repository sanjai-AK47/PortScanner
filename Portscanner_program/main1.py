import nmap
import argparse
import re
import os
import asyncio
import concurrent.futures
from colorama import Fore, Style

# Define the banner function
def banner():
    print(Fore.GREEN + "****************")
    print(Fore.GREEN + "**      Sanjai Port Scanner          **")
    print(Fore.GREEN + "****************" + Style.RESET_ALL)

# Call the banner function
banner()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Input file containing list of hostnames", required=True)
parser.add_argument("-p", "--ports", help="Comma-separated list of ports to scan. Default is 1-1000", default="1-1000")
parser.add_argument("-o", "--output", help="Output format for scan results. Default is text", choices=["text", "xml", "json", "csv"], default="text")
parser.add_argument("-t", "--threads", help="Number of threads to use for scanning. Default is 1", type=int, default=1)
args = parser.parse_args()

# read the list of hostnames from the input file
with open(args.file, 'r') as f:
    hostnames = f.readlines()

# remove whitespace characters like `\n` at the end of each line
hostnames = [x.strip() for x in hostnames]

# create an nmap scanner object
nm = nmap.PortScanner()

# create a directory for the scan results if it doesn't already exist
if not os.path.exists('scan_results'):
    os.mkdir('scan_results')

async def scan_host(hostname):
    try:
        print(Fore.GREEN + f"Scanning {hostname}..." + Style.RESET_ALL)
        hostname_escaped = re.sub('[^0-9a-zA-Z.-]', '\\\\' + '\\g<0>', hostname) # escape special characters in the hostname
        nm.scan(hostname_escaped, arguments=f'-sV -p {args.ports}')  # use the -sV option to enable service/version detection and scan the specified ports
        if args.output == "text":
            with open(f'scan_results/{hostname}.txt', 'w') as f:
                f.write(f"Scan results for {hostname}:\n")
                f.write(nm[hostname_escaped].get('tcp', ''))
        else:
            with open(f'scan_results/{hostname}.{args.output}', 'w') as f:
                f.write(nm[hostname_escaped].get_nmap_last_output())
    except Exception as e:
        print(Fore.RED + f"Error scanning {hostname}: {e}" + Style.RESET_ALL)

async def main():
    tasks = [asyncio.create_task(scan_host(hostname)) for hostname in hostnames]
    await asyncio.gather(*tasks)

asyncio.run(main())
