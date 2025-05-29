$TTL    60000
@               IN      SOA     dnscom.com.    root.dnscom.com. (
                        2024120401 ; serial
                        28800 ; refresh
                        14400 ; retry
                        3600000 ; expire
                        0 ; negative cache ttl
                        )
@                    IN      NS      dnscom.com.
dnscom.com.          IN      A       192.168.0.2

amazon.com.          IN     NS      dnsamazon.amazon.com.
dnsamazon.amazon.com. IN     A       192.168.0.22
