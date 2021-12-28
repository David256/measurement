# -*- coding: utf-8 -*-


class MeasurementError(Exception):
    """
    Esta excepción es lanzada cuando un error genérico ocurre.
    """
    def __init__(self, code: str, message: str) -> None:
        Exception.__init__(self, f'{code}: {message}')


class MeasurementFileNotFoundError(MeasurementError):
    """
    Esta excepción es lanzada cuando el archivo fuente no es encontrado.
    """
    code = 'EX001'

    def __init__(self, filename: str) -> None:
        message = f'No se encuentra el archivo fuente {filename}'
        MeasurementError.__init__(self, self.code, message)


class MeasurementDestinationNotFoundError(MeasurementError):
    """
    Esta excepción es lanzada cuando no se puede acceder a la ruta destino.
    """
    def __init__(self, destination_path: str) -> None:
        message = 'No se encuentra la ruta destino'
        MeasurementError.__init__(self, self.code, message)


class MeasurementRecordError(MeasurementError):
    """
    Esta excepción es lanzada cuando no se puede leer la información en el
    registro.
    """
    code = 'EX003'

    def __init__(self, record_raw: str) -> None:
        message = 'Error en la información del registro ' \
            f'{record_raw}'
        MeasurementError.__init__(self, self.code, message)


class MeasurementUnhandledError(MeasurementError):
    """
    Esta excepción es lanzada cuando un error de Python o del sistema operativo
    ocurre.
    """
    code = 'EX004'

    def __init__(self, e: Exception) -> None:
        message = f'Error generado por Python o SO el cual entrega: {e}'
        MeasurementError.__init__(self, self.code, message)
