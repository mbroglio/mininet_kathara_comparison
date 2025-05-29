#!/usr/bin/python3

from mininet.net import Mininet
from mininet.cli import CLI


def runCustomTopo():
    net = Mininet()

    # Add hosts and switches
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    r1 = net.addHost("r1")

    net.addLink(h1, r1)
    net.addLink(h2, r1)

    net.start()

    # Configuring ip addresses
    h1.setIP("10.0.0.5/24")
    h2.setIP("10.0.1.5/24")
    r1.setIP("10.0.0.1/24", intf="r1-eth0")
    r1.setIP("10.0.1.1/24", intf="r1-eth1")

    r1.cmd("sysctl -w net.ipv4.ip_forward=1")

    h1.cmd("ip route add default via 10.0.0.1")
    h2.cmd("ip route add default via 10.0.1.1")

    net.pingAll()

    CLI(net)
    net.stop()


if __name__ == "__main__":
    runCustomTopo()
