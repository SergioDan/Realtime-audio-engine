import argparse
import time
import struct
from udp_stream import create_udp_socket, send_udp, receive_udp
from jitter_buffer import JitterBuffer

def sender(ip="127.0.0.1", port=5000):
    sock = create_udp_socket()
    seq = 0

    while True:
        payload = b"AUDIO_FRAME"
        packet = struct.pack("!I", seq) + payload  # 4 bytes sequence id
        send_udp(sock, ip, port, packet)
        print(f"Sent packet {seq}")
        seq += 1
        time.sleep(0.05)

def receiver(port=5000):
    sock = create_udp_socket()
    sock.bind(("0.0.0.0", port))
    jb = JitterBuffer()

    while True:
        data, addr = receive_udp(sock)
        seq = struct.unpack("!I", data[:4])[0]
        payload = data[4:]
        jb.push((seq, time.time(), payload))

        packet = jb.pop()
        if packet:
            print(f"Played packet {packet[0]} (payload={packet[2]})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["sender", "receiver"], required=True)
    args = parser.parse_args()

    if args.mode == "sender":
        sender()
    else:
        receiver()

if __name__ == "__main__":
    main()
