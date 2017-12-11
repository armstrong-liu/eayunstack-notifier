#!/usr/bin/env python
# coding=utf-8

from eayunstack_notifier import notification
from ceilometer import service
from ceilometer.openstack.common import service as os_service


def main():
    service.prepare_service()
    launcher = os_service.ProcessLauncher()
    launcher.launch_service(
        notification.NotificationService(),
        workers=service.get_workers('notification'))
    launcher.wait()


if __name__ == "__main__":
    main()
