import pytest

from measurement.record import MeasurementRecord
from measurement.errors import MeasurementRecordError

good_header = 'P.01(1210430001500)(00)(15)(4)(1.9)(kWh)(3.9)(kVArh)(2.9)(kWh)(4.9)(kVArh)'
bad_header = 'P.01(...)(00)(15)(4)(xx)(kWh)(xx)(kVArh)(xx)(kWh)(xx)(kVArh)'

some_good_data = [
    '(0.116)(0.060)(0.000)(0.022)',
    '(0.078)(0.000)(0.000)(0.032)',
    '(0.088)(0.012)(0.000)(0.030)',
]

some_bad_data = [
    '(0.07 )(0.)(0-000)(0.032)',
]

@pytest.fixture
def mrecord():
    return MeasurementRecord(header_raw=good_header)


def test_check_header():
    assert MeasurementRecord.is_header(good_header)
    assert not MeasurementRecord.is_header(bad_header)


def test_read_bad_header():
    with pytest.raises(
                       MeasurementRecordError,
                       match='EX003: Error en la información del registro'):
        MeasurementRecord(header_raw=bad_header)


def test_read_bad_data(mrecord: MeasurementRecord):
    with pytest.raises(
                       MeasurementRecordError,
                       match='EX003: Error en la información del registro'):
        for data in some_bad_data:
            mrecord << data


def test_read_date(mrecord: MeasurementRecord):
    # Test the date
    assert mrecord.date.year == 2021
    assert mrecord.date.month == 4
    assert mrecord.date.day == 30
    assert mrecord.date.hour == 0
    assert mrecord.date.minute == 15
    assert mrecord.date.second == 0


def test_read_sample_time(mrecord: MeasurementRecord):
    # Test the sample time
    assert mrecord.sample.seconds == 15 * 60


def test_read_variables(mrecord: MeasurementRecord):
    # Test the variable parsing
    assert mrecord.variable_size == 4

    assert mrecord.variables[0].value == 1.9
    assert mrecord.variables[0].unit_name == 'kWh'

    assert mrecord.variables[1].value == 3.9
    assert mrecord.variables[1].unit_name == 'kVArh'

    assert mrecord.variables[2].value == 2.9
    assert mrecord.variables[2].unit_name == 'kWh'

    assert mrecord.variables[3].value == 4.9
    assert mrecord.variables[3].unit_name == 'kVArh'


def test_read_data(mrecord: MeasurementRecord):
    for data in some_good_data:
        mrecord << data

    # Check
    assert len(mrecord.data) == len(some_good_data)

    assert mrecord.data[0][0] == 0.116
    assert mrecord.data[0][1] == 0.060
    assert mrecord.data[0][2] == 0.000
    assert mrecord.data[0][3] == 0.022

    assert mrecord.data[1][0] == 0.078
    assert mrecord.data[1][1] == 0.000
    assert mrecord.data[1][2] == 0.000
    assert mrecord.data[1][3] == 0.032

    assert mrecord.data[2][0] == 0.088
    assert mrecord.data[2][1] == 0.012
    assert mrecord.data[2][2] == 0.000
    assert mrecord.data[2][3] == 0.030