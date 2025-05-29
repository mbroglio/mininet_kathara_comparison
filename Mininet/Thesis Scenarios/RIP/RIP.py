#!/usr/bin/python3

from mininet.net import Mininet

if __name__ == "__main__":
    net = Mininet()

    r1 = net.addHost("r1")
    r2 = net.addHost("r2")
    r3 = net.addHost("r3")
    pc1 = net.addHost("pc1")
    pc2 = net.addHost("pc2")

    net.addLink(pc1, r1)
    net.addLink(pc2, r3)
    net.addLink(r1, r2)
    net.addLink(r2, r3)
    net.addLink(r1, r3)

    net.start()

    pc1.setIP("192.168.1.2/24", intf="pc1-eth0")
    pc1.cmd("ip route add default via 192.168.1.1")

    pc2.setIP("192.168.0.2/24", intf="pc2-eth0")
    pc2.cmd("ip route add default via 192.168.0.1")

    r1.setIP("192.168.1.1/24", intf="r1-eth0")
    r1.setIP("10.0.0.1/30", intf="r1-eth1")
    r1.setIP("10.0.0.10/30", intf="r1-eth2")

    r2.setIP("10.0.0.2/30", intf="r2-eth0")
    r2.setIP("10.0.0.5/30", intf="r2-eth1")

    r3.setIP("192.168.0.1/24", intf="r3-eth0")
    r3.setIP("10.0.0.6/30", intf="r3-eth1")
    r3.setIP("10.0.0.9/30", intf="r3-eth2")

    for router in [r1, r2, r3]:
        router.cmd("sysctl -w net.ipv4.ip_forward=1")

    r1.cmd("/usr/lib/frr/frrinit.sh start 'r1'")
    r2.cmd("/usr/lib/frr/frrinit.sh start 'r2'")
    r3.cmd("/usr/lib/frr/frrinit.sh start 'r3'")

    p1 = pc1.popen("ping 192.168.0.2 -c 10")
    p2 = pc2.popen("ping 192.168.1.2 -c 10")

    p1.wait()
    p2.wait()

    net.stop()
