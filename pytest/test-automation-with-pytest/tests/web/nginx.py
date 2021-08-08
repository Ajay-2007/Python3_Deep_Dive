import psutil
import shlex
import logging
from contextlib import contextmanager
import os

logger = logging.getLogger(__name__)


class NginXServer(object):
    def __init__(self, config_file, location) -> None:
        self.nginx_location = location
        self.config_file = config_file

        self.process = None

    def start(self):
        command = "{} -p . -c {}".format(self.nginx_location, self.config_file)
        logger.info("Starting Nginx Server {}".format(command))
        self.process = psutil.Popen(shlex.split(command), cwd=os.getcwd())

    def stop(self):
        logger.info("Stopping Nginx Server")
        self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except psutil.TimeoutExpired:
            logger.error("Failed to stop server in time, killing")
            self.process.kill()
            raise
        finally:
            self.process = None


@contextmanager
def nginxServer(config_file, location="/usr/sbin/nginx"):
    server = NginXServer(config_file, location)
    try:
        server.start()
        yield server
    finally:
        server.stop()
