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
