# -*- coding: utf-8 -*-

import re
import datetime

from .data import MeasurementData
from .variable import Variable
from .errors import MeasurementRecordError
from .log import logger

date_fmt = r'\(1(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)\)'
sample_time_fmt = r'\([a-zA-Z0-9][a-zA-Z0-9]\)\((\d\d)\)'
variable_size_fmt = r'\((\d+)\)'
var_fmt = r'\((\d*\.?\d+)\)\(([a-zA-Z]+)\)'

re_header = re.compile(
    fr'P\.01{date_fmt}{sample_time_fmt}'
    fr'{variable_size_fmt}{var_fmt}{var_fmt}{var_fmt}{var_fmt}'
)


class MeasurementRecord(object):
    """
    Esta clase permite guardar todo el registro asociado a una fecha.

    Cuando se leen los datos, se listan registros bajo una cabecera que
    proporciona información sobre la fecha, el período de muestreo y los
    nombres de variables. Después de esta cabecera estarán los valores medidos.
    """
    def __init__(self, header_raw: str) -> None:
        """
        Argumentos:
            header_raw (str):
                Línea de texto leído desde archivo para la cabecera.
        """
        super().__init__()
        self.header_raw = header_raw
        self.data: list[MeasurementData] = []
        self.variables: list[Variable] = []
        # Get data from header
        matched = re_header.search(self.header_raw)
        if matched is None:
            raise MeasurementRecordError(header_raw)

        # Get data for date
        try:
            year_str = matched[1]
            month_str = matched[2]
            day_str = matched[3]
            hour_str = matched[4]
            minute_str = matched[5]
            second_str = matched[6]
            # Create date
            full_year_str = f'20{year_str}'
            self.date = datetime.datetime(
                int(full_year_str),
                int(month_str),
                int(day_str),
                int(hour_str),
                int(minute_str),
                int(second_str),
            )
        except Exception as e:
            logger.error(e)
            raise MeasurementRecordError(header_raw)

        # Get data for sample time
        try:
            sample_str = matched[7]
            self.sample = datetime.timedelta(
                minutes=int(sample_str),
            )
        except Exception as e:
            logger.error(e)
            raise MeasurementRecordError(header_raw)

        # Get variable size and variables
        try:
            variable_size_str = matched[8]
            self.variable_size = int(variable_size_str)
            offset = 9

            for i in range(offset, offset + (self.variable_size*2), 2):
                value_str = matched[i]
                unit_name = matched[i + 1]
                logger.debug('Get %s and %s', value_str, unit_name)
                self.variables.append(Variable(float(value_str), unit_name))
        except Exception as e:
            logger.error(e)
            raise MeasurementRecordError(header_raw)

    @staticmethod
    def is_header(header_raw: str) -> bool:
        """
        Esta función evalúa si una línea de texto es o no una cabecera.

        Retorno:
            bool: Retorna `True` si los datos son una cabecera.
        """
        matched = re_header.search(header_raw)
        return matched is not None

    def add(self, data_raw: str):
        """
        Agrega información a un registro.

        Argumentos:
            data_raw (str): El dato crudo para ser procesado y agregado.

        También podría usarse el operador de desplazamiento a la izquierda,
        ``<<``, para agregar los datos.

        .. code:: python
        
            measurement_record = MeasurementRecord(...)
            measurement_record << new_data_1
            measurement_record << new_data_2
            ...
        """
        self << data_raw

    def __lshift__(self, data_raw: str):
        """
        Agrega información a un registro.
        """
        if MeasurementData.is_data(data_raw):
            data = MeasurementData(data_raw)
            self.data.append(data)
        else:
            raise MeasurementRecordError(data_raw)
