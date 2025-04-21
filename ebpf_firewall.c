#include <uapi/linux/if_ether.h>
#include <uapi/linux/ip.h>
#include <bcc/proto.h>
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

#define ETH_P_IP 0x0800
#define MAX_RULES 1024

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32);
    __type(value, __u8);
    __uint(max_entries, MAX_RULES);
} rules_map SEC(".maps");

struct packet_info {
    __u32 src_ip;
    __u8 protocol;
};

struct {
    __uint(type, BPF_MAP_TYPE_PERF_EVENT_ARRAY);
    __uint(key_size, sizeof(__u32));
    __uint(value_size, sizeof(__u32));
} packet_metadata SEC(".maps");

SEC("xdp")
int xdp_firewall(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if (data + sizeof(*eth) > data_end)
        return XDP_PASS;

    if (bpf_ntohs(eth->h_proto) != ETH_P_IP)
        return XDP_PASS;

    struct iphdr *ip = data + sizeof(*eth);
    if ((void *)ip + sizeof(*ip) > data_end)
        return XDP_PASS;

    struct packet_info pkt = {
        .src_ip = ip->saddr,
        .protocol = ip->protocol,
    };

    bpf_perf_event_output(ctx, &packet_metadata, BPF_F_CURRENT_CPU, &pkt, sizeof(pkt));

    __u8 *action = bpf_map_lookup_elem(&rules_map, &ip->saddr);
    if (action && *action == 1)
        return XDP_DROP;

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";