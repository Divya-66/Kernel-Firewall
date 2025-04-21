from bcc import BPF
import socket
import threading
import os

SOCKET_PATH = "/tmp/flask_socket"

def send_packet_data(src_ip, protocol):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    msg = f"{src_ip},{protocol}".encode()
    try:
        sock.sendto(msg, SOCKET_PATH)
    except Exception as e:
        print(f"Socket error: {e}")
    finally:
        sock.close()

def main():
    # Load eBPF program
    bpf = BPF(src_file="ebpf_firewall.c")

    # Attach to interface
    interface = "enx76fb796c9305"
    fn = bpf.load_func("xdp_firewall", BPF.XDP)
    bpf.attach_xdp(interface, fn, 0)

    # Initialize rules
    rules_map = bpf.get_table("rules_map")
    test_ip = int.from_bytes(b"\xc0\xa8\xdc\x32", "big")  # 192.168.220.50
    rules_map[test_ip] = 1

    # Read perf events
    def handle_packet(cpu, data, size):
        pkt = bpf["packet_metadata"].event(data)
        src_ip = f"{(pkt.src_ip >> 24) & 0xff}.{(pkt.src_ip >> 16) & 0xff}.{(pkt.src_ip >> 8) & 0xff}.{pkt.src_ip & 0xff}"
        print(f"Packet: src_ip={src_ip}, protocol={pkt.protocol}")  # Debug
        send_packet_data(src_ip, pkt.protocol)

    bpf["packet_metadata"].open_perf_buffer(handle_packet)

    print("Listening for packets...")
    try:
        while True:
            bpf.perf_buffer_poll()
    except KeyboardInterrupt:
        pass
    finally:
        bpf.remove_xdp(interface)

if __name__ == "__main__":
    main()