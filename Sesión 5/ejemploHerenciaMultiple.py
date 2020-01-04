class Persona:
    def __init__(self, nombre: str, apellido: str, edad: int, sexo: str):
        assert sexo == 'M' or sexo == 'F'
        assert edad >= 0
        self.name = nombre
        self.surname = apellido
        self.age = edad
        self.sex = sexo


class Alumno(Persona):
    def __init__(self, nombre: str, apellido: str, edad: int, sexo: str,
                 grado: str, ident: str):
        self.grade = grado
        self.id = ident
        Persona.__init__(self, nombre, apellido, edad, sexo)


class Empleado(Persona):
    def __init__(self, nombre: str, apellido: str, edad: int, sexo: str,
                 salario: float, ident: str):
        self.salary = salario
        self.id = ident
        Persona.__init__(self, nombre, apellido, edad, sexo)


class Becario(Alumno, Empleado):
    def __init__(self, nombre: str, apellido: str, edad: int, sexo: str,
                 grado: str, salario: float, ident: str):
        Alumno.__init__(self, nombre, apellido, edad, sexo, grado, ident)
        Empleado.__init__(self, nombre,  apellido, edad, sexo, salario, ident)


ejemplo = Becario('Mariano', 'Fernandez', 25, 'M',
                  'Electr.', 12000, '40240132W')
print(ejemplo.salary, ejemplo.grade)
