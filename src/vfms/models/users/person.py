"""represents a person signed on system"""

class Person:
    def __init__(
        self, 
        name    : str,
        cpf     : int,
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
    def cpf(self, n):
        n = str(n)

        n = n.replace("-", "").replace(".", "")

        l = len(n)
        
        if l < 11 or l > 11:
            raise Exception("The cpf must have 11 digits")
        
        for letter in n:
            try:
                letter = int(letter)
            except:
                raise Exception("The cpf is only digits") 

        n = int(n)
            

        self._cpf = n

    """
    Special method to uses with print(d), where d is a Driver class
    """
    def __str__(self) -> str:
        return f"""Name: {self.name}
cpf: {self.cpf}"""
    
    """
    Special method to uses with print(repr(d)), where d is a Driver class
    """
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, cpf={self.cpf})"

    """
    Special method to compare objects using the cpf (Ex: d1 == d2 -> d1.cpf == v2.cpf, where d1 and d2 are from Driver class)
    """
    def __eq__(self, other) -> bool:
        return self.cpf == other.cpf
    