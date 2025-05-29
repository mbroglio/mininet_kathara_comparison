#!/usr/bin/python3

from mininet.net import Mininet
import time

if __name__ == "__main__":
    net = Mininet()

    as10r1 = net.addHost("as10r1")
    as10pc1 = net.addHost("as10pc1")
    as20r1 = net.addHost("as20r1")
    as20pc1 = net.addHost("as20pc1")
    as20server1 = net.addHost("srv1")

    net.addLink(
        as10r1,
        as20r1,
        intfName1="as10r1-eth0",
        intfName2="as20r1-eth0",
        params1={"ip": "100.0.0.2/30"},
        params2={"ip": "100.0.0.1/30"},
    )
    net.addLink(
        as10r1,
        as10pc1,
        intfName1="as10r1-eth1",
        intfName2="as10pc1-eth0",
        params1={"ip": "192.168.0.1/24"},
        params2={"ip": "192.168.0.8/24"},
    )
    net.addLink(
        as20r1,
        as20pc1,
        intfName1="as20r1-eth1",
        intfName2="as20pc1-eth0",
        params1={"ip": "10.0.0.1/16"},
        params2={"ip": "10.0.0.10/16"},
    )
    net.addLink(
        as20r1,
        as20server1,
        intfName1="as20r1-eth2",
        intfName2="srv1-eth0",
        params1={"ip": "11.0.0.1/24"},
        params2={"ip": "11.0.0.2/24"},
    )

    # Start the network
    net.start()

    # Set IPs and interfaces up
    as10r1.setIP("100.0.0.2/30", intf="as10r1-eth0")
    as10r1.setIP("192.168.0.1/24", intf="as10r1-eth1")
    as10r1.cmd("ip link set dev as10r1-eth0 up")
    as10r1.cmd("ip link set dev as10r1-eth1 up")
    as10r1.cmd("sysctl -w net.ipv4.ip_forward=1")

    as10pc1.setIP("192.168.0.8/24", intf="as10pc1-eth0")
    as10pc1.cmd("ip link set dev as10pc1-eth0 up")
    as10pc1.cmd("ip route add default via 192.168.0.1")

    as20r1.setIP("100.0.0.1/30", intf="as20r1-eth0")
    as20r1.setIP("10.0.0.1/16", intf="as20r1-eth1")
    as20r1.setIP("11.0.0.1/24", intf="as20r1-eth2")
    as20r1.cmd("ip link set dev as20r1-eth0 up")
    as20r1.cmd("ip link set dev as20r1-eth1 up")
    as20r1.cmd("ip link set dev as20r1-eth2 up")
    as20r1.cmd("sysctl -w net.ipv4.ip_forward=1")

    as20pc1.setIP("10.0.0.10/16", intf="as20pc1-eth0")
    as20pc1.cmd("ip link set dev as20pc1-eth0 up")
    as20pc1.cmd("ip route add default via 10.0.0.1")

    as20server1.setIP("11.0.0.2/24", intf="srv1-eth0")
    as20server1.cmd("ip link set dev srv1-eth0 up")
    as20server1.cmd("ip route add default via 11.0.0.1")

    # Allow BGP traffic
    as10r1.cmd("iptables -A INPUT -p tcp --dport 179 -j ACCEPT")
    as10r1.cmd("iptables -A OUTPUT -p tcp --sport 179 -j ACCEPT")
    as20r1.cmd("iptables -A INPUT -p tcp --dport 179 -j ACCEPT")
    as20r1.cmd("iptables -A OUTPUT -p tcp --sport 179 -j ACCEPT")

    # Start FRR (BGP) after interfaces are up
    time.sleep(5)  # Add a short delay for proper setup
    as10r1.cmd("/usr/lib/frr/frrinit.sh start 'as10r1'")
    as20r1.cmd("/usr/lib/frr/frrinit.sh start 'as20r1'")

    as10pc1.cmd("ping 11.0.0.2 -c 20")

    net.stop()
