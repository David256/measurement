# -*- coding: utf-8 -*-

import re
import datetime

from .data import MeasurementData
from .errors import MeasurementRecordError

date_fmt = r'\(1(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)\)'
sample_time_fmt = r'\((\d\d)\)\((\d\d)\)'
variable_size_fmt = r'\((\d+)\)'
var_fmt = r'\((\d*\.?\d+)\)\(([a-zA-Z]+)\)'

re_header = re.compile(
    fr'P\.01{date_fmt}{sample_time_fmt}'
    fr'{variable_size_fmt}{var_fmt}{var_fmt}{var_fmt}{var_fmt}'
)


class MeasurementRecord(object):
    def __init__(self, header_raw: str) -> None:
        super().__init__()
        self.header_raw = header_raw
        self.data: list[MeasurementData] = []
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
            raise MeasurementRecordError(header_raw)

    @staticmethod
    def is_header(header_raw: str):
        matched = re_header.search(header_raw)
        return matched is not None

    def __lshift__(self, data_raw):
        """
        Append new data to current record
        """
        if MeasurementData.is_data(data_raw):
            data = MeasurementData(data_raw)
            self.data.append(data)
        else:
            raise MeasurementRecordError(data_raw)
