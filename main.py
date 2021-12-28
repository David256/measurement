#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from measurement import measurement
from measurement.errors import MeasurementError, MeasurementUnhandledError

dev_mode = os.environ.get('MEASUREMENT_ENV', 'production') == 'development'


def print_result(success: bool, filename: str = None, e: Exception = None):
    print('Estado =>', success)
    if filename:
        print('Ruta =>', filename)
    if e:
        print('Error =>', e)


def main():
    if dev_mode:
        source_path = '../dataIEC62056-21.txt'
        destination_path = '../processed'
    else:
        source_path = input('Archivo fuente: ')
        destination_path = input('Archivo destino: ')

    try:
        # Read data
        m = measurement.Measurement(source_path, destination_path)

        # Save processed data
        filename = m.save()

        # Print results
        print_result(True, filename=filename)
    except MeasurementError as e:
        print_result(False, e=e)
    except Exception as e:
        print_result(False, e=MeasurementUnhandledError(e))


if __name__ == '__main__':
    main()
