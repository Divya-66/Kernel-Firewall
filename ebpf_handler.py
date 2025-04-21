from bcc import BPF
import json
import os
import netifaces
import ctypes as ct
import time
import pwd

# Absolute path for mint user
BASE_DIR = "/home/mint/Desktop/firewall-project/data"
os.makedirs(BASE_DIR, exist_ok=True)
PACKETS_FILE = os.path.join(BASE_DIR, "packets.json")
RULES_FILE = os.path.join(BASE_DIR, "rules.json")

# eBPF program
BPF_CODE = """
#include <uapi/linux/if_ether.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/in.h>
#include <linux/bpf.h>

#define ETH_P_IP 0x0800
#define MAX_RULES 1024

BPF_HASH(rules_map, u32, u8, MAX_RULES);
BPF_PERF_OUTPUT(packet_metadata);

struct packet_info {
    u32 src_ip;
    u8 protocol;
};

int xdp_firewall(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if (data + sizeof(*eth) > data_end)
        return XDP_PASS;

    if (ntohs(eth->h_proto) != ETH_P_IP)
        return XDP_PASS;

    struct iphdr *ip = data + sizeof(*eth);
    if ((void *)ip + sizeof(*ip) > data_end)
        return XDP_PASS;

    u8 *action = rules_map.lookup(&ip->saddr);
    if (action && *action == 1)
        return XDP_DROP;

    struct packet_info pkt = {
        .src_ip = ip->saddr,
        .protocol = ip->protocol,
    };

    packet_metadata.perf_submit(ctx, &pkt, sizeof(pkt));
    return XDP_PASS;
}
"""

def write_packet(src_ip, protocol):
    try:
        user_id = pwd.getpwnam("mint").pw_uid
        os.seteuid(user_id)
        packet = {"src_ip": src_ip, "protocol": protocol, "timestamp": time.time()}
        packets = []
        if os.path.exists(PACKETS_FILE):
            try:
                with open(PACKETS_FILE, "r") as f:
                    packets = json.load(f)
            except Exception as e:
                print(f"Packet read error: {e}")
        packets.append(packet)
        packets = packets[-100:]  # Keep last 100 packets
        with open(PACKETS_FILE, "w") as f:
            json.dump(packets, f)
        os.chmod(PACKETS_FILE, 0o666)
        print(f"Wrote packet to {PACKETS_FILE}")
    except Exception as e:
        print(f"Packet write error: {e}")
    finally:
        os.seteuid(0)

def update_rules(bpf):
    rules_map = bpf.get_table("rules_map")
    last_mtime = 0
    while True:
        if os.path.exists(RULES_FILE):
            mtime = os.path.getmtime(RULES_FILE)
            if mtime != last_mtime:
                try:
                    with open(RULES_FILE, "r") as f:
                        rules = json.load(f)
                    rules_map.clear()
                    for rule in rules:
                        ip_parts = rule["ip"].split('.')
                        ip_int = ct.c_uint32(
                            (int(ip_parts[0]) << 24) +
                            (int(ip_parts[1]) << 16) +
                            (int(ip_parts[2]) << 8) +
                            int(ip_parts[3])
                        )
                        rules_map[ip_int] = ct.c_uint8(1 if rule["action"] == "block" else 0)
                        print(f"Rule updated: {rule['ip']} -> {rule['action']}")
                    last_mtime = mtime
                except Exception as e:
                    print(f"Rule file error: {e}")
        time.sleep(1)

def get_active_interface():
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        if iface == "lo":
            continue
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs and addrs[netifaces.AF_LINK][0].get("addr"):
            return iface
    return None

def main():
    # Initialize files
    try:
        user_id = pwd.getpwnam("mint").pw_uid
        os.seteuid(user_id)
        for f in [PACKETS_FILE, RULES_FILE]:
            if os.path.exists(f):
                os.unlink(f)
            with open(f, "w") as fd:
                json.dump([], fd)
            os.chmod(f, 0o666)
            print(f"Initialized {f}")
    except Exception as e:
        print(f"File init error: {e}")
    finally:
        os.seteuid(0)

    # Find interface
    interface = "enx12f2d317950a"
    if interface not in netifaces.interfaces():
        print(f"Interface {interface} not found. Available interfaces: {netifaces.interfaces()}")
        interface = get_active_interface()
        if not interface:
            print("No active network interface found. Exiting.")
            return
        print(f"Using interface: {interface}")

    # Load eBPF program
    bpf = BPF(text=BPF_CODE)

    # Attach to interface
    try:
        fn = bpf.load_func("xdp_firewall", BPF.XDP)
        bpf.attach_xdp(interface, fn, 0)
    except Exception as e:
        print(f"Failed to attach XDP to {interface}: {e}")
        return

    # Initialize rules
    try:
        user_id = pwd.getpwnam("mint").pw_uid
        os.seteuid(user_id)
        rules_map = bpf.get_table("rules_map")
        test_ip = ct.c_uint32(int.from_bytes(b"\xc0\xa8\xdc\x32", "big"))  # 192.168.220.50
        rules_map[test_ip] = ct.c_uint8(1)
        with open(RULES_FILE, "w") as f:
            json.dump([{"ip": "192.168.220.50", "action": "block"}], f)
        os.chmod(RULES_FILE, 0o666)
        print(f"Initial rule: 192.168.220.50 -> block")
    except Exception as e:
        print(f"Rule init error: {e}")
    finally:
        os.seteuid(0)

    # Start rule updates
    import threading
    threading.Thread(target=update_rules, args=(bpf,), daemon=True).start()

    # Read perf events
    def handle_packet(cpu, data, size):
        pkt = bpf["packet_metadata"].event(data)
        src_ip = f"{(pkt.src_ip >> 24) & 0xff}.{(pkt.src_ip >> 16) & 0xff}.{(pkt.src_ip >> 8) & 0xff}.{pkt.src_ip & 0xff}"
        print(f"Packet: src_ip={src_ip}, protocol={pkt.protocol}")
        write_packet(src_ip, pkt.protocol)

    bpf["packet_metadata"].open_perf_buffer(handle_packet)

    print(f"Listening for packets on {interface}...")
    try:
        while True:
            bpf.perf_buffer_poll()
    except KeyboardInterrupt:
        pass
    finally:
        bpf.remove_xdp(interface)
        try:
            user_id = pwd.getpwnam("mint").pw_uid
            os.seteuid(user_id)
            for f in [PACKETS_FILE, RULES_FILE]:
                if os.path.exists(f):
                    os.unlink(f)
        except Exception as e:
            print(f"Cleanup error: {e}")
        finally:
            os.seteuid(0)

if __name__ == "__main__":
    main()