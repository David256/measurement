# -*- coding: utf-8 -*-

import os

from .record import MeasurementRecord
from .data import MeasurementData
from .errors import MeasurementFileNotFoundError, MeasurementRecordError
from .errors import MeasurementDestinationNotFoundError
from .log import logger


class Measurement(object):
    def __init__(self, source_path: str, destination_path: str) -> None:
        object.__init__(self)
        self.records: list[MeasurementRecord] = []
        if not os.path.exists(source_path):
            raise MeasurementFileNotFoundError(source_path)

        # Open the file and read
        file = open(source_path, 'r')
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
                    if MeasurementData.is_data(line):
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
                raise MeasurementRecordError(line)
        file.close()

    def save(self):
        pass
