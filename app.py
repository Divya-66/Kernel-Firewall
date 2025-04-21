from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import json
import os
import time
import threading
import stat
from collections import Counter
import io
import requests

app = Flask(__name__)
socketio = SocketIO(app)

BASE_DIR = "/home/mint/Desktop/firewall-project/data"
PACKETS_FILE = os.path.join(BASE_DIR, "packets.json")
RULES_FILE = os.path.join(BASE_DIR, "rules.json")
GEO_API_KEY = "610f720a356f4ad3ace4d4bc941bca24"  # Your ipgeolocation.io key

# Track stats
stats = {
    "total_packets": 0,
    "blocked_packets": 0,
    "top_ips": Counter(),
    "packet_rate": [0] * 60,
    "ip_rates": {}  # Track packets/sec per IP
}
last_rate_update = time.time()
packet_count = 0
geo_cache = {}  # Cache IP -> country

def get_geo(ip):
    if ip in geo_cache:
        print(f"Geo cache hit for {ip}: {geo_cache[ip]}")
        return geo_cache[ip]
    for attempt in range(2):
        try:
            print(f"Fetching geo for {ip}, attempt {attempt + 1}")
            response = requests.get(
                f"https://api.ipgeolocation.io/ipgeo?apiKey={GEO_API_KEY}&ip={ip}",
                timeout=3
            )
            response.raise_for_status()
            data = response.json()
            country = data.get("country_name") or "Unknown"
            geo_cache[ip] = country
            print(f"Geo success for {ip}: {country}")
            return country
        except Exception as e:
            print(f"Geo error for {ip}, attempt {attempt + 1}: {e}")
            time.sleep(0.5)
    geo_cache[ip] = "Unknown"
    print(f"Geo fallback for {ip}: Unknown")
    return "Unknown"

def read_packets():
    global last_rate_update, packet_count
    last_mtime = 0
    protocol_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
    blocked_packet_cache = []
    ip_counts = Counter()
    last_ip_rate_update = time.time()
    while True:
        if not os.path.exists(PACKETS_FILE):
            print(f"Packet file missing: {PACKETS_FILE}")
            time.sleep(0.1)
            continue
        try:
            mtime = os.path.getmtime(PACKETS_FILE)
            if mtime > last_mtime:
                with open(PACKETS_FILE, "r") as f:
                    packets = json.load(f)
                with open(RULES_FILE, "r") as f:
                    rules = json.load(f)
                blocked_ips = [r["ip"] for r in rules if r["action"] == "block"]
                recent_packets = packets[-10:]
                for pkt in recent_packets:
                    country = get_geo(pkt["src_ip"])
                    packet = {
                        'src_ip': pkt["src_ip"],
                        'protocol': protocol_map.get(int(pkt["protocol"]), str(pkt["protocol"])),
                        'blocked': pkt.get("blocked", pkt["src_ip"] in blocked_ips),
                        'timestamp': pkt["timestamp"],
                        'country': country  # Explicitly set
                    }
                    print(f"Emitting packet: {packet}")
                    stats["total_packets"] += 1
                    stats["top_ips"].update([pkt["src_ip"]])
                    packet_count += 1
                    ip_counts[pkt["src_ip"]] += 1
                    if packet["blocked"]:
                        stats["blocked_packets"] += 1
                        blocked_packet_cache.append(packet)
                        socketio.emit('blocked_alert', {'ip': pkt["src_ip"]})
                    socketio.emit('new_packet', packet)
                blocked_packet_cache = sorted(
                    list({p["src_ip"]: p for p in blocked_packet_cache}.values()),
                    key=lambda x: x["timestamp"],
                    reverse=True
                )[:10]
                socketio.emit('blocked_packets', blocked_packet_cache)
                print(f"Blocked packets emitted: {[p['src_ip'] + ':' + p['country'] for p in blocked_packet_cache]}")
                current_time = time.time()
                if current_time - last_rate_update >= 1:
                    stats["packet_rate"].pop(0)
                    stats["packet_rate"].append(packet_count)
                    packet_count = 0
                    last_rate_update = current_time
                if current_time - last_ip_rate_update >= 1:
                    for ip, count in ip_counts.items():
                        stats["ip_rates"][ip] = count
                        if count > 100:
                            socketio.emit('rate_alert', {'ip': ip, 'rate': count})
                    ip_counts.clear()
                    last_ip_rate_update = current_time
                socketio.emit('stats_update', {
                    "total_packets": stats["total_packets"],
                    "blocked_packets": stats["blocked_packets"],
                    "top_ips": stats["top_ips"].most_common(5),
                    "packet_rate": stats["packet_rate"]
                })
                last_mtime = mtime
                print(f"Emitted {len(recent_packets)} packets, {len(blocked_packet_cache)} blocked")
        except Exception as e:
            print(f"Packet file error: {e}")
        time.sleep(0.1)

