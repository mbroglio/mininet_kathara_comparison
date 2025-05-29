#!/usr/bin/env python3

from mininet.net import Containernet
from mininet.node import Controller, OVSController
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.link import TCLink


def topology():
    "Create a network with the complete DNS hierarchy"
    net = Containernet(controller=OVSController)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1", cls=OVSSwitch)

    info("*** Adding docker containers\n")
    # Root DNS server
    dnsroot = net.addDocker(
        "dnsroot",
        ip="192.168.0.5/24",
        dimage="dnsroot-image",
    )

    # IT TLD server
    dnsit = net.addDocker(
        "dnsit",
        ip="192.168.0.1/24",
        dimage="dnsit-image",
    )

    # COM TLD server
    dnscom = net.addDocker(
        "dnscom",
        ip="192.168.0.2/24",
        dimage="dnscom-image",
    )

    # UNIMIB authoritative server
    dnsunimib = net.addDocker(
        "dnsunimib",
        ip="192.168.0.11/24",
        dimage="dnsunimib-image",
    )

    # AMAZON authoritative server
    dnsamazon = net.addDocker(
        "dnsamazon",
        ip="192.168.0.22/24",
        dimage="dnsamazon-image",
    )

    # Web servers
    wsunimib = net.addDocker(
        "wsunimib",
        ip="192.168.0.110/24",
        dimage="wsunimib-image",
    )

    wsamazon = net.addDocker(
        "wsamazon",
        ip="192.168.0.220/24",
        dimage="wsamazon-image",
    )

    # Hosts
    pc1 = net.addDocker(
        "pc1",
        ip="192.168.0.111/24",
        dimage="client-image",
    )

    pc2 = net.addDocker(
        "pc2",
        ip="192.168.0.222/24",
        dimage="client-image",
    )

    info("*** Creating links\n")
    net.addLink(dnsroot, s1)
    net.addLink(dnsit, s1)
    net.addLink(dnscom, s1)
    net.addLink(dnsunimib, s1)
    net.addLink(dnsamazon, s1)
    net.addLink(wsunimib, s1)
    net.addLink(wsamazon, s1)
    net.addLink(pc1, s1)
    net.addLink(pc2, s1)

    info("*** Starting network\n")
    net.start()

    # Configure default routes
    info("*** Configuring default routes\n")
    for host in [
        dnsroot,
        dnsit,
        dnscom,
        dnsunimib,
        dnsamazon,
        wsunimib,
        wsamazon,
        pc1,
        pc2,
    ]:
        host.cmd("ip route add default dev eth0")

    # Configure DNS resolution
    info("*** Configuring DNS resolution\n")
    # Root server points to itself
    dnsroot.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")

    # TLD servers point to root
    dnsit.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")
    dnscom.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")

    # Authoritative servers point to root
    dnsunimib.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")
    dnsamazon.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")

    # Web servers and hosts point to root
    wsunimib.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")
    wsamazon.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")
    pc1.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")
    pc2.cmd("echo 'nameserver 192.168.0.5' > /etc/resolv.conf")

    # Start DNS servers with named -4 -u bind
    info("*** Starting DNS servers with named -4 -u bind\n")
    dnsroot.cmd("service bind9 start")
    dnsroot.cmd("named -4 -u bind")

    dnsit.cmd("service bind9 start")
    dnsit.cmd("named -4 -u bind")

    dnscom.cmd("service bind9 start")
    dnscom.cmd("named -4 -u bind")

    dnsunimib.cmd("service bind9 start")
    dnsunimib.cmd("named -4 -u bind")

    dnsamazon.cmd("service bind9 start")
    dnsamazon.cmd("named -4 -u bind")

    wsunimib.cmd("service bind9 start")
    wsunimib.cmd("named -4 -u bind")

    wsamazon.cmd("service bind9 start")
    wsamazon.cmd("named -4 -u bind")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    topology()
