python
#!/usr/bin/env python3

import nmap
import socket
import concurrent.futures
from datetime import datetime

def scan_ports(target, ports):
    print(f"Scanning target: {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    try:
        nm = nmap.PortScanner()
        nm.scan(target, ports, arguments='-sV -O')
        print(nm.scanstats())
        print("-" * 50)

        for host in nm.all_hosts():
            print(f"Host: {host} ({nm[host].hostname()})")
            print(f"State: {nm[host].state()}")

            for proto in nm[host].all_protocols():
                print(f"Protocol: {proto}")

                lport = nm[host][proto].keys()
                for port in sorted(lport):
                    print(f"Port: {port}\tState: {nm[host][proto][port]['state']}")
                    print(f"Service: {nm[host][proto][port]['name']}")
                    print(f"Product: {nm[host][proto][port]['product']}")
                    print(f"Version: {nm[host][proto][port]['version']}")
                    print(f"Extrainfo: {nm[host][proto][port]['extrainfo']}")
                    print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")

def scan_subdomains(target):
    print(f"Scanning subdomains for: {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    try:
        with open('subdomains.txt', 'r') as file:
            subdomains = file.read().splitlines()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_subdomain, target, subdomain) for subdomain in subdomains]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"Found subdomain: {result}")

    except Exception as e:
        print(f"An error occurred: {e}")

def check_subdomain(target, subdomain):
    try:
        domain = f"{subdomain}.{target}"
        socket.gethostbyname(domain)
        return domain
    except:
        return None

if __name__ == "__main__":
    target = input("Enter target domain or IP: ")
    ports = input("Enter ports to scan (e.g., 1-1000): ")

    scan_ports(target, ports)
    scan_subdomains(target)
