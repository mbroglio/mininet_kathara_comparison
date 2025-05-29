#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import OVSController
import time

if __name__ == "__main__":
    # Create Mininet instance
    net = Mininet(controller=OVSController)

    # Create controller and add it to the network
    c0 = net.addController("c0", controller=OVSController)

    # Add hosts
    as10r1 = net.addHost("as10r1")
    as10pc1 = net.addHost("as10pc1")
    as20r1 = net.addHost("as20r1")
    as20r2 = net.addHost("as20r2")
    as20r3 = net.addHost("as20r3")
    as20r4 = net.addHost("as20r4")
    as20r5 = net.addHost("as20r5")
    as20ws1 = net.addHost("as20ws1")

    # Add links between hosts and routers
    net.addLink(
        as10pc1,
        as10r1,
        intfName1="as10pc1-eth0",
        intfName2="as10r1-eth1",
        params1={"ip": "192.168.0.8/24"},
        params2={"ip": "192.168.0.1/24"},
    )
    net.addLink(
        as10r1,
        as20r1,
        intfName1="as10r1-eth0",
        intfName2="as20r1-eth3",
        params1={"ip": "100.0.0.2/30"},
        params2={"ip": "100.0.0.1/30"},
    )
    net.addLink(
        as20r1,
        as20r2,
        intfName1="as20r1-eth0",
        intfName2="as20r2-eth0",
        params1={"ip": "10.0.0.1/30"},
        params2={"ip": "10.0.0.2/30"},
    )
    net.addLink(
        as20r1,
        as20r4,
        intfName1="as20r1-eth1",
        intfName2="as20r4-eth1",
        params1={"ip": "10.0.0.14/30"},
        params2={"ip": "10.0.0.13/30"},
    )
    net.addLink(
        as20r1,
        as20r3,
        intfName1="as20r1-eth2",
        intfName2="as20r3-eth2",
        params1={"ip": "10.0.0.17/30"},
        params2={"ip": "10.0.0.18/30"},
    )
    net.addLink(
        as20r2,
        as20r3,
        intfName1="as20r2-eth1",
        intfName2="as20r3-eth1",
        params1={"ip": "10.0.0.5/30"},
        params2={"ip": "10.0.0.6/30"},
    )
    net.addLink(
        as20r3,
        as20r4,
        intfName1="as20r3-eth0",
        intfName2="as20r4-eth0",
        params1={"ip": "10.0.0.9/30"},
        params2={"ip": "10.0.0.10/30"},
    )
    net.addLink(
        as20r3,
        as20r5,
        intfName1="as20r3-eth3",
        intfName2="as20r5-eth0",
        params1={"ip": "15.0.0.1/30"},
        params2={"ip": "15.0.0.2/30"},
    )
    net.addLink(
        as20r5,
        as20ws1,
        intfName1="as20r5-eth1",
        intfName2="as20ws1-eth0",
        params1={"ip": "192.168.1.1/24"},
        params2={"ip": "192.168.1.4/24"},
    )

    # Bring up the interfaces manually for the devices
    as10r1.cmd("ifconfig as10r1-eth1 up")
    as20r1.cmd("ifconfig as20r1-eth3 up")
    as20r2.cmd("ifconfig as20r2-eth0 up")
    as20r3.cmd("ifconfig as20r3-eth2 up")
    as20r4.cmd("ifconfig as20r4-eth1 up")
    as20r5.cmd("ifconfig as20r5-eth0 up")
    as20r5.cmd("ifconfig as20r5-eth1 up")
    as20ws1.cmd("ifconfig as20ws1-eth0 up")

    # Configure IP addresses
    as10pc1.setIP("192.168.0.8/24")
    as10r1.setIP("192.168.0.1/24", intf="as10r1-eth1")
    as20r1.setIP("100.0.0.1/30", intf="as20r1-eth3")
    as20r2.setIP("10.0.0.2/30", intf="as20r2-eth0")
    as20r3.setIP("10.0.0.18/30", intf="as20r3-eth2")
    as20r4.setIP("10.0.0.13/30", intf="as20r4-eth1")
    as20r5.setIP("15.0.0.2/30", intf="as20r5-eth0")
    as20r5.setIP("192.168.1.1/24", intf="as20r5-eth1")
    as20ws1.setIP("192.168.1.4/24", intf="as20ws1-eth0")

    # Manually configure routes
    as10pc1.cmd("ip route add default via 192.168.0.1")
    as20ws1.cmd("ip route add default via 192.168.1.1")

    # Enable IP forwarding and configure FRR on routers
    for router in [as10r1, as20r1, as20r2, as20r3, as20r4, as20r5]:
        router.cmd("/usr/lib/frr/frrinit.sh start " + router.name)
        router.cmd("sysctl -w net.ipv4.ip_forward=1")
        router.cmd("iptables -A INPUT -p tcp --dport 179 -j ACCEPT")

    # Start HTTP server on as20ws1
    as20ws1.cmd("cd /var/www/html && python3 -m http.server 80 &")

    as20ws1.cmd("iperf3 -s -D")

    time.sleep(65)
    as10pc1.cmd("iperf3 -c 192.168.1.4 -t 30")

    net.stop()
