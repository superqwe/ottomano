#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys

# from logging_redirect import DualStream
#
# print_logger = logging.getLogger('print_logger')
# sys.stdout = DualStream(print_logger, logging.INFO)
# sys.stderr = DualStream(print_logger, logging.ERROR)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ottomano.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
