# PacketReaper

PacketReaper is a powerful and versatile MITM (Man-In-The-Middle) helper tool designed for Linux environments. It automates network scanning, live host discovery, ARP spoofing, and IP forwarding setup to enable effective full-duplex ARP spoofing attacks for authorized security testing.

---

## Features

- **Network scanning:** Auto-detect subnet and live scan hosts (similar to netdiscover).
- **ARP spoofing:** Launch full-duplex ARP spoofing attacks targeting chosen devices and gateways.
- **Auto IP forwarding:** Enables system IP forwarding and sets up iptables masquerade for seamless traffic flow.
- **Multi-threaded:** Runs spoofing attacks in separate threads for concurrent targeting.
- **Graceful cleanup:** Restores ARP tables, disables forwarding, and removes iptables rules on exit.
- **Vendor lookup:** Identifies MAC address vendors using the mac-vendor-lookup database.
- **Interactive menu:** Command-line interface for easy device management and attack control.
- **Logging:** Logs all actions and discovered devices for audit and review.

---

## Installation

### Requirements

- Python 3.x
- Root privileges (sudo) on Linux
- Dependencies:
  - [scapy](https://scapy.net/)
  - [netifaces](https://pypi.org/project/netifaces/)
  - [mac-vendor-lookup](https://pypi.org/project/mac-vendor-lookup/)

Install dependencies with:

```bash
pip install -r requirements.txt
