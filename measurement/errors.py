# -*- coding: utf-8 -*-


class MeasurementError(Exception):
    """
    This exception is thrown  when a generic error happens.
    """
    def __init__(self, code: str, message: str) -> None:
        Exception.__init__(self, f'{code}: {message}')


class MeasurementFileNotFoundError(MeasurementError):
    """
    This exception is thrown when the data file is not found.
    """
    code = 'EX001'

    def __init__(self, filename: str) -> None:
        message = f'No se encuentra el archivo fuente {filename}'
        MeasurementError.__init__(self, self.code, message)


class MeasurementDestinationNotFoundError(MeasurementError):
    """
    This exception is thrown when the destination file can not be found.
    """
    def __init__(self, destination_path: str) -> None:
        message = 'No se encuentra la ruta destino'
        MeasurementError.__init__(self, self.code, message)


class MeasurementRecordError(MeasurementError):
    """
    This exception is thrown when the data format is invalid or it can not be
    read.
    """
    code = 'EX003'

    def __init__(self, record_raw: str) -> None:
        message = 'Error en la información del registro ' \
            f'{record_raw}'
        MeasurementError.__init__(self, self.code, message)


class MeasurementUnhandledError(MeasurementError):
    """
    """
    code = 'EX004'

    def __init__(self, e: Exception) -> None:
        message = f'Error generado por Python o SO el cual entrega: {e}'
        MeasurementError.__init__(self, self.code, message)