def get_rules():
    for _ in range(3):
        try:
            if os.path.exists(RULES_FILE):
                with open(RULES_FILE, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Get rules error: {e}")
            time.sleep(0.1)
    return []

def update_rule(cmd, ip, action):
    for _ in range(3):
        try:
            if os.path.exists(RULES_FILE):
                perms = os.stat(RULES_FILE).st_mode
                if not (perms & stat.S_IWUSR and perms & stat.S_IWGRP and perms & stat.S_IWOTH):
                    os.chmod(RULES_FILE, 0o666)
                    print(f"Fixed permissions on {RULES_FILE}")
            rules = get_rules()
            if cmd == "add":
                if not any(r["ip"] == ip for r in rules):
                    rules.append({"ip": ip, "action": action})
            elif cmd == "remove":
                rules = [r for r in rules if r["ip"] != ip]
            with open(RULES_FILE + ".tmp", "w") as f:
                json.dump(rules, f)
            os.rename(RULES_FILE + ".tmp", RULES_FILE)
            os.chmod(RULES_FILE, 0o666)
            print(f"Rule updated: {cmd} {ip} {action}")
            socketio.emit('rule_alert', {'cmd': cmd, 'ip': ip, 'action': action})
            return True
        except Exception as e:
            print(f"Rule file error: {e}")
            time.sleep(0.1)
    return False

@app.route('/')
def index():
    rules = get_rules()
    return render_template('index.html', rules=rules)

@app.route('/add_rule', methods=['POST'])
def add_rule():
    ip = request.form['ip']
    action = request.form['action']
    if update_rule("add", ip, action):
        return jsonify({'status': 'success', 'ip': ip, 'action': action})
    return jsonify({'status': 'error', 'message': 'Failed to add rule'})

@app.route('/remove_rule/<ip>', methods=['POST'])
def remove_rule(ip):
    if update_rule("remove", ip, "block"):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Failed to remove rule'})

@app.route('/get_rules', methods=['GET'])
def get_rules_route():
    rules = get_rules()
    return jsonify(rules)

@app.route('/export_packets', methods=['GET'])
def export_packets():
    try:
        with open(PACKETS_FILE, "r") as f:
            packets = json.load(f)
        csv_data = io.StringIO()
        csv_data.write("src_ip,protocol,timestamp,blocked,country\n")
        for pkt in packets:
            country = get_geo(pkt["src_ip"])
            csv_data.write(f"{pkt['src_ip']},{pkt['protocol']},{pkt['timestamp']},{pkt.get('blocked', False)},{country}\n")
        csv_data.seek(0)
        return send_file(
            io.BytesIO(csv_data.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='packets.csv'
        )
    except Exception as e:
        print(f"Export error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to export packets'})

@socketio.on('connect')
def handle_connect():
    print("SocketIO client connected")
    threading.Thread(target=read_packets, daemon=True).start()

@socketio.on('disconnect')
def handle_disconnect():
    print("SocketIO client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)