#!/usr/bin/env python
# coding=utf-8

import hmac
import json
import time
import hashlib
import logging
import requests
from eayunstack_notifier.common.log import logger
from eayunstack_notifier.config import CONF

logger.setLevel(logging.INFO)

CLOUD_API = CONF.get('api', 'api_address')
AK = CONF.get('api', 'access_key')
SK = CONF.get('api', 'secret_key')


class ApiHandler(object):
    '''Api client to call cloud api'''
    def __init__(self):
        pass

    @staticmethod
    def call_api(event):
        # RFC 1123 format
        current_time = time.localtime()
        xdate = time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        sign = hmac.new(SK, xdate,
                        hashlib.sha1).digest().encode('base64').rstrip()
        auth_pwd = (AK + ":" + sign).encode('base64').rstrip()
        headers = {'content-type': 'application/json',
                   'x-date': xdate, 'Authorization': auth_pwd}
        json_data = json.dumps(event)
        resp = requests.post(CLOUD_API, data=json_data, headers=headers)
        return resp
