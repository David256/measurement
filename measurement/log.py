import os
import logging

dev_mode = os.environ.get('MEASUREMENT_ENV', 'production') == 'development'

logger = logging.getLogger('Measurement')

logger.setLevel(
    logging.DEBUG if dev_mode else logging.CRITICAL,
)
