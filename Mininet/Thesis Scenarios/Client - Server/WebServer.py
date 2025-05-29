#!/usr/bin/python3

from mininet.net import Mininet

if __name__ == "__main__":
    net = Mininet()

    pc1 = net.addHost("pc1")
    ws1 = net.addHost("ws1")
    r1 = net.addHost("r1")

    net.addLink(pc1, r1)
    net.addLink(ws1, r1)

    net.start()

    pc1.setIP("10.0.0.2/24", intf="pc1-eth0")
    pc1.cmd("ip route add default via 10.0.0.1")

    r1.setIP("10.0.0.1/24", intf="r1-eth0")
    r1.setIP("10.0.5.1/24", intf="r1-eth1")
    r1.cmd("sysctl -w net.ipv4.ip_forward=1")

    ws1.setIP("10.0.5.2/24", intf="ws1-eth0")
    ws1.cmd("ip route add default via 10.0.5.1")
    ws1.cmd("python3 -m http.server 80 &")

    # Start iperf server on ws1
    ws1.cmd("iperf3 -s -D")

    # Generate TCP traffic from pc1 to ws1
    print("Starting iperf client on pc1...")
    pc1.cmd("iperf3 -c 10.0.5.2 -t 30")

    # Stop the network
    net.stop()
