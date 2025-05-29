#!/usr/bin/python3

from mininet.net import Mininet

if __name__ == "__main__":
    net = Mininet()

    pc1 = net.addHost("pc1")
    pc2 = net.addHost("pc2")
    r1 = net.addHost("r1")
    r2 = net.addHost("r2")

    net.addLink(pc1, r1)
    net.addLink(r1, r2)
    net.addLink(r2, pc2)

    net.start()

    pc1.setIP("10.0.0.2/24", intf="pc1-eth0")
    pc1.cmd("ip route add default via 10.0.0.1")

    pc2.setIP("10.0.1.4/24", intf="pc2-eth0")
    pc2.cmd("ip route add default via 10.0.1.1")

    r1.setIP("10.0.0.1/24", intf="r1-eth0")
    r1.setIP("100.0.0.1/30", intf="r1-eth1")
    r1.cmd("ip route add 10.0.1.0/24 via 100.0.0.2")
    r1.cmd("sysctl -w net.ipv4.ip_forward=1")

    r2.setIP("100.0.0.2/30", intf="r2-eth0")
    r2.setIP("10.0.1.1/24", intf="r2-eth1")
    r2.cmd("ip route add 10.0.0.0/24 via 100.0.0.1")
    r2.cmd("sysctl -w net.ipv4.ip_forward=1")

    p1 = pc1.popen("ping 10.0.1.4 -c 10")
    p2 = pc2.popen("ping 10.0.0.2 -c 10")

    p1.wait()
    p2.wait()

    net.stop()
