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

        self._name = n

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, n):
        l = len(n)
        if n < 11 or n > 11:
            raise Exception("The cpf must have 11 digits")

        self._name = n

    