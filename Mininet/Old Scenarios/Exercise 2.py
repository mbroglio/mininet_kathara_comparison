from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.term import makeTerms


def runCustomTopo():
    # Set the log level to info
    setLogLevel("info")

    # Create an instance of Mininet with the custom topology
    net = Mininet()

    # Add hosts
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    h3 = net.addHost("h3")

    # Add switches
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")

    # Add links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s1, s2)
    net.addLink(h3, s2)

    # Add a controller
    net.addController("c0")

    # Start the network
    net.start()

    net.pingAll()
    makeTerms([h1, h2, h3])

    # Start the CLI
    CLI(net)

    # Stop the network
    net.stop()


if __name__ == "__main__":
    runCustomTopo()
