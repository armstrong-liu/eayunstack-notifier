from oslo.config import cfg
import oslo.messaging


DEFAULT_URL = "__default__"
TRANSPORTS = {}

_ALIASES = {
    'ceilometer.openstack.common.rpc.impl_kombu': 'rabbit',
    'ceilometer.openstack.common.rpc.impl_qpid': 'qpid',
    'ceilometer.openstack.common.rpc.impl_zmq': 'zmq',
}


def setup():
    oslo.messaging.set_transport_defaults('eayunstack_notifier')


def get_transport(url=None, optional=False, cache=True):
    """Initialise the oslo.messaging layer."""
    global TRANSPORTS, DEFAULT_URL
    cache_key = url or DEFAULT_URL
    transport = TRANSPORTS.get(cache_key)
    if not transport or not cache:
        try:
            transport = oslo.messaging.get_transport(cfg.CONF, url,
                                                     aliases=_ALIASES)
        except oslo.messaging.InvalidTransportURL as e:
            if not optional or e.url:
                # NOTE(sileht): oslo.messaging is configured but unloadable
                # so reraise the exception
                raise
            return None
        else:
            if cache:
                TRANSPORTS[cache_key] = transport
    return transport


def get_notification_listener(transport, targets, endpoints,
                              allow_requeue=True):
    """Return a configured oslo.messaging notification listener."""
    return oslo.messaging.get_notification_listener(
        transport, targets, endpoints, executor='eventlet',
        allow_requeue=allow_requeue)


def convert_to_old_notification_format(priority, ctxt, publisher_id,
                                       event_type, payload, metadata):
    notification = {'priority': priority,
                    'payload': payload,
                    'event_type': event_type,
                    'publisher_id': publisher_id}
    notification.update(metadata)
    for k in ctxt:
        notification['_context_' + k] = ctxt[k]
    return notification
