#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel

setLogLevel("info")

net = Containernet(controller=Controller)

info("*** Adding controller\n")
net.addController("c0")

info("*** Adding docker containers\n")

dnsamazon = net.addDocker(
    "dnsamazon",
    ip="192.168.0.22/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/dnsamazon:/dnsamazon"],
)

dnscom = net.addDocker(
    "dnscom",
    ip="192.168.0.2/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/dnscom:/dnscom"],
)

dnsit = net.addDocker(
    "dnsit",
    ip="192.168.0.1/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/dnsit:/dnsit"],
)

dnsroot = net.addDocker(
    "dnsroot",
    ip="192.168.0.5/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/dnsroot:/dnsroot"],
)

dnsunimib = net.addDocker(
    "dnsunimib",
    ip="192.168.0.11/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/dnsunimib:/dnsunimib"],
)

pc1 = net.addDocker(
    "pc1",
    ip="192.168.0.111/24",
    dimage="ubuntu:trusty",
    volumes=["/home/teo/Desktop/Containernet/DNS/pc1:/pc1"],
)

pc2 = net.addDocker(
    "pc2",
    ip="192.168.0.222/24",
    dimage="ubuntu:trusty",
    volumes=["/home/teo/Desktop/Containernet/DNS/pc2:/pc2"],
)

wsamazon = net.addDocker(
    "wsamazon",
    ip="192.168.0.220/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/wsamazon:/wsamazon"],
)

wsunimib = net.addDocker(
    "wsunimib",
    ip="192.168.0.110/24",
    dimage="ubuntu:latest",
    volumes=["/home/teo/Desktop/Containernet/DNS/wsunimib:/wsunimib"],
)

info("*** Creating switches\n")
s1 = net.addSwitch("s1")
s2 = net.addSwitch("s2")
s3 = net.addSwitch("s3")

info("*** Creating links\n")
net.addLink(dnsroot, s1)
net.addLink(dnscom, s1)
net.addLink(dnsit, s1)

net.addLink(dnsit, s2)
net.addLink(dnsunimib, s2)
net.addLink(wsunimib, s2)
net.addLink(pc1, s2)

net.addLink(dnscom, s3)
net.addLink(dnsamazon, s3)
net.addLink(wsamazon, s3)
net.addLink(pc2, s3)

info("*** Starting network\n")
net.start()

bind9 = [dnsroot, dnscom, dnsit, dnsunimib, dnsamazon, wsamazon, wsunimib]
for container in bind9:
    container.cmd("apt-get update")
    container.cmd("apt-get install -y bind9")
    container.cmd("apt-get install -y net-tools iproute iputils-ping dnsutils")
    container.cmd(f"cp -a {container.name}/etc/bind/. etc/bind")
    container.cmd("service bind9 restart")

pc1.cmd("cp -a pc1/etc/resolv.conf etc/resolv.conf")
pc1.cmd("apt-get install -y net-tools iproute iputils-ping dnsutils")

pc2.cmd("cp -a pc2/etc/resolv.conf etc/resolv.conf")
pc2.cmd("apt-get install -y net-tools iproute iputils-ping dnsutils")

info("*** Starting CLI\n")
CLI(net)

info("*** Stopping network\n")
net.stop()
