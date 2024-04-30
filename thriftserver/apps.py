from django.apps import AppConfig
import threading
import os


class ThriftserverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thriftserver'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from thriftserver.timestamp_server import run_thrift_server
            t = threading.Thread(target=run_thrift_server)
            print("starting thrift server...")
            t.start()
