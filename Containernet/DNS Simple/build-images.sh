#!/bin/bash

# Create directories for our Dockerfiles
mkdir -p dns-server
mkdir -p client

# Copy configurations to DNS server directory
cat > dns-server/Dockerfile << 'EOF'
FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y bind9 bind9utils dnsutils iproute2 iputils-ping net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create default configuration files
RUN mkdir -p /var/run/named && \
    chown -R bind:bind /var/run/named && \
    mkdir -p /var/cache/bind && \
    chown -R bind:bind /var/cache/bind

# These configuration files need to be copied into the image
COPY named.conf.options /etc/bind/
COPY named.conf.local /etc/bind/
COPY db.example.com /etc/bind/

# Ensure proper permissions
RUN chown -R bind:bind /etc/bind

EXPOSE 53/udp
EXPOSE 53/tcp

# Use a script that can be run interactively
CMD ["/bin/bash", "-c", "sleep infinity"]
EOF

cat > dns-server/named.conf.options << 'EOF'
options {
        directory "/var/cache/bind";
        
        listen-on { any; };
        allow-query { any; };
        
        recursion yes;
        
        dnssec-validation auto;
        auth-nxdomain no;

        // Important: Allow all network traffic
        listen-on-v6 { any; };
        allow-transfer { any; };
};
EOF

cat > dns-server/named.conf.local << 'EOF'
zone "example.com" {
        type master;
        file "/etc/bind/db.example.com";
        allow-transfer { any; };
        allow-update { any; };
};
EOF

cat > dns-server/db.example.com << 'EOF'
$TTL    604800
@       IN      SOA     example.com. root.example.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns1.example.com.
@       IN      A       10.0.0.10
ns1     IN      A       10.0.0.10
www     IN      A       10.0.0.10
client1 IN      A       10.0.0.100
client2 IN      A       10.0.0.101
EOF

# Create client Dockerfile
cat > client/Dockerfile << 'EOF'
FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils iputils-ping net-tools curl iproute2 traceroute && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "sleep infinity"]
EOF

# Build the Docker images
echo "Building DNS server image..."
docker build -t dns-server-image dns-server/

echo "Building client image..."
docker build -t client-image client/

echo "Docker images built successfully"