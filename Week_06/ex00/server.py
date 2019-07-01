import asyncio


storage = {}


def put(command):
    if len(command) == 4:
        server_response = "ok\n\n"
        key, value, time = command[1], float(command[2]), int(command[3])
        if key in storage:
            old_data = storage[key]
            for idx, metric_values in enumerate(old_data):
                if metric_values[0] == time:
                    old_data.remove((metric_values[0], metric_values[1]))
                    break
            old_data.append((time, value))
            storage[key].sort(key=lambda x: x[0])
        else:
            storage[key] = [(time, value)]
        # print(storage)
        return server_response
    return "error\n\n"


def get(command):
    to_find = command[1][0:-1]
    if len(command) == 2:
        server_response = "ok\n"
        if to_find == "*":
            for key, value_list in storage.items():
                for params in value_list:
                    server_response += "{} {} {}\n".format(key, params[1], params[0])
        elif to_find in storage:
            for value in storage[to_find]:
                server_response += "{} {} {}\n".format(to_find, value[1], value[0])
        server_response += "\n"
        # print(server_response)
        return server_response
    return "error\n\n"


def process_data(data):
    command = data.split(' ')
    if command[0] == "get":
        return get(command)
    elif command[0] == "put":
        return put(command)
    return "error\nwrong command\n\n"


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
