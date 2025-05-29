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
