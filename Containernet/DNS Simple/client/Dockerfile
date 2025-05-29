FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils iputils-ping net-tools curl iproute2 traceroute && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "sleep infinity"]
