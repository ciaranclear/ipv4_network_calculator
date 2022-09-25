from ipv4_number.ipv4_number import IPv4Number
from ipv4_address.ipv4_address import IPv4Address, IPv4AddressError
from ipv4_subnet_mask.ipv4_subnet_mask import IPv4SubnetMask
import re


class IPv4NetworkError(Exception):

    def __init__(self, message: str) -> None:
        """
        
        """
        super().__init__(message)


class IPv4Network:

    @classmethod
    def valid_network(cls, network_address: str, subnet_mask: str) -> str:
        """

        """
        network_address = IPv4Network.valid_network_address(network_address)
        subnet_mask = IPv4SubnetMask.valid_subnet_mask(subnet_mask)
        classfull_subnet = IPv4Address.classfull_subnet(network_address)
        if classfull_subnet:
            address_integer = IPv4Number.number_to_integer(classfull_subnet)
            subnet_integer = IPv4Number.number_to_integer(subnet_mask)
            if address_integer > subnet_integer:
                msg = (f"Subnet mask {subnet_mask} is to small for "
                       f"the given network address {network_address}. \n"
                       f"{address_integer} addresses required but capacity only {subnet_integer}")
                raise IPv4NetworkError(msg)
        else:
            msg = f"Invalid network address {network_address}. Must be Class 'A','B','C'."
            raise IPv4NetworkError(msg)

    @classmethod
    def valid_network_address(cls, network_address: str) -> str:
        """

        """
        network_address = IPv4Address.valid_address(network_address)
        integer = IPv4Number.number_to_integer(network_address)
        if integer % 2 != 0:
            msg = (f"Invalid network address {network_address}. "
                   f"Must be an even number.")
            raise IPv4NetworkError(msg)
        address_class = IPv4Address.address_class(network_address)
        if address_class not in ['A','B','C']:
            msg = (f"Invalid network address {network_address}. "
                   f"Must be a Class 'A','B','C' address.")
            raise IPv4AddressError(msg)
        return network_address

    @classmethod
    def valid_broadcast_address(cls, broadcast_address: str, subnet_mask: str) -> str:
        """

        """
        broadcast_address = IPv4Address.valid_address(broadcast_address)
        subnet_mask = IPv4SubnetMask.valid_subnet_mask(subnet_mask)
        broadcast_binary = IPv4Number.number_to_binary(broadcast_address)
        subnet_binary = IPv4Number.number_to_binary(subnet_mask)
        broadcast_binary = re.search(r"^0?b?([0-1]*)$", broadcast_binary).group(1)
        subnet_binary = re.search(r"^0?b?([0-1]*)$", subnet_binary).group(1)
        for i in range(len(subnet_binary)):
            if subnet_binary[i] == '0' and broadcast_binary[i] != '1':
                msg = (f"Invalid broadcast address {broadcast_address} "
                       f"for subnet mask {subnet_mask}.")
                raise IPv4NetworkError(msg)
        return broadcast_address

    @classmethod
    def broadcast_address(cls, network_address: str, subnet_mask: str) -> str:
        """

        """
        network_address = IPv4Network.valid_network_address(network_address)
        subnet_mask = IPv4SubnetMask.valid_subnet_mask(subnet_mask)
        network_binary = IPv4Number.number_to_binary(network_address)
        subnet_binary = IPv4Number.number_to_binary(subnet_mask)
        network_binary = re.search(r"^0?b?([0-1]*)$", network_binary).group(1)
        subnet_binary = re.search(r"^0?b?([0-1]*)$", subnet_binary).group(1)
        broadcast_binary = ''
        for i in range(len(network_binary)):
            if subnet_binary[i] == '0':
                broadcast_binary += '1'
            if subnet_binary[i] != '0':
                broadcast_binary += network_binary[i]
        return IPv4Number.binary_to_number(broadcast_binary)

    def __init__(self, network_address: str, subnet_mask: str) -> None:
        """

        """
        IPv4Network.valid_network(network_address, subnet_mask)
        self._network_address = IPv4Network.valid_network_address(network_address)
        self._subnet_mask = IPv4SubnetMask.valid_subnet_mask(subnet_mask)

    def __str__(self) -> str:
        """

        """
        return (f"network {self._network_address}\n"
                f"subnet {self._subnet_mask}\n"
                f"broadcast {self.broadcast_addr()}\n"
                f"number of networks {self.number_of_networks()}\n"
                f"number of hosts {self.number_of_hosts()}\n"
                f"first host address {self.first_host_address()}\n"
                f"last host address {self.last_host_address()}")

    def broadcast_addr(self) -> str:
        """

        """
        return IPv4Network.broadcast_address(self._network_address, self._subnet_mask)

    def number_of_networks(self) -> int:
        """

        """
        return IPv4SubnetMask.number_of_networks(self._subnet_mask)

    def number_of_hosts(self) -> int:
        """

        """
        return IPv4SubnetMask.number_of_hosts(self._subnet_mask)

    def first_host_address(self) -> str:
        """

        """
        network_integer = IPv4Number.number_to_integer(self._network_address)
        first_host_integer = network_integer + 1
        return IPv4Number.integer_to_number(first_host_integer)

    def last_host_address(self) -> str:
        """

        """
        broadcast_integer = IPv4Number.number_to_integer(self.broadcast_addr())
        last_host_integer = broadcast_integer - 1
        return IPv4Number.integer_to_number(last_host_integer)

    def host_in_network(self, address: str) -> bool:
        """

        """
        address = IPv4Address.valid_address(address)
        address_integer = IPv4Number.number_to_integer(address)
        first_integer = IPv4Number.number_to_integer(self.first_host_address())
        last_integer = IPv4Number.number_to_integer(self.last_host_address())
        return first_integer <= address_integer <= last_integer
