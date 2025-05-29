FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y bind9 bind9utils dnsutils iproute2 iputils-ping net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/named && \
    chown -R bind:bind /var/run/named && \
    mkdir -p /var/cache/bind && \
    chown -R bind:bind /var/cache/bind

COPY named.conf.options /etc/bind/
COPY named.conf /etc/bind/
COPY db.root /etc/bind/

RUN chown -R bind:bind /etc/bind

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
