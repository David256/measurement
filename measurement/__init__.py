# -*- coding: utf-8 -*-

"""
Este módulo de Python permite procesar datos de medición de energía eléctrica.

Para esto define la clase :class:`measurement.measurement.Measurement` que
hace uso de otras clases como son
:class:`measurement.record.MeasurementRecord`, para el procesamiento de los
registros, :class:`measurement.data.MeasurementData` para el procesamiento de
los datos de los registros, :class:`measurement.variable.Variable` para
tener un control de las variables de la cabecera de datos y el módulo
:mod:`measurement.errors` con clases que manejan diferentes tipos de
excepciones.
"""

__version__ = '1.0.0'
