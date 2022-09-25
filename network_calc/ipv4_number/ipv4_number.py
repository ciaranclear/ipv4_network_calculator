import re


class IPv4NumberError(Exception):

    def __init__(self, message: str) -> None:
        """
        takes an error message and initializes an IPv4NumberError.
        """
        super().__init__(message)


class IPv4Number:

    @classmethod
    def valid_number(cls, number: str) -> str:
        """
        takes the string repressentation of an ipv4 number and validates that
        it is four '.' seperated numbers in the range 0 -> 255. if not
        valid raises IPv4NumberError. if valid return the valid ipv4 number.
        """

        if not isinstance(number, str):
            msg = f"ipv4 number needs to be string not {type(number)}"
            raise IPv4NumberError(msg)
        octets = number.split('.')
        if len(octets) != 4:
            msg = (f"Invalid ipv4 number {number}. "
                   f"ipv4 number must be 4 '.' seperated numbers")
            raise IPv4NumberError(msg)
        try:
            nums = [int(n) for n in octets]
        except ValueError:
            msg = (f"ipv4 number {number} contains one or more invalid characters. "
                   f"Must be four '.' seperated numbers in range 0 -> 255")
            raise IPv4NumberError(msg)

        for num in nums:
            if num < 0 or num > 255:
                msg = (f"Invalid ipv4 number {number}. "
                       f"ipv4 octet values must be in range 0 -> 255")
                raise IPv4NumberError(msg)

        return '.'.join([str(n).rjust(3, '0') for n in nums])

    @classmethod
    def format_binary(cls, binary: str) -> str:
        """
        takes a binary string in the form '0b11110000' where the '0b' is optional.
        the binary string value must be in the range of an unsigned 32 bit int.
        returns binary string of 32 bits preceeded by '0b'.
        """
        if not isinstance(binary, str):
            msg = (f"Binary value type is {type(binary)}. "
                   f"Must be type string")
            raise IPv4NumberError(msg)
        pat = re.compile(r'^0?b?([0-1]+)$')
        res = pat.match(binary)
        if not res:
            msg = (f"Non valid binary string value {binary}."
                   f"Must be an optional '0b' followed by '1' and '0' characters")
            raise IPv4NumberError(msg)
        else:
            binary = res.group(1)
        n = int(binary, 2)
        if n < 0 or n > 2**32:
            msg = (f"Integer value {n} of binary value is out of range. "
                   f"Must be 0 -> {2**32}")
            raise IPv4NumberError(msg)
        binary = binary.rjust(32, '0')
        return '0b' + binary

    @classmethod
    def number_to_binary(cls, number: str) -> str:
        """
        takes the string repressentation of an ipv4 number and converts it to
        a string repressentation of a 32 bit 0 left padded binary number
        beginning with '0b'.
        """
        number = IPv4Number.valid_number(number)
        octets = [int(s) for s in number.split('.')]
        binary = bin(octets[0] << 24 | octets[1] << 16 | octets[2] << 8 | octets[3])
        binary = IPv4Number.format_binary(binary)
        return binary

    @classmethod
    def binary_to_number(cls, binary: str) -> str:
        """
        takes the string repressentation of a binary number. if binary value is
        not valid raises IPv4NumberError. if binary value is valid returns a
        string repressentation of an ipv4 number.
        """
        b = IPv4Number.format_binary(binary)
        if b[0:2] == '0b': b = b[2:]
        octets = [int(b[0:8], 2), int(b[8:16], 2), int(b[16:24], 2), int(b[24:32], 2)]
        octets = [str(n).rjust(3, '0') for n in octets]
        return '.'.join(octets)

    @classmethod
    def invert_binary(cls, binary: str) -> str:
        """
        takes a binary string and returns a binary string with the inverted value. 
        """
        binary = IPv4Number.format_binary(binary)
        binary = bin(int(binary, 2) ^ 2**32)
        return IPv4Number.format_binary(binary)

    @classmethod
    def number_to_integer(cls, number: str) -> str:
        """
        takes the string repressentation of an ipv4 number and returns its
        integer value.
        """
        IPv4Number.valid_number(number)
        binary = IPv4Number.number_to_binary(number)
        return int(binary, 2)

    @classmethod
    def integer_to_number(cls, integer):
        """
        takes an integer value. if integer value is not valid raises an
        IPv4NumberError. if integer value is valid returns the string
        repressentation of an ipv4 number.
        """
        if not isinstance(integer, int):
            msg = f"Integer value type is {type(integer)}. Must be type int"
            raise IPv4Number(msg)
        if not (0 <= integer < 2**32):
            msg = f"Integer value {integer} is out of range. Must be in range 0 -> {2**32}"
            raise IPv4NumberError(msg)
        binary = bin(integer)
        return IPv4Number.binary_to_number(binary)

    @classmethod
    def invert_number(cls, number: str) -> str:
        """
        returns the inverted ipv4 number.
        """
        number = IPv4Number.valid_number(number)
        binary = IPv4Number.number_to_binary(number)
        binary = IPv4Number.invert_binary(binary)
        return IPv4Number.binary_to_number(binary)

    def __init__(self, number: str) -> None:
        """
        takes the string repressentation of an ipv4 number. if number is
        valid will set that number.
        """
        self._number = IPv4Number.valid_number(number)

    def __str__(self) -> str:
        """
        returns the string repressentation of an ipv4 number.
        """
        return self._number

    @property
    def number(self) -> str:
        """
        returns a string repressentation of an ipv4 number.
        """
        return self._number

    @number.setter
    def number(self, number: str) -> None:
        """
        takes the string repressentation of an ipv4 number.
        """
        self._number = IPv4Number.valid_number(number)

    @property
    def binary(self) -> str:
        """
        returns the string repressentation of a binary number with
        the binary value of the ipv4 number.
        """
        return IPv4Number.number_to_binary(self._number)

    @binary.setter
    def binary(self, binary: str) -> None:
        """
        takes the string repressentation of a binary number and sets
        its ipv4 number equivalent value.
        """
        self._number = IPv4Number.binary_to_number(binary)

    @property
    def integer(self):
        """
        returns the integer value of the ipv4 number.
        """
        return IPv4Number.number_to_integer(self._number)

    @integer.setter
    def integer(self, integer):
        """
        takes an integer value. if integer is valid will set the
        ipv4 numberequivalent.
        """
        self._number = IPv4Number.integer_to_number(integer)

