from celery.decorators import task
from celery.utils.log import get_task_logger
from monitor.models import StoreToken
from django.conf import settings
import requests
import json
from django.utils import timezone
from celery.exceptions import MaxRetriesExceededError
from monitor.custome_exceptions import TokenInvalidError, TokenExpireError


logger = get_task_logger(__name__)
@task
def check_status():
    pass
