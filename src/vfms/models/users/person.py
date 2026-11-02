# Represents a person signed on the system.

class Person:
    # Abstract identity data shared by people registered in VFMS.
    def __init__(
        self    : Person,
        name    : str,
        cpf     : str | int,
    ) -> None:
        if type(self) is Person:
            raise TypeError("You cannot create a Person object directly")

        self.name   = name
        self.cpf    = cpf

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, n: str) -> None:
        if len(n) < 3:
            raise Exception("The name must have at least 3 letters")

        if len(n) > 70:
            raise Exception("The name must have less than 70 letters")

        for letter in n:
            if letter.isdigit():
                raise Exception("The name cannot have numbers")

        self._name = n

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, cpf: str | int) -> None:
        digits = "".join(char for char in str(cpf) if char.isdigit())
        if len(digits) != 11:
            raise ValueError("The cpf must have 11 digits")

        numbers = [int(char) for char in digits]
        if len(set(numbers)) == 1:
            raise ValueError("Invalid cpf")

        def check_digit(values: list[int]) -> int:
            remainder = sum(number * weight for number, weight in zip(values, range(len(values) + 1, 1, -1))) % 11
            return 0 if remainder < 2 else 11 - remainder

        if check_digit(numbers[:9]) != numbers[9] or check_digit(numbers[:10]) != numbers[10]:
            raise ValueError("Invalid cpf")

        self._cpf = digits

    # Special method to uses with print(d), where d is a Driver class
    def __str__(self) -> str:
        return f"""Name: {self.name}
cpf: {self.cpf}"""


    # Special method to uses with print(repr(d)), where d is a Driver class
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, cpf={self.cpf})"


    # Special method to compare objects using the cpf (Ex: d1 == d2 -> d1.cpf == v2.cpf, where d1 and d2 are from Driver class)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.cpf == other.cpf

