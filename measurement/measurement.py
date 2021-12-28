# -*- coding: utf-8 -*-

import os

from .record import MeasurementRecord
from .data import MeasurementData
from .errors import MeasurementFileNotFoundError, MeasurementRecordError
from .errors import MeasurementDestinationNotFoundError


class Measurement(object):
    def __init__(self, source_path: str, destination_path: str) -> None:
        object.__init__(self)
        self.records: list[MeasurementRecord] = []
        if not os.path.exists(source_path):
            raise MeasurementFileNotFoundError(source_path)

        # Open the file and read
        file = open(source_path, 'r')
        line = file.readline()
        while line != '':
            if MeasurementRecord.is_header(line):
                record = MeasurementRecord(line)

                # Now read data to current record
                line = file.readline()
                while line != '':
                    if MeasurementData.is_data(line):
                        record << line
                    else:
                        # Stop reading data
                        self.records.append(record)
                        break
            else:
                file.close()
                raise MeasurementRecordError(line)
        file.close()

    def save(self):
        pass
