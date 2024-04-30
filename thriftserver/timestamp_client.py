import thriftpy2 as thriftpy
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException
from datetime import datetime

timestamp_thrift = thriftpy.load("thriftserver/timestamp.thrift", module_name="timestamp_thrift")
Timestamp = timestamp_thrift.TimestampService


def get_timestamp():
    try:
        client = make_client(Timestamp, '127.0.0.1', 10000)
        timestamp = client.getTimestamp()
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except TException as tx:
        print(f"Exception: {tx}")


if __name__ == "__main__":
    get_timestamp()
