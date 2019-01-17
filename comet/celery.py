"""Celery init."""

from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comet.settings')

app = Celery('comet', broker='amqp://mercer:esogub40@localhost:5672/DESKTOP-VMIK0FP')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
