#!/usr/bin/env python
# coding=utf-8


import requests
import logging
import eventlet
import oslo.messaging
from openstack_notifier import messaging
from openstack_notifier.emit import ApiHandler
from openstack_notifier.common.log import logger
from openstack_notifier import event as event_converter
from ceilometer.openstack.common import service as os_service


eventlet.monkey_patch()

# logger.setLevel(logging.INFO)


class NotificationHandler(object):
    def __init__(self):
        super(NotificationHandler, self).__init__()
        self.event_converter = event_converter.setup_events()
        self.launcher = os_service.ProcessLauncher()

    def info(self, ctxt, publisher_id, event_type, payload, metadata):

        """Convert message to Eayunstack Notifier Event.

        :param ctxt: oslo.messaging context
        :param publisher_id: publisher of the notification
        :param event_type: type of notification
        :param payload: notification payload
        :param metadata: metadata about the notification
        """

        notification = messaging.convert_to_old_notification_format(
            'info', ctxt, publisher_id, event_type, payload, metadata)
        process_return = self.process_notification(notification)
        if process_return:
            return oslo.messaging.NotificationResult.HANDLED
        else:
            return oslo.messaging.NotificationResult.REQUEUE

    def error(self, ctxt, publisher_id, event_type, payload, metadata):

        """Convert message to Eayunstack Notifier Event.

        :param ctxt: oslo.messaging context
        :param publisher_id: publisher of the notification
        :param event_type: type of notification
        :param payload: notification payload
        :param metadata: metadata about the notification
        """

        notification = messaging.convert_to_old_notification_format(
            'error', ctxt, publisher_id, event_type, payload, metadata)
        process_return = self.process_notification(notification)
        if process_return:
            return oslo.messaging.NotificationResult.HANDLED
        else:
            return oslo.messaging.NotificationResult.REQUEUE

    def process_notification(self, notification):
        event = self.event_converter.to_event(notification)

        if event is not None:
            logger.info("Time to emit event to cloud api: %s" % event)
            try:
                response = ApiHandler.call_api(event)
            except requests.ConnectionError as e:
                logger.error("The error from api: %s" % e)
                return False
            except Exception as err:
                logger.error("The error from api: %s" % err)
                return False
            try:
                data = response.json()
                if data['status'] == '000000':
                    logger.info("Success to emit event: %s to cloud api.The "
                                "response code and msg are: %s, %s." %
                                (event, data['status'], data['message']))
                    return True
                else:
                    logger.error("Failed to emit event: %s to cloud api. The "
                                 "response code and msg are: %s, %s." %
                                 (event, data['status'], data['message']))
                    return False
            except Exception as err:
                logger.info("The response error is: %s" % err)
                return False
        return True
