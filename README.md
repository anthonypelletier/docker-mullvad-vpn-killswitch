# Docker Mullvad VPN killswitch
Simple Mullvad VPN with killswitch security

## Quick Start :
```bash
git clone https://github.com/anthonypelletier/docker-mullvad-vpn-killswitch.git
touch docker-compose.yml
```

Replace VPN_USERPASS and VPN_COUNTRY
```yaml
version: '3'
services:
  vpn:
    container_name: vpn
    build:
      context: ./docker-mullvad-vpn-killswitch
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun
    sysctls:
      - net.ipv6.conf.all.disable_ipv6=0
    environment:
      - VPN_COUNTRY=fr
      - VPN_USERPASS=*****
    restart: unless-stopped

  alpine:
    container_name: alpine
    image: alpine
    network_mode: service:vpn
    depends_on:
      - vpn
    command: sleep 3600
    restart: unless-stopped
```

```bash
docker-compose up -d
```
Enjoy :)