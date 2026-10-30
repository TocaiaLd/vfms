"""represents a person signed on system"""

class Person:
    def __init__(
        self    : Person, 
        name    : str,
        cpf     : str,
    ):
        if type(self) is Person:
            raise TypeError("You cannot create a Person object directly")
        
        self.name   = name
        self.cpf    = cpf

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, n):
        if len(n) < 3:
            raise Exception("The name must have at least 3 letters")

        if len(n) > 70:
            raise Exception("The name must have less than 70 letters")

        for letter in n:
            if letter.isdigit():
                raise Exception("The name cannot have numbers")

        self._name = n

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf):
        cpf_to_setter   = cpf
        first_number    = 0
        second_number   = 0
        count           = 11
        
        # Gets a rest of a number divided by 11
        def get_rest(number) -> int:
            r = number % 11 
            if r < 2:
                return 0
            else:
                return (11 - r)

        # If is not a string, convert to it
        if not isinstance(cpf_to_setter, str):
            cpf_to_setter = str(cpf_to_setter)

        cpf_length = len(cpf_to_setter)
        
        if cpf_length < 11 or cpf_length > 11:
            raise Exception("The cpf must have 11 digits")
        
        # Checks if all characters are numbers
        for digit in cpf_to_setter:
            try:
                digit = int(digit)
            except:
                raise Exception("The cpf is only digits") 
            
        for index, char in enumerate(cpf):
            number = int(char)

            if index <= 9:
                second_number += number * count
                
                if index <= 8:
                    first_number += number * (count - 1)
                    if index == 8:
                        first_number = get_rest(first_number)
    
                if index == 9:
                    second_number = get_rest(second_number)
                    break
                
            count -= 1

        if first_number != int(cpf_to_setter[9]) or second_number != int(cpf_to_setter[10]):
            print(first_number)
            print(second_number)
            raise Exception("Invalid cpf!")

        self._cpf = cpf_to_setter

    # Special method to uses with print(d), where d is a Driver class
    def __str__(self) -> str:
        return f"""Name: {self.name}
cpf: {self.cpf}"""
    
    
    # Special method to uses with print(repr(d)), where d is a Driver class
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, cpf={self.cpf})"

    
    # Special method to compare objects using the cpf (Ex: d1 == d2 -> d1.cpf == v2.cpf, where d1 and d2 are from Driver class)
    def __eq__(self, other) -> bool:
        return self.cpf == other.cpf
    