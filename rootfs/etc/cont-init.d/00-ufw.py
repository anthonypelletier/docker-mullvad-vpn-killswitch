#!/usr/local/bin/python3
import os
import re
import pydig
import pyufw

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(ROOT_PATH, 'etc', 'openvpn')


def get_allowed_ips(country=None):
    hosts = dict()
    for filename in os.listdir(CONFIG_PATH):
        if filename.endswith(".conf"):
            if country and filename != 'mullvad_{}_all.conf'.format(country):
                continue
            with open(os.path.join(CONFIG_PATH, filename), 'r') as configfile:
                hosts.update(dict(re.findall(r"remote (.+)\.mullvad\.net (\d{2,5})", configfile.read())))

    ips = dict()
    for name, port in hosts.items():
        for ip in pydig.query('{}.mullvad.net'.format(name), 'A'):
            ips[ip] = port
    return ips


def setup_killswitch(ips):
    pyufw.reset(force=True)
    pyufw.default(incoming='deny', outgoing='deny', routed='reject')
    pyufw.add("allow out on tun+")
    pyufw.add("allow in on tun+")
    pyufw.add("allow out on lo")
    pyufw.add("allow in on lo")
    pyufw.add("allow out to any port 53")
    pyufw.add("allow in from any port 53")
    for ip, port in ips.items():
        pyufw.add("allow out on eth+ to {} port {} proto udp".format(ip, port))
        pyufw.add("allow in on eth+ from {} port {} proto udp".format(ip, port))
    pyufw.add("allow out to 172.0.0.0/8")
    pyufw.add("allow in to 172.0.0.0/8")


def setup_userpass(userpass):
    if userpass is None:
        print('Error: Please set VPN_USERPASS environment variable !')
        exit(1)
    with open(os.path.join(CONFIG_PATH, 'mullvad_userpass.txt'), 'w') as userpassfile:
        userpassfile.write('{}\nm'.format(userpass))


if __name__ == '__main__':
    setup_userpass(userpass=os.getenv('VPN_USERPASS', None))
    setup_killswitch(get_allowed_ips(country=os.getenv('VPN_COUNTRY', 'fr')))
