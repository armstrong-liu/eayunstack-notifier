#
# Copyright 2012-2013 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack_notifier.config import CONF
import oslo
import logging
from openstack_notifier import messaging
from openstack_notifier.common.log import logger
from ceilometer.openstack.common import service as os_service
from openstack_notifier import endpoint

logger.setLevel(logging.INFO)

TRANSPORT_URL = None

HOSTS = CONF.get('default', 'rabbit_hosts')
RABBIT_USER = CONF.get('default', 'rabbit_userid')
RABBIT_PASSWD = CONF.get('default', 'rabbit_password')
TOPIC = CONF.get('default', 'notification_topics')


class NotificationService(os_service.Service):

    def start(self):
        super(NotificationService, self).start()
        endpoints = [endpoint.NotificationHandler()]
        targets = [oslo.messaging.Target(topic=TOPIC)]
        self.listeners = []
        logger.info("The rabbit broker hosts are : %s" % HOSTS)
        for url in HOSTS.split(','):
            TRANSPORT_URL = 'rabbit://%s:%s@%s/' % (RABBIT_USER,
                                                    RABBIT_PASSWD, url)
            transport = messaging.get_transport(url=TRANSPORT_URL)
            listener = messaging.get_notification_listener(
                transport, targets, endpoints)
            logger.info("The listener is: %s" % listener)
            logger.info('Starting up server')
            listener.start()
            self.listeners.append(listener)
            logger.info('Waiting for something')
        self.tg.add_timer(604800, lambda: None)

    def stop(self):
        map(lambda x: x.stop(), self.listeners)
        super(NotificationService, self).stop()
