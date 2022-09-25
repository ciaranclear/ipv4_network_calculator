from ipv4_number.ipv4_number import IPv4Number, IPv4NumberError


class IPv4AddressError(Exception):

    def __init__(self, message):
        """
        takes an error message and initializes an IPv4AddressError.
        """
        super().__init__(message)


class IPv4Address:

    @classmethod
    def valid_address(cls, address):
        """
        takes the string repressentation of an ipv4 address. if address is
        not valid raises an IPv4AddressError. if address is valid returns
        the valid address.
        """
        try:
            address = IPv4Number.valid_number(address)
        except IPv4NumberError as e:
            raise IPv4AddressError(e.__str__())
        else:
            return address

    @classmethod
    def address_class(cls, address):
        """
        takes the string repressentation of an ipv4 address. if address is
        not valid raises IPv4AddressError. if address valid returns the
        letter repressentation of the address class ie 'A','B','C','D','E'.
        """
        try:
            b = IPv4Number.number_to_binary(address)
        except IPv4NumberError as e:
            raise IPv4AddressError(e.__str__())
        if b[0:2] == '0b':
            b = b[2:]
        if b[0:4] == '1111':
            return 'E'
        if b[0:3] == '111':
            return 'D'
        if b[0:2] == '11':
            return 'C'
        if b[0] == '1':
            return 'B'
        if b[0] == '0':
            return 'A'

    @classmethod
    def classfull_subnet(cls, address):
        """
        takes the string repressentation of an ipv4 address. returns
        the subnet mask for class 'A','B','C' addresses else returns None.
        """
        ac = IPv4Address.address_class(address)
        if ac == 'A':
            return "255.000.000.000"
        if ac == 'B':
            return "255.255.000.000"
        if ac == 'C':
            return "255.255.255.000"
        else:
            return None

    def __init__(self, address):
        """
        takes the string repressentation of an ipv4 address. if address is
        valid sets that address else raises an IPv4AddressError.
        """
        try:
            self._address = IPv4Address.valid_address(address)
        except IPv4NumberError as e:
            raise IPv4AddressError(e.__str__())

    def __str__(self):
        """
        returns the string repressentation of an ipv4 address.
        """
        return self._address

    def address_class_letter(self):
        """
        returns the ipv4 address class letter.
        """
        return IPv4Address.address_class(self._address)

    def classfull_subnet_mask(self):
        """
        returns the ipv4 address classfull subnet.
        """
        return IPv4Address.classfull_subnet(self._address)
