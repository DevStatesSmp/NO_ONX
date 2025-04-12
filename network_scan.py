import socket

def port_scan(target_ip, port_range=range(1, 1025)):
    open_ports = []
    for port in port_range:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

open_ports = port_scan('192.168.1.1')
print(f"Open ports: {open_ports}")
