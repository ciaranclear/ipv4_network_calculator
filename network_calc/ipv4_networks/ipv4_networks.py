from typing import Dict, List, Sequence
from ipv4_subnet_mask.ipv4_subnet_mask import IPv4SubnetMask
from ipv4_network.ipv4_network import IPv4Network
from ipv4_number.ipv4_number import IPv4Number

Networks = Sequence[Sequence]


class IPv4NetworksError(Exception):
    def __init__(self, message: str) -> None:
        """

        """
        super().__init__(message)


def min_hosts(hosts, cidr: bool=False) -> int:
    """

    """
    if not isinstance(hosts, int):
        msg = f"hosts must be type int not type {type(hosts)}"
        raise IPv4NetworksError(msg)
    if not (0 < hosts < 2**32):
        msg = (f"hosts value {hosts} is out of range. "
               f"Must be in range 0 -> {2**32}")
        raise IPv4NetworksError(msg)

    n = 1 if cidr else 256

    while n < 2**32:
        if (n - 2) >= hosts:
            return n - 2
        n *= 2

def order_networks(networks: Networks) -> Networks:
    """

    """
    networks.sort(key=lambda x: x[1])
    networks.reverse()
    return networks

def networks_fit(
        networks: Networks,
        subnet_mask: str,
        cidr: bool=False
    ) -> bool:
    """

    """
    networks = order_networks(networks)
    addresses = 0
    for network in networks:
        addresses += (min_hosts(network[1] + 2, cidr))
    max_addresses = IPv4SubnetMask.number_of_hosts(subnet_mask) + 2
    if addresses > max_addresses:
        msg = f""
        raise IPv4NetworksError(msg)
    return True

def make_networks(
        networks: Networks,
        network_address: str,
        subnet_mask: str,
        cidr: bool=False
    ) -> Dict[str,IPv4Network]:
    """

    """
    networks = order_networks(networks)
    networks_fit(networks, subnet_mask, cidr)
    network_objs = {}

    for network in networks:
        name = network[0]
        hosts = network[1]
        subnet_mask = IPv4SubnetMask.hosts_to_subnet_mask(hosts, cidr)
        net_obj = IPv4Network(network_address, subnet_mask)
        network_objs[name] = net_obj
        integer = IPv4Number.number_to_integer(net_obj.broadcast_addr())
        integer += 1
        network_address = IPv4Number.integer_to_number(integer)
    return network_objs

