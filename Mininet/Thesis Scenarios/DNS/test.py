from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.cli import CLI


class DNSExampleTopo(Topo):
    def build(self):
        """Create custom topology with a DNS server and two clients."""
        # Add hosts
        dns_server = self.addHost("dns", ip="10.0.0.1")
        client1 = self.addHost("h1", ip="10.0.0.2")
        client2 = self.addHost("h2", ip="10.0.0.3")

        # Add a switch
        switch = self.addSwitch("s1")

        # Add links
        self.addLink(dns_server, switch)
        self.addLink(client1, switch)
        self.addLink(client2, switch)


# Function to configure and run the DNS server
def setup_dns_server(dns_server):
    """Configure the DNS server."""
    info("*** Installing bind9 on the DNS server\n")
    dns_server.cmd("apt-get update")
    dns_server.cmd("apt-get install -y bind9")

    info("*** Configuring bind9\n")
    named_conf_local = "/etc/bind/named.conf.local"
    zone_file = "/etc/bind/db.example.com"

    # Configure a custom zone for example.com
    dns_server.cmd(
        f'echo "zone "example.com" {{ type master; file "{zone_file}"; }};" >> {named_conf_local}'
    )

    # Create a zone file
    dns_server.cmd(f'echo "$TTL 86400" > {zone_file}')
    dns_server.cmd(
        f'echo "@ IN SOA ns.example.com. admin.example.com. (1 604800 86400 2419200 86400)" >> {zone_file}'
    )
    dns_server.cmd(f'echo "@ IN NS ns.example.com." >> {zone_file}')
    dns_server.cmd(f'echo "ns IN A 10.0.0.1" >> {zone_file}')
    dns_server.cmd(f'echo "www IN A 10.0.0.10" >> {zone_file}')

    # Restart bind9
    dns_server.cmd("/etc/init.d/bind9 restart")


# Function to configure clients
def setup_client(client, dns_ip):
    """Configure a client to use the DNS server."""
    info(f"*** Configuring {client.name}\n")
    client.cmd(f'echo "nameserver {dns_ip}" > /etc/resolv.conf')


if __name__ == "__main__":
    setLogLevel("info")

    # Create the network
    topo = DNSExampleTopo()
    net = Mininet(topo=topo, controller=Controller, switch=OVSKernelSwitch, link=TCLink)

    # Start the network
    net.start()

    # Get the DNS server and clients
    dns_server = net.get("dns")
    client1 = net.get("h1")
    client2 = net.get("h2")

    # Setup the DNS server
    setup_dns_server(dns_server)

    # Setup the clients to use the DNS server
    setup_client(client1, "10.0.0.1")
    setup_client(client2, "10.0.0.1")

    info("*** Network setup complete\n")
    info("*** Testing DNS resolution\n")

    # Test DNS resolution from client1
    result = client1.cmd("nslookup www.example.com")
    info(f"Client 1 DNS resolution:\n{result}\n")

    # Test DNS resolution from client2
    result = client2.cmd("nslookup www.example.com")
    info(f"Client 2 DNS resolution:\n{result}\n")

    # Drop to the CLI for further interaction
    CLI(net)

    # Stop the network
    net.stop()
