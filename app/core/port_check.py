import socket


def is_udp_port_available(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(("", port))
        return True
    except OSError:
        return False


def is_tcp_port_available(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
        return True
    except OSError:
        return False


def find_free_tcp_port(start_port: int, max_tries: int = 20) -> int:
    for offset in range(max_tries):
        port = start_port + offset
        if is_tcp_port_available(port):
            return port

    raise RuntimeError("No free TCP ports available.")