# -*- coding: utf-8 -*-


class Variable(object):
    """
    Esta clase representa las variables en una cabecera de registro.
    """
    def __init__(self, value: float, unit_name: str) -> None:
        """
        Argumentos:
            value (float): Representa el valor de la varible.
            unit_name (str): Representa la unidad de medida.
        """
        object.__init__(self)
        self.value = value
        self.unit_name = unit_name

    def __repr__(self) -> str:
        return f'<Variable {self.value} {self.unit_name}>'
