#!/usr/bin/env python3

from mininet.net import Containernet
from mininet.node import Controller, OVSController
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.link import TCLink


def topology():
    "Create a network with a DNS server and two clients"
    net = Containernet(controller=OVSController)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1", cls=OVSSwitch)

    info("*** Adding docker containers\n")
    # DNS server without volume mount
    dns = net.addDocker(
        "dns",
        ip="10.0.0.10/24",
        dimage="dns-server-image",
        # Remove volume mount
    )

    # Client containers with proper network configuration
    client1 = net.addDocker("client1", ip="10.0.0.100/24", dimage="client-image")

    client2 = net.addDocker("client2", ip="10.0.0.101/24", dimage="client-image")

    info("*** Creating links\n")
    net.addLink(dns, s1)
    net.addLink(client1, s1)
    net.addLink(client2, s1)

    info("*** Starting network\n")
    net.start()

    # Configure DNS clients with correct networking
    info("*** Configuring clients to use DNS server\n")
    client1.cmd("ip route add default dev eth0")
    client2.cmd("ip route add default dev eth0")
    dns.cmd("ip route add 10.0.0.100 dev eth0")
    dns.cmd("ip route add 10.0.0.101 dev eth0")

    client1.cmd("echo 'nameserver 10.0.0.10' > /etc/resolv.conf")
    client2.cmd("echo 'nameserver 10.0.0.10' > /etc/resolv.conf")

    # Start BIND DNS server
    info("*** Starting DNS server\n")
    dns.cmd("service bind9 start")
    dns.cmd("named -4 -u bind")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    topology()
