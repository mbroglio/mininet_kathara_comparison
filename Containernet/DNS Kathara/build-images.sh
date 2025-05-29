#!/bin/bash

# Create directories for our Dockerfiles
mkdir -p dnsroot dnsit dnscom dnsunimib dnsamazon wsunimib wsamazon client

# DNS Root Server
cat > dnsroot/Dockerfile << 'EOF'
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
EOF

cat > dnsroot/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
};
EOF

cat > dnsroot/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type master;
    file "/etc/bind/db.root";
};
EOF

cat > dnsroot/db.root << 'EOF'
$TTL 60000
@               IN  SOA     ROOT-SERVER.    root.ROOT-SERVER. (
                        2025020302 ; serial
                        28800      ; refresh
                        14400      ; retry
                        3600000    ; expire
                        0          ; negative cache ttl
                        )

@               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5

it.             IN  NS      dnsit.it.
dnsit.it.       IN  A       192.168.0.1

com.            IN  NS      dnscom.com.
dnscom.com.     IN  A       192.168.0.2
EOF

# DNS IT Server
cat > dnsit/Dockerfile << 'EOF'
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
COPY db.it /etc/bind/

RUN chown -R bind:bind /etc/bind

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
EOF

cat > dnsit/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
};
EOF

cat > dnsit/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "it" {
    type master;
    file "/etc/bind/db.it";
};
EOF

cat > dnsit/db.root << 'EOF'
.               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5
EOF

cat > dnsit/db.it << 'EOF'
$TTL 60000
@               IN  SOA     dnsit.it.    root.dnsit.it. (
                        2025020302 ; serial
                        28800      ; refresh
                        14400      ; retry
                        3600000    ; expire
                        0          ; negative cache ttl
                        )

@               IN  NS      dnsit.it.
dnsit.it.       IN  A       192.168.0.1

unimib.it.      IN  NS      dnsunimib.unimib.it.
dnsunimib.unimib.it. IN  A  192.168.0.11
EOF

# DNS COM Server
cat > dnscom/Dockerfile << 'EOF'
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
COPY db.com /etc/bind/

RUN chown -R bind:bind /etc/bind

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
EOF

cat > dnscom/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
};
EOF

cat > dnscom/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "com" {
    type master;
    file "/etc/bind/db.com";
};
EOF

cat > dnscom/db.root << 'EOF'
.               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5
EOF

cat > dnscom/db.com << 'EOF'
$TTL 60000
@               IN  SOA     dnscom.com.    root.dnscom.com. (
                        2025020302 ; serial
                        28800      ; refresh
                        14400      ; retry
                        3600000    ; expire
                        0          ; negative cache ttl
                        )

@               IN  NS      dnscom.com.
dnscom.com.     IN  A       192.168.0.2

amazon.com.     IN  NS      dnsamazon.amazon.com.
dnsamazon.amazon.com. IN  A  192.168.0.22
EOF

# DNS UNIMIB Server
cat > dnsunimib/Dockerfile << 'EOF'
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
COPY db.it.unimib /etc/bind/

RUN chown -R bind:bind /etc/bind

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
EOF

cat > dnsunimib/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
};
EOF

cat > dnsunimib/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "unimib.it" {
    type master;
    file "/etc/bind/db.it.unimib";
};
EOF

cat > dnsunimib/db.root << 'EOF'
.               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5
EOF

cat > dnsunimib/db.it.unimib << 'EOF'
$TTL 60000
@               IN  SOA     dnsunimib.unimib.it.    root.dnsunimib.unimib.it. (
                        2025020302 ; serial
                        28        ; refresh
                        14        ; retry
                        3600000   ; expire
                        0         ; negative cache ttl
                        )

@               IN  NS      dnsunimib.unimib.it.
dnsunimib.unimib.it. IN  A  192.168.0.11

pc1.unimib.it.  IN  A       192.168.0.111
wsunimib.unimib.it. IN  A   192.168.0.110
EOF

# DNS AMAZON Server
cat > dnsamazon/Dockerfile << 'EOF'
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
COPY db.com.amazon /etc/bind/

RUN chown -R bind:bind /etc/bind

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
EOF

cat > dnsamazon/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
};
EOF

cat > dnsamazon/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "amazon.com" {
    type master;
    file "/etc/bind/db.com.amazon";
};
EOF

cat > dnsamazon/db.root << 'EOF'
.               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5
EOF

cat > dnsamazon/db.com.amazon << 'EOF'
$TTL 60000
@               IN  SOA     dnsamazon.amazon.com.    root.dnsamazon.amazon.com. (
                        2025020302 ; serial
                        28        ; refresh
                        14400     ; retry
                        3600000   ; expire
                        15        ; negative cache ttl
                        )

@               IN  NS      dnsamazon.amazon.com.
dnsamazon.amazon.com. IN  A  192.168.0.22

pc2.amazon.com. IN  A       192.168.0.222
wsamazon.amazon.com. IN  A   192.168.0.220
EOF

# WSUNIMIB Server
cat > wsunimib/Dockerfile << 'EOF'
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
EOF

cat > wsunimib/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
    allow-recursion { 192.168.0.0/24; };
    auto-dnssec off;
    dnssec-validation no;
    dnssec-enable no;
    dnssec-lookaside no;
    filter-aaaa-on-v4 yes;
    send-cookie no;
};
EOF

cat > wsunimib/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};
EOF

cat > wsunimib/db.root << 'EOF'
.               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5
EOF

# WSAMAZON Server
cat > wsamazon/Dockerfile << 'EOF'
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
EOF

cat > wsamazon/named.conf.options << 'EOF'
options {
    directory "/var/cache/bind";
    allow-recursion { 192.168.0.0/24; };
    auto-dnssec off;
    dnssec-validation no;
    dnssec-enable no;
    dnssec-lookaside no;
    filter-aaaa-on-v4 yes;
    send-cookie no;
};
EOF

cat > wsamazon/named.conf << 'EOF'
include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};
EOF

cat > wsamazon/db.root << 'EOF'
.               IN  NS      ROOT-SERVER.
ROOT-SERVER.    IN  A       192.168.0.5
EOF

# Client
cat > client/Dockerfile << 'EOF'
FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils iputils-ping net-tools curl iproute2 traceroute && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "sleep infinity"]
EOF

# Build all Docker images
echo "Building DNS root server image..."
docker build -t dnsroot-image dnsroot/

echo "Building DNS it server image..."
docker build -t dnsit-image dnsit/

echo "Building DNS com server image..."
docker build -t dnscom-image dnscom/

echo "Building DNS unimib server image..."
docker build -t dnsunimib-image dnsunimib/

echo "Building DNS amazon server image..."
docker build -t dnsamazon-image dnsamazon/

echo "Building wsunimib server image..."
docker build -t wsunimib-image wsunimib/

echo "Building wsamazon server image..."
docker build -t wsamazon-image wsamazon/

echo "Building client image..."
docker build -t client-image client/

echo "All Docker images built successfully"