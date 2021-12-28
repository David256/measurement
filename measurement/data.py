# -*- coding: utf-8 -*-

import re

col_fmt = r'\(\d*\.?\d+\)'

re_data = re.compile(
    f'{col_fmt}{col_fmt}{col_fmt}{col_fmt}',
)


class MeasurementData(object):
    def __init__(self, data_raw: str) -> None:
        object.__init__(self)
        self.data_raw = data_raw

    @staticmethod
    def is_data(data_raw: str) -> bool:
        matched = re_data.search(data_raw)
        return matched is not None
