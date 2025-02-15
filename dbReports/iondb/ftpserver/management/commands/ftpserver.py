import sys
import os

from optparse import make_option

import pyftpdlib
from pyftpdlib import handlers
from pyftpdlib.servers import FTPServer

from django import get_version
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.daemonize import become_daemon
from iondb.ftpserver.authorizers import FTPAccountAuthorizer
from iondb.ftpserver import utils

import logging

logger = logging.getLogger("pyftpdlib")
logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    help = "Start FTP server"

    option_list = BaseCommand.option_list + (
        make_option(
            "--daemonize",
            action="store_true",
            dest="daemonize",
            help="become background service.",
        ),
        make_option(
            "--pidfile",
            action="store",
            dest="pidfile",
            help="filename to write process id (PID).",
        ),
        make_option(
            "--timeout",
            action="store",
            dest="timeout",
            type=int,
            help="timeout for remote client.",
        ),
        make_option(
            "--passive-ports",
            action="store",
            dest="passive-ports",
            help="Passive ports. eg. 12345,30000-50000",
        ),
        make_option(
            "--masquerade-address",
            action="store",
            dest="masquerade-address",
            help="masquerade address.",
        ),
        make_option(
            "--file-access-user",
            action="store",
            dest="file-access-user",
            help="user for access to file.",
        ),
        make_option(
            "--certfile", action="store", dest="certfile", help="TLS certificate file."
        ),
        make_option(
            "--keyfile", action="store", dest="keyfile", help="TLS private key file."
        ),
        make_option(
            "--sendfile", action="store_true", dest="sendfile", help="Use sendfile."
        ),
    )

    def make_server(
        self,
        server_class,
        handler_class,
        authorizer_class,
        host_port,
        file_access_user=None,
        **handler_options
    ):
        """Helper method for making a server"""
        return utils.make_server(
            server_class,
            handler_class,
            authorizer_class,
            host_port,
            file_access_user=file_access_user,
            **handler_options
        )

    def handle(self, *args, **options):
        # bind host and port
        host_port = options.get("host_port", None)
        if host_port:
            host, _port = host_port.split(":", 1)
            port = int(_port)
        else:
            host = utils.get_settings_value("FTPSERVER_HOST") or "127.0.0.1"
            port = utils.get_settings_value("FTPSERVER_PORT") or 21

        timeout = options.get("timeout") or utils.get_settings_value(
            "FTPSERVER_TIMEOUT"
        )

        # passive ports
        _passive_ports = options.get("passive-ports") or utils.get_settings_value(
            "FTPSERVER_PASSIVE_PORTS"
        )
        if _passive_ports:
            try:
                passive_ports = utils.parse_ports(_passive_ports)
            except (TypeError, ValueError):
                raise CommandError("Invalid passive ports: {}".format(_passive_ports))
        else:
            passive_ports = None

        # masquerade address
        masquerade_address = options.get(
            "masquerade-address"
        ) or utils.get_settings_value("FTPSERVER_MASQUERADE_ADDRESS")

        # file access user
        file_access_user = options.get("file-access-user") or utils.get_settings_value(
            "FTPSERVER_FILE_ACCESS_USER"
        )

        # certfile
        certfile = options.get("certfile") or utils.get_settings_value(
            "FTPSERVER_CERTFILE"
        )

        # keyfile
        keyfile = options.get("keyfile") or utils.get_settings_value(
            "FTPSERVER_KEYFILE"
        )

        # sendfile
        sendfile = options.get("sendfile") or utils.get_settings_value(
            "FTPSERVER_SENDFILE"
        )

        # daemonize
        daemonize = options.get("daemonize") or utils.get_settings_value(
            "FTPSERVER_DAEMONIZE"
        )
        if daemonize:
            daemonize_options = (
                utils.get_settings_value("FTPSERVER_DAEMONIZE_OPTIONS") or {}
            )
            become_daemon(**daemonize_options)

        # write pid to file
        pidfile = options.get("pidfile") or utils.get_settings_value(
            "FTPSERVER_PIDFILE"
        )
        if pidfile:
            with open(pidfile, "w") as f:
                f.write(str(os.getpid()))

        # select handler class
        if certfile or keyfile:
            if hasattr(handlers, "TLS_FTPHandler"):
                handler_class = (
                    utils.get_settings_value("FTPSERVER_TLSHANDLER")
                ) or handlers.TLS_FTPHandler
            else:
                # unsupported
                raise CommandError("Can't import OpenSSL. Please install pyOpenSSL.")
        else:
            handler_class = (
                utils.get_settings_value("FTPSERVER_HANDLER")
            ) or handlers.FTPHandler

        # setup server
        server = self.make_server(
            server_class=FTPServer,
            handler_class=handler_class,
            authorizer_class=FTPAccountAuthorizer,
            host_port=(host, port),
            file_access_user=file_access_user,
            timeout=timeout,
            passive_ports=passive_ports,
            masquerade_address=masquerade_address,
            certfile=certfile,
            keyfile=keyfile,
            sendfile=sendfile,
        )

        # start server
        sys.stdout.write(
            (
                "Django version {version_dj}, using settings '{settings}'\n"
                "pyftpdlib version {version_ftp}\n"
                "Quit the server with {quit_command}.\n"
            ).format(
                version_dj=get_version(),
                version_ftp=pyftpdlib.__ver__,
                settings=settings.SETTINGS_MODULE,
                quit_command="CONTROL-C",
            )
        )
        server.serve_forever()
