from __future__ import absolute_import, unicode_literals

# Import Celery app
from .celery import app as celery_app

__all__ = ('celery_app',)