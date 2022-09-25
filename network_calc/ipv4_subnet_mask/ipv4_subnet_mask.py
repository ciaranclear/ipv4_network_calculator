from typing import Optional, Sequence
from ipv4_number.ipv4_number import IPv4Number, IPv4NumberError
import re


class IPv4SubnetMaskError(Exception):

    def __init__(self, message: str) -> None:
        """
        takes an error message and initializes an IPv4SubnetMaskError.
        """
        super().__init__(message)


class IPv4SubnetMask:

    @classmethod
    def valid_subnet_mask(cls, subnet_mask: str) -> str:
        """
        takes a string repressentation of a subnet mask.
        if valid returns the subnet mask else raises exception.
        """
        try:
            subnet_mask = IPv4Number.valid_number(subnet_mask)
        except IPv4NumberError as e:
            raise IPv4SubnetMaskError(e.__str__())
        binary = IPv4Number.number_to_binary(subnet_mask)
        pat = re.compile(r'^0?b?1*0*$')
        res = pat.match(binary)
        if not res:
            msg = (f"Invalid subnet mask {subnet_mask}")
            raise IPv4SubnetMaskError(msg)
        return subnet_mask

    @classmethod
    def valid_slash_notation(cls, slash: str) -> str:
        """
        takes a string repressentation of a subnet slash.
        if valid returns the subnet slash else raises exception.
        """
        if not isinstance(slash, str):
            msg = f"Slash value is type {type(slash)}. Should be string"
            raise IPv4SubnetMaskError(msg)
        pat = re.compile(r'^/([0-9]{1,2})$')
        res = pat.match(slash)
        if not res:
            msg = (f"Invalid slash value {slash}. "
                   f"Slash must be '/' followed by integer value")
            raise IPv4SubnetMaskError(msg)
        if not 0 <= int(res.group(1)) <= 32:
            msg = (f"Invalid slash integer value {slash}. "
                   f"Slash must be '/' followed by integer in range 0 -> 32")
            raise IPv4SubnetMaskError(msg)
        return slash

    @classmethod
    def subnet_mask_to_slash(cls, subnet_mask: str) -> str:
        """
        takes a string repressentation of a subnet mask and returns
        the string repressentation of a subnet slash.
        """
        IPv4SubnetMask.valid_subnet_mask(subnet_mask)
        b = IPv4Number.number_to_binary(subnet_mask)
        return f"/{b.count('1')}"

    @classmethod
    def slash_to_subnet_mask(cls, slash: str) -> str:
        """
        takes a string repressentation of a subnet slash and returns
        the string repressentation of a subnet mask
        """
        IPv4SubnetMask.valid_slash_notation(slash)
        n = int(slash[1:])
        b = '1' * n
        b = b.ljust(32, '0')
        return IPv4Number.binary_to_number(b)

    @classmethod
    def valid_wildcard(cls, wildcard: str) -> str:
        """
        takes a string repressentation of a wildcard.
        if valid returns the wildcard else raises exception.
        """
        try:
            wildcard = IPv4Number.valid_number(wildcard)
        except IPv4NumberError as e:
            raise IPv4SubnetMaskError(e.message)
        binary = IPv4Number.number_to_binary(wildcard)
        pat = re.compile(r'^0?b?0*1*$')
        res = pat.match(binary)
        if not res:
            msg = (f"Invalid wildcard {wildcard}. "
                f"'1' found before '0'. "
                f"'1' must follow '0' characters")
            raise IPv4SubnetMaskError(msg)
        return wildcard

    @classmethod
    def wildcard_to_subnet_mask(cls, wildcard: str) -> str:
        """
        takes a string repressentation of a wildcard and returns
        a string repressentation of its subnet mask value.
        """
        return IPv4Number.invert_number(wildcard)

    @classmethod
    def subnet_mask_to_wildcard(cls, subnet_mask: str) -> str:
        """
        takes a string repressentation of a subnet mask and return
        the string repressentation of its wildcard value.
        """
        return IPv4Number.invert_number(subnet_mask)

    @classmethod
    def number_of_hosts(cls, subnet_mask: str) -> int:
        """
        takes a string repressentation of a subnet mask and returns
        an integer value of the number of hosts it can accomodate.
        """
        IPv4SubnetMask.valid_subnet_mask(subnet_mask)
        b = IPv4Number.number_to_binary(subnet_mask)
        c = b.count('1')
        return (2 ** (32 - c)) - 2

    @classmethod
    def hosts_to_subnet_mask(cls, hosts: int, cidr: Optional[bool]=False) -> str:
        """
        takes an integer value for the number of hosts and a cidr boolean flag.
        returns a subnet mask that can accomodate the number of hosts provided.
        if the cidr flag is set to true a variable length subnet mask can be
        returned. cidr flag defaults to false which will return a classfull
        subnet.
        """
        if not isinstance(hosts, int):
            msg = f"hosts must be type int not type {type(hosts)}"
            raise IPv4SubnetMaskError(msg)
        if not (0 < hosts < 2**32):
            msg = (f"hosts value {hosts} is out of range. "
                   f"Must be in range 0 -> {2**32}")
            raise IPv4SubnetMaskError(msg)

        n = 1 if cidr else 256

        while n < 2**32:
            if (n - 2) >= hosts:
                number = IPv4Number.integer_to_number(2**32  - n)
                return number
            n *= 2

    @classmethod
    def number_of_networks(cls, subnet_mask: str) -> int:
        """
        takes the string repressentation of a subnet mask and returns
        an integer value for the number of networks the subnet can
        accomodate. 
        """
        IPv4SubnetMask.valid_subnet_mask(subnet_mask)
        b = IPv4Number.number_to_binary(subnet_mask)
        c = b.count('1')
        return 2 ** c

    @classmethod
    def shortest_subnet_mask(cls, subnet_masks: Sequence[str]) -> str:
        """
        takes a list of subnet masks and returns the subnet mask with
        the lowest number of leading ones.
        """
        subnet_integers = []

        for subnet_mask in subnet_masks:
            IPv4SubnetMask.valid_subnet_mask(subnet_mask)
            subnet_integers.append(IPv4Number.number_to_integer(subnet_mask))

        subnet_integers.sort()
        shortest = subnet_integers[0]
        return IPv4Number.integer_to_number(shortest)

    @classmethod
    def longest_subnet_mask(cls, subnet_masks: Sequence[str]) -> str:
        """
        takes a list of subnet masks and returns the subnet mask with
        the highest number of leading ones.
        """
        subnet_integers = []

        for subnet_mask in subnet_masks:
            IPv4SubnetMask.valid_subnet_mask(subnet_mask)
            subnet_integers.append(IPv4Number.number_to_integer(subnet_mask))

        subnet_integers.sort()
        subnet_integers.reverse()
        shortest = subnet_integers[0]
        return IPv4Number.integer_to_number(shortest)

    def __init__(self, subnet_mask: str) -> None:
        """
        takes the string repressentation of a subnet mask.
        """
        self._subnet_mask = IPv4SubnetMask.valid_subnet_mask(subnet_mask)

    def __str__(self) -> str:
        """
        returns the string repressentation of this subnet mask.
        """
        return self._subnet_mask

    @property
    def subnet_mask(self) -> str:
        """
        returns the string repressentation of this subnet mask.
        """
        return self._subnet_mask

    @subnet_mask.setter
    def subnet_mask(self, subnet_mask: str) -> None:
        """
        takes the string repressentation of a subnet mask and sets that value.
        """
        self._subnet_mask = IPv4SubnetMask.valid_subnet_mask(subnet_mask)

    @property
    def slash(self) -> str:
        """
        returns the string repressentation of this subnet mask.
        """
        return IPv4SubnetMask.subnet_mask_to_slash(self._subnet_mask)

    @slash.setter
    def slash(self, slash: str) -> None:
        """
        takes the string repressentation of a subnet slash and sets this
        subnet mask to that value.
        """
        self._subnet_mask = IPv4SubnetMask.slash_to_subnet_mask(slash)

    @property
    def wildcard(self) -> None:
        """
        returns a string repressentation of a wildcard for the subnet mask.
        """
        return IPv4SubnetMask.subnet_mask_to_wildcard(self._subnet_mask)

    @wildcard.setter
    def wildcard(self, wildcard: str) -> None:
        """
        takes the string repressentation of a wildcard and.
        """
        self._subnet_mask = IPv4SubnetMask.wildcard_to_subnet_mask(wildcard)

    def max_networks(self) -> int:
        """
        returns an integer value for the maximum number of networks the subnet
        mask can accomodate.
        """
        return IPv4SubnetMask.number_of_networks(self._subnet_mask)

    def max_hosts(self) -> int:
        """
        returns an integer value for the maximum number of hosts the subnet
        mask can accomodate.
        """
        return IPv4SubnetMask.number_of_hosts(self._subnet_mask)
