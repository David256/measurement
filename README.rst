Electrical Energy Measurement Processing Library
================================================

Este paquete de Python contiene la librería ``measurement`` y sus tests.

Para el desarrollo se codificó y probó unicamente bajo la versión de **Python 3.9.2**,
en una máquina Debian 11, y se utilizó la librería externa de xlsxwriter_ para
crear archivos XLS.

Preparación
-----------

Las librerías externas utilizadas en este proyecto pueden ser instalada con el
comando ``pip`` y el archivo de ``requirements.txt``.

.. code:: bash

    pip install -r requirements.txt

En el directorio `docs` se encuentra la documentación de la librería.

Pruebas
-------

Se recomienda el uso del framework pytest_ para ejecutar los tests en el
directorio ``tests`` con el comando:

.. code:: bash

    py.test

Ejecución
---------

Se puede ejecutar el archivo ``main.py``, el cual solicitará datos al usuario
de forma interactiva para finalmente dar el resultado de la ejecución.

.. code:: bash

    python main.py
    >>> Archivo fuente: /path/to/source.txt
    >>> Archivo destino: /path/to/destination/file

    Estado => True
    Ruta => /path/to/destination/fileYYMMDD.xls

.. _xlsxwriter: https://xlsxwriter.readthedocs.io/
.. _pytest: https://docs.pytest.org/en/6.2.x/
