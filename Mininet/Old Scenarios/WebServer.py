#!/usr/bin/python3

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.term import makeTerms
from mininet.cli import CLI


def runCustomTopo():
    setLogLevel("info")
    net = Mininet()

    h1 = net.addHost("h1")
    h2 = net.addHost("h2")

    s1 = net.addSwitch("s1")

    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addController("c0")

    net.start()
    net.pingAll()

    h1.cmd("python3 -m http.server 80 &")
    # echo "<html><body><h1>Hello from Mininet!</h1></body></html>" > index.html
    # Shoudl be invoked from the h1 host

    makeTerms([h1, h2])
    CLI(net)

    net.stop()


if __name__ == "__main__":
    runCustomTopo()
