import scapy.all as scapy
import time
import subprocess
import ipaddress

NETWORK = "192.168.1.0/24"
INTERVAL = 30  # seconds
mapping = {
    '11:22:22:33:44:55': 'John Mobile',
    '66:77:88:99:11:22': 'Eric PC',
    '33:44:55:66:77:88': 'Bob Mobile'
}


def scan(ip):
    # Use a set object to store the MAC addresses of the devices
    macs = set()

    # Create an ARP request packet
    arp_request = scapy.ARP(pdst=ip)

    # Create an Ethernet packet with a broadcast destination MAC address
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    # Combine the Ethernet and ARP request packets
    arp_request_broadcast = broadcast/arp_request

    # Send the packet and get the response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Iterate over the hosts in the response
    for host in answered_list:
        # Check if the host's IP address is not the default gateway
        if host[1].psrc != "192.168.1.1":
            # Add the host's MAC address to the set of MAC addresses
            macs.add(host[1].src)

    # Return the set of MAC addresses
    return macs


def connection_change(hosts, action):
    # Validate the action
    if action not in ("connected", "disconnected"):
        raise ValueError(f"Invalid action: {action}")

    # Iterate over the hosts in the set
    for host in hosts:
        # Check if the host's MAC address is in the mapping
        if host in mapping:
            device = mapping[host]  # Get the device name
        else:
            device = 'unknown device'  # Use a default name

        # Create the command to run
        if action == 'connected':
            cmd = ["echo", f"{device} connected", "|", "cscript", "C:\\Progra~1\\Jampal\\ptts.vbs"]
        else:
            cmd = ["echo", f"{device} disconnected", "|", "cscript", "C:\\Progra~1\\Jampal\\ptts.vbs"]

        # Run the command
        subprocess.run(cmd, stdout=None, stderr=None)


def main():
    # Parse and validate the network IP address and subnet mask
    network = ipaddress.ip_network(NETWORK, strict=False)

    # Scan the network for devices
    old_macs = scan(network)

    # Announce that the devices are connected
    connection_change(old_macs, "connected")

    # Loop indefinitely
    while True:
        # Sleep for the specified interval
        time.sleep(INTERVAL)

        # Scan the network for devices
        macs = scan(network)

        # Calculate the set of new devices
        new = macs
