import psutil
import shlex
import logging
from contextlib import contextmanager
import os

logger = logging.getLogger(__name__)


class NginXServer(object):
    # def __init__(self, config_file, location) -> None:
    #     self.nginx_location = location
    #     self.config_file = config_file

    #     self.process = None

    def __init__(self, config, location) -> None:
        self.nginx_location = location
        config.write_to("/tmp/generated_config.cfg")
        self.config_file = "/tmp/generated_config.cfg"

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


class NginxConfig(object):
    def __init__(
        self,
        processes=1,
        daemon=False,
        error_log="nginx_error.log",
        worker_connections=1024,
        port=8090,
        location="/var/www/html",
    ) -> None:
        self.body = """
        
        worker_processes {};
        daemon {};
        error_log {};
        events {{
            worker_connections {};
        }}

        http {{
            server {{
                listen {};

                location / {{
                    root {};
                }}
            }}
        }}
        """.format(
            processes,
            "on" if daemon else "off",
            error_log,
            worker_connections,
            port,
            location,
        )

    def to_string(self):
        return self.body

    def write_to(self, filename):
        f = open(filename, "w")
        f.write(self.body)
        f.close()
