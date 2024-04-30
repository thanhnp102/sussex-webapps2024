import thriftpy2 as thriftpy
from thriftpy2.rpc import make_server
from datetime import datetime

timestamp_thrift = thriftpy.load("thriftserver/timestamp.thrift", module_name="timestamp_thrift")
Timestamp = timestamp_thrift.TimestampService


class TimestampHandler:
    def getTimestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_thrift_server():
    handler = TimestampHandler()
    server = make_server(Timestamp, handler, '127.0.0.1', 10000)
    server.serve()
