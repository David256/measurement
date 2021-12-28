# -*- coding: utf-8 -*-

import re

from .errors import MeasurementRecordError
from .log import logger

logger = logger.getChild('Data')

col_fmt = r'\((\d*\.?\d+)\)'

re_data = re.compile(
    f'{col_fmt}{col_fmt}{col_fmt}{col_fmt}',
)


class MeasurementData(object):
    """
    Esta clase almacena la información de datos para un período de lectura.
    """
    def __init__(self, data_raw: str) -> None:
        """
        Argumentos:
            data_raw (str): Línea de texto con información de lectura.
        """
        object.__init__(self)
        self.data_raw = data_raw
        # Get data
        matched = re_data.search(data_raw)
        if matched is None:
            raise MeasurementRecordError(data_raw)

        logger.debug('Data is %s', data_raw)
        logger.debug('Matched groups: %s', matched.groups())

        self.__cell: list[float] = []
        for item in matched.groups():
            logger.debug('Adding %s', item)
            self.__cell.append(float(item))

    @staticmethod
    def is_data(data_raw: str) -> bool:
        """
        Determina si una línea de texto para datos de lectura es correcto.

        Retorno:
            bool: Retorna `True` si el formato es correcto.
        """
        matched = re_data.search(data_raw)
        return matched is not None

    def __getitem__(self, index: int) -> float:
        """
        Argumentos:
            index (int): Índice para acceder a un dato del registro.

        Retorno:
            float: Valor en el índice solicitado.
        """
        return self.__cell[index]
