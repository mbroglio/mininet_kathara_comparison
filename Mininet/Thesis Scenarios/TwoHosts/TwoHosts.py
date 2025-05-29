#!/usr/bin/python3

from mininet.net import Mininet

if __name__ == "__main__":
    net = Mininet()

    pc1 = net.addHost("pc1")
    pc2 = net.addHost("pc2")

    net.addLink(pc1, pc2)

    net.start()

    pc1.setIP("10.0.0.1/24", intf="pc1-eth0")
    pc2.setIP("10.0.0.2/24", intf="pc2-eth0")

    # Run pings in parallel
    p1 = pc1.popen("ping 10.0.0.2 -c 10")
    p2 = pc2.popen("ping 10.0.0.1 -c 10")

    # Wait for both pings to finish
    p1.wait()
    p2.wait()

    net.stop()
