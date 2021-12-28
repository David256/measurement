Electrical Energy Measurement Processing Library
================================================

Este paquete de Python contiene la librería ``measurement`` y sus tests.

Para el desarrollo se codificó y probó unicamente bajo la versión de **Python 3.9.2**,
y se utilizó la librería externa de xlsxwriter_.

Preparación
-----------

Puede ser instalada con el comando ``pip`` y el archivo de ``requirements.txt``.

.. code:: bash

    pip install -r requirements.txt

En el directorio `docs` se encuentra la documentación de la librería.

Pruebas
-------

Se recomienda el uso del framework pytest_ para ejecutar los tests en el
directorio ``tests`` con el comando:

.. code:: bash

    py.test

.. _xlsxwriter: https://xlsxwriter.readthedocs.io/
.. _pytest: https://docs.pytest.org/en/6.2.x/
