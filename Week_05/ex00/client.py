import socket
import time


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def get(self, key):
        request = "get {}\n".format(key)
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(request.encode("utf-8"))
                data = sock.recv(1024).decode("utf-8")
                # print(data[0:5] + "~~~")
                if "error" in data:
                    raise ClientError
                response = data.split("\n")
                metric_dict = {}
                for metric in response:
                    mtr_args = metric.split(" ")
                    if len(mtr_args) == 3:
                        metric_name, metric_value, metric_time = mtr_args[0], float(mtr_args[1]), int(mtr_args[2])
                        if metric_name not in metric_dict:
                            metric_dict[metric_name] = [(metric_time, metric_value)]
                        else:
                            metric_dict[metric_name].append((metric_time, metric_value))
                for _, value in metric_dict.items():
                    value.sort(key=lambda x: x[0])
                return metric_dict
            except socket.error:
                print("Socket error {}".format(socket.error.strerror))

    def put(self, key, value, timestamp=None):
        request = "put {} {} {}\n".format(key, value, timestamp or int(time.time()))
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(request.encode("utf-8"))
                data = sock.recv(1024).decode("utf-8")
                if "error" in data:
                    raise ClientError
            except socket.error:
                print("Socket error {}".format(socket.error.strerror))


class ClientError(Exception):
    pass
