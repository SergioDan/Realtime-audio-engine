import socket

def create_udp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def send_udp(sock, target_ip, target_port, data):
    sock.sendto(data, (target_ip, target_port))

def receive_udp(sock, buffer_size=1024):
    data, addr = sock.recvfrom(buffer_size)
    return data, addr
