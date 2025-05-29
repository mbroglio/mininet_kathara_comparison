#!/usr/bin/python3

from mininet.net import Mininet
import time

if __name__ == "__main__":
    net = Mininet()

    # Add Hosts (Routers)
    r1 = net.addHost("r1")
    r2 = net.addHost("r2")
    r3 = net.addHost("r3")
    r4 = net.addHost("r4")

    # Start network
    net.start()

    # Explicitly add links with interface names
    net.addLink(
        r1,
        r2,
        intfName1="r1-eth0",
        params1={"ip": "10.0.0.1/30"},
        intfName2="r2-eth0",
        params2={"ip": "10.0.0.2/30"},
    )

    net.addLink(
        r2,
        r3,
        intfName1="r2-eth1",
        params1={"ip": "10.0.0.5/30"},
        intfName2="r3-eth1",
        params2={"ip": "10.0.0.6/30"},
    )

    net.addLink(
        r3,
        r4,
        intfName1="r3-eth0",
        params1={"ip": "10.0.0.9/30"},
        intfName2="r4-eth0",
        params2={"ip": "10.0.0.10/30"},
    )

    net.addLink(
        r4,
        r1,
        intfName1="r4-eth1",
        params1={"ip": "10.0.0.14/30"},
        intfName2="r1-eth1",
        params2={"ip": "10.0.0.13/30"},
    )

    net.addLink(
        r1,
        r3,
        intfName1="r1-eth2",
        params1={"ip": "10.0.0.17/30"},
        intfName2="r3-eth2",
        params2={"ip": "10.0.0.18/30"},
    )

    # Enable IP forwarding on all routers
    for router in [r1, r2, r3, r4]:
        router.cmd("sysctl -w net.ipv4.ip_forward=1")

    # Start FRR for OSPF routing
    r1.cmd("/usr/lib/frr/frrinit.sh start 'r1'")
    r2.cmd("/usr/lib/frr/frrinit.sh start 'r2'")
    r3.cmd("/usr/lib/frr/frrinit.sh start 'r3'")
    r4.cmd("/usr/lib/frr/frrinit.sh start 'r4'")

    time.sleep(65)

    rt1 = r1.popen("ping -I r1-eth0 10.0.0.6 -c 10")
    rt2 = r2.popen("ping -I r2-eth0 10.0.0.14 -c 10")

    print(rt1.communicate())
    print(rt2.communicate())

    rt1.wait()
    rt2.wait()

    # Stop network
    net.stop()
