#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.node import OVSController

if __name__ == "__main__":
    net = Mininet(controller=OVSController)
    c0 = net.addController("c0", controller=OVSController)

    pc1 = net.addHost("pc1")
    pc2 = net.addHost("pc2")
    ws1 = net.addHost("ws1")
    ws2 = net.addHost("ws2")
    ws3 = net.addHost("ws3")
    lb1 = net.addHost("lb1")

    s1 = net.addSwitch("s1", cls=OVSSwitch)
    s2 = net.addSwitch("s2", cls=OVSSwitch)

    net.addLink(pc1, s1)
    net.addLink(pc2, s1)
    net.addLink(s1, lb1)
    net.addLink(lb1, s2)
    net.addLink(s2, ws1)
    net.addLink(s2, ws2)
    net.addLink(s2, ws3)

    net.start()

    pc1.setIP("10.0.0.2/24", intf="pc1-eth0")
    pc2.setIP("10.0.0.3/24", intf="pc2-eth0")

    lb1.setIP("10.0.0.4/24", intf="lb1-eth0")
    lb1.setIP("100.0.0.4/24", intf="lb1-eth1")

    ws1.setIP("100.0.0.1/24", intf="ws1-eth0")
    ws1.cmd("ip route add default via 100.0.0.4")
    ws1.cmd("cd /var/www/html/ws1 && python3 -m http.server 80 &")

    ws2.setIP("100.0.0.2/24", intf="ws2-eth0")
    ws2.cmd("ip route add default via 100.0.0.4")
    ws2.cmd("cd /var/www/html/ws2 && python3 -m http.server 80 &")

    ws3.setIP("100.0.0.3/24", intf="ws3-eth0")
    ws3.cmd("ip route add default via 100.0.0.4")
    ws3.cmd("cd /var/www/html/ws3 && python3 -m http.server 80 &")

    lb1.cmd(
        "iptables-legacy --table nat --append PREROUTING --destination 10.0.0.4 -p tcp --dport 80 --match statistic --mode random --probability 0.33 --jump DNAT --to-destination 100.0.0.1:80"
    )

    lb1.cmd(
        "iptables-legacy --table nat --append PREROUTING --destination 10.0.0.4 -p tcp --dport 80 --match statistic --mode random --probability 0.5 --jump DNAT --to-destination 100.0.0.2:80"
    )

    lb1.cmd(
        "iptables-legacy --table nat --append PREROUTING --destination 10.0.0.4 -p tcp --dport 80 --jump DNAT --to-destination 100.0.0.3:80"
    )

    lb1.cmd("iperf3 -s -D")
    ws1.cmd("iperf3 -s -D")
    ws2.cmd("iperf3 -s -D")
    ws3.cmd("iperf3 -s -D")

    p1 = pc1.popen("iperf3 -c 10.0.0.4 -t 30")
    p2 = pc2.popen("iperf3 -c 10.0.0.4 -t 30")

    p1.wait()
    p2.wait()

    net.stop()
