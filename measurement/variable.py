# -*- coding: utf-8 -*-


class Variable(object):
    def __init__(self, value, unit_name) -> None:
        object.__init__(self)
        self.value = value
        self.unit_name = unit_name

    def __repr__(self) -> str:
        return f'<Variable {self.value} {self.unit_name}>'
