import scapy.all as scapy
import time,subprocess

NETWORK = "192.168.1.0/24"
current_macs =[]
dictionnary = {
'11:22:22:33:44:55' : 'John Mobile',
'66:77:88:99:11:22' : 'Eric PC',
'33:44:55:66:77:88' : 'Bob Mobile'
}

def scan(ip):
    macs = []
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    for host in answered_list:
        if host[1].psrc != "192.168.1.1":
            macs.append(host[1].src)
    return macs

def disconnected(hosts):
    for host in hosts:
        try:
            say = "echo " + dictionnary[host] + " disconnected" + " | cscript C:\\Progra~1\\Jampal\\ptts.vbs"
        except KeyError:
            say = "echo unknown device disconnected" + " | cscript C:\\Progra~1\\Jampal\\ptts.vbs"
        cmd = subprocess.call(say,shell=True,stdout=None,stderr=None)

def connected(hosts):
    for host in hosts:
        try:
            say = "echo " + dictionnary[host] + " connected" + " | cscript C:\\Progra~1\\Jampal\\ptts.vbs"
        except KeyError:
            say = "echo unknown device connected" + " | cscript C:\\Progra~1\\Jampal\\ptts.vbs"
        cmd = subprocess.call(say,shell=True,stdout=None,stderr=None)


def main():
    current_macs = scan(NETWORK)
    connected(current_macs)
    while True:
        time.sleep(10)
        macs = scan(NETWORK)
        new = list(set(macs) - set(current_macs))
        left = list(set(current_macs) - set(macs))
        current_macs = current_macs + new
        current_macs = list(set(current_macs) - set(left))

        if new :
            connected(new)
        if left :
            disconnected(left)



if __name__ == "__main__":
    main()