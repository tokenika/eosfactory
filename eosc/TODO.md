```
Edit > Virtual Network Editor: Host-only
Virtual Machine Settings > Network Adapter: Host-only

ifconfig
## inet 192.168.229.141  netmask 255.255.255.0  broadcast 192.168.229.255
```
eosd config.ini: http-server-endpoint = 192.168.229.141:8888 # Host-only

* Wallet NOT on localhost  -- *
* - Password and/or Private Keys - *
* - are transferred unencrypted.

OK, now trying the tunnel.