#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from measurement import measurement

dev_mode = os.environ.get('MEASUREMENT_ENV', 'production') == 'development'


def main():
    if dev_mode:
        source_path = '../dataIEC62056-21.txt'
        destination_path = '../processed'
    else:
        source_path = input('Archivo fuente: ')
        destination_path = input('Archivo destino: ')

    # Read data
    m = measurement.Measurement(source_path, destination_path)

    # Save processed data
    m.save()


if __name__ == '__main__':
    main()
