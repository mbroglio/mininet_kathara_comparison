#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import OVSController, OVSSwitch
from mininet.cli import CLI


if __name__ == "__main__":
    net = Mininet(controller=OVSController)
    c0 = net.addController("c0", controller=OVSController)

    dnsroot = net.addHost("dnsroot")
    s1 = net.addSwitch("s1", cls=OVSSwitch)
    dnsit = net.addHost("dnsit")
    dnscom = net.addHost("dnscom")
    s2 = net.addSwitch("s2", cls=OVSSwitch)
    s3 = net.addSwitch("s3", cls=OVSSwitch)
    pc1 = net.addHost("pc1")
    dnsunimib = net.addHost("dnsunimib")
    wsunimib = net.addHost("wsunimib")
    pc2 = net.addHost("pc2")
    dnsamazon = net.addHost("dnsamazon")
    wsamazon = net.addHost("wsamazon")

    net.addLink(dnsroot, s1)
    net.addLink(s1, dnsit)
    net.addLink(s1, dnscom)
    net.addLink(dnsit, s2)
    net.addLink(dnscom, s3)
    net.addLink(s2, pc1)
    net.addLink(s2, dnsunimib)
    net.addLink(s2, wsunimib)
    net.addLink(s3, pc2)
    net.addLink(s3, dnsamazon)
    net.addLink(s3, wsamazon)

    net.start()

    dnsroot.setIP("192.168.0.5/24", intf="dnsroot-eth0")
    dnsit.setIP("192.168.0.1/24", intf="dnsit-eth0")
    dnscom.setIP("192.168.0.2/24", intf="dnscom-eth0")
    pc1.setIP("192.168.0.111/24", intf="pc1-eth0")
    dnsunimib.setIP("192.168.0.11/24", intf="dnsunimib-eth0")
    wsunimib.setIP("192.168.0.110/24", intf="wsunimib-eth0")
    pc2.setIP("192.168.0.222/24", intf="pc2-eth0")
    dnsamazon.setIP("192.168.0.22/24", intf="dnsamazon-eth0")
    wsamazon.setIP("192.168.0.220/24", intf="wsamazon-eth0")

    CLI(net)

    net.stop()
