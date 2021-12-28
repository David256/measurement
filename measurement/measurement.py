# -*- coding: utf-8 -*-

import os

from .record import MeasurementRecord
from .data import MeasurementData
from .errors import MeasurementFileNotFoundError
from .errors import MeasurementRecordError
from .errors import MeasurementUnhandledError
from .errors import MeasurementDestinationNotFoundError
from .log import logger

import xlsxwriter


class Measurement(object):
    """
    Esta clase procesa datos de medición de energía elétrica.

    Al contruirse se solicita información del archivo fuente y la ruta destino,
    además, se proporciona el método ``save`` para guardar los datos procesados.
    """
    def __init__(self, source_path: str, destination_path: str) -> None:
        """
        Argumentos:
            source_path (str): La ruta al archivo fuente.
            destination_path (str): La ruta destino.
        """
        object.__init__(self)
        self.source_path = source_path
        self.destination_path = destination_path
        self.records: list[MeasurementRecord] = []
        if not os.path.exists(self.source_path):
            raise MeasurementFileNotFoundError(self.source_path)
        if not os.path.exists(os.path.dirname(self.destination_path)):
            raise MeasurementDestinationNotFoundError(self.destination_path)

        # Open the file and read
        file = open(self.source_path, 'r')
        line = file.readline()
        count = 0

        while line != '':
            count += 1
            if MeasurementRecord.is_header(line):
                logger.debug('Read header line: %s', line)
                record = MeasurementRecord(line)

                # Now read data to current record
                line = file.readline()
                while line != '':
                    if (
                       MeasurementData.is_data(line)
                       and not MeasurementRecord.is_header(line)
                       ):
                        count += 1
                        record << line
                        # Read next line
                        line = file.readline()
                    else:
                        # Stop reading data
                        self.records.append(record)
                        break
            elif line.startswith(chr(0x03)):
                # End-of-text
                file.close()
                break
            else:
                file.close()
                logger.warning('Error in line %d', count)
                raise MeasurementRecordError(line.strip())
        file.close()

    def save(self) -> str:
        """
        Guarda el archivo procesado en la ruta configurada.

        Retorno:
            str: Retorna el valor de ``filename`` generado.
        """
        date = self.records[0].date
        date_str = date.strftime('%y%m%d')
        filename = f'{self.destination_path}{date_str}.xls'
        try:
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
        except xlsxwriter.exceptions.XlsxFileError as e:  # type: ignore
            raise MeasurementUnhandledError(e)

        # Read each record
        counter = 1
        row = 0
        added_header = False
        for record in self.records:
            # Reset the col value
            col = 0

            # If the header has not been added yet, then:
            if not added_header:
                worksheet.write(row, col, 'No')
                col += 1
                worksheet.write(row, col, 'Fecha')
                for variable in record.variables:
                    col += 1
                    worksheet.write(row, col, f'Cabezote {variable.value}')

                # Next state
                added_header = True
                col = 0

            # Get the current date
            current_date = record.date
            # Read all data for current record
            for data in record.data:
                row += 1
                # Write the index and the date
                worksheet.write(row, col, counter)
                col += 1
                worksheet.write(row, col,
                                current_date.strftime('%Y-%m-%d %H:%M:%S'))

                for cell in data:
                    col += 1
                    worksheet.write(row, col, f'{cell:.3f}')
                col = 0

                # Update the next date
                current_date += record.sample
                # Increase the counter
                counter += 1
        # Close book
        workbook.close()
        return filename
