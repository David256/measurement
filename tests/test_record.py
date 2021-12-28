from measurement.record import MeasurementRecord

good_header = 'P.01(210430001500)(00)(15)(4)(1.9)(kWh)(3.9)(kVarh)(2.9)(kWh)(4.9)(kVarh)'

some_good_data = [
    '(0.116)(0.060)(0.000)(0.022)',
    '(0.078)(0.000)(0.000)(0.032)',
    '(0.088)(0.012)(0.000)(0.030)',
]



def test_read_good_header():
    assert MeasurementRecord.is_header(good_header)
    MeasurementRecord(header_raw=good_header)


def test_read_date():
    mrecord = MeasurementRecord(header_raw=good_header)
    # Test the date
    assert mrecord.date.year == 2021
    assert mrecord.date.month == 4
    assert mrecord.date.day == 3
    assert mrecord.date.hour == 0
    assert mrecord.date.minute == 15
    assert mrecord.date.second == 0


def test_read_sample_time():
    mrecord = MeasurementRecord(header_raw=good_header)
    # Test the sample time
    assert mrecord.sample.hour == 0
    assert mrecord.sample.minute == 15


def test_read_variables():
    mrecord = MeasurementRecord(header_raw=good_header)
    # Test the variable parsing
    assert mrecord.variable_size == 4

    assert mrecord.variables[0].value == 1.9
    assert mrecord.variables[0].unit_name == 'kWh'

    assert mrecord.variables[1].value == 3.9
    assert mrecord.variables[1].unit_name == 'kVarh'

    assert mrecord.variables[2].value == 2.9
    assert mrecord.variables[2].unit_name == 'kWh'

    assert mrecord.variables[3].value == 4.9
    assert mrecord.variables[3].unit_name == 'kVarh'


def test_read_data():
    mrecord = MeasurementRecord(header_raw=good_header)
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