# eBPF Firewall Dashboard

A real-time network firewall dashboard built with **eBPF**, **Flask**, and **SocketIO** to monitor network traffic, visualize packet details, and automatically block malicious IPs based on threat intelligence.

This project captures packets at the kernel level, enriches them with geolocation (via ipgeolocation.io) and threat scores (via AbuseIPDB), and displays them in a responsive web interface with live updates, filtering, and export capabilities.

---

## 🚀 Features

| Feature             | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| Packet Capture      | Uses eBPF to capture IPv4 packets at the kernel level with low overhead |
| Geolocation         | Tags source IPs with country names using ipgeolocation.io               |
| Threat Intelligence | Scores IPs using AbuseIPDB, auto-blocks IPs with score > 50             |
| Real-Time Dashboard | Displays packets and stats live via SocketIO                            |
| Interactive UI      | Filter by IP/protocol/threat score; dark mode; export CSV               |
| Firewall Rules      | Add/remove block/allow rules, applied via eBPF                          |
| Animations & Alerts | Blocked packets highlighted with effects; toast alerts                  |

---

## 📁 Project Structure

```
firewall-project/
├── ebpf_handler.py        # eBPF packet capture and rule enforcement
├── app.py                # Flask backend with geolocation, threat scoring, and SocketIO
├── templates/
│   └── index.html        # Frontend dashboard with Bootstrap, Chart.js
├── static/
│   └── style.css         # Custom styles for dark mode, animations
├── data/
│   ├── packets.json      # Logs captured packets
│   └── rules.json        # Stores firewall rules
├── venv/                 # Python virtual environment
└── README.md             # Project documentation
```

---

## ✅ Prerequisites

* OS: Ubuntu 20.04 (tested on WSL2)
* Network Interface: Active interface (e.g., eth0)
* API Keys:

  * [ipgeolocation.io](https://ipgeolocation.io)
  * [AbuseIPDB](https://abuseipdb.com)
* Root Access: Required for eBPF

---

## 🧰 Installation

### Clone the Repository:

```bash
git clone https://github.com/your-username/firewall-project.git
cd firewall-project
```

### Install System Dependencies:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv libbpf-dev clang llvm
```

### Set Up Python Environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-socketio netifaces requests bcc
```

### Configure API Keys:

Edit `app.py`:

```python
GEO_API_KEY = "your_ipgeolocation_api_key"
ABUSEIPDB_KEY = "your_abuseipdb_api_key"
```

### Set Network Interface:

```bash
ip link
```

Update `INTERFACE` in `ebpf_handler.py`:

```python
INTERFACE = "your_interface_name"
```

---

## ▶️ Usage

### Run eBPF Packet Capture:

```bash
sudo python3 ebpf_handler.py
```

### Run Flask Backend:

```bash
source venv/bin/activate
python3 app.py
```

Access at: `http://<your-ip>:5000`

### Access Dashboard

Open in browser: `http://<your-ip>:5000`

### Generate Traffic

```bash
ping 8.8.8.8
curl http://example.com
```

### Stop the Project

Press `Ctrl+C` in both terminals. XDP hook is removed automatically.

---

## 📊 Dashboard Features

| Feature               | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| Recent Packets Table  | Shows last 10 packets with IP, Protocol, Country, Threat Score |
| Blocked Packets Table | Lists blocked IPs with red highlight                           |
| Stats Cards           | Total packets, blocked packets, top IPs                        |
| Packet Rate Graph     | Packets/sec over 60 seconds                                    |
| Firewall Rules        | Add/remove rules dynamically                                   |
| Filters & Export      | Filter by IP/protocol/threat score; Export CSV                 |
| Toasts & Alerts       | Real-time alerts for blocks and rate limits                    |

---

## ⚙️ How It Works

### eBPF Packet Capture (`ebpf_handler.py`):

* Uses BCC to attach XDP
* Captures packets and checks rules
* Logs to `packets.json`

### Flask Backend (`app.py`):

* Reads packets and adds metadata (country, threat)
* Sends updates via SocketIO
* Auto-blocks malicious IPs (>50 threat score)

### Web Frontend:

* Built with Bootstrap, Chart.js, and SocketIO
* Displays and animates packet data

---

## 🧪 Example Output

### Ping 8.8.8.8:

```json
{"src_ip": "8.8.8.8", "protocol": 1, "timestamp": 1744642985.71, "blocked": false}
```

### Malicious IP 14.24.17.104:

```bash
Threat check: score 75 → auto-blocked
```

```json
{"ip": "14.24.17.104", "action": "block"}
```

Toast: "Auto-blocked malicious IP: 14.24.17.104"

---

## 🛠️ Troubleshooting

| Issue                 | Fix                                                   |
| --------------------- | ----------------------------------------------------- |
| No packets captured   | Check interface, run with `sudo`, generate traffic    |
| API Errors            | Check API keys, verify internet connection and quota  |
| Dashboard Not Loading | Check Flask logs, use correct IP and port             |
| Too Many IPs          | Filter by score > 25 or update emit logic in `app.py` |

---

## 🔮 Future Improvements

* 🌍 World map of packet origins
* 🌐 IPv6 support
* 📈 Rate-based blocking
* 🏁 Country flag icons
* 🗃️ Store history in DB

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch:

   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit:

   ```bash
   git commit -m "Add new feature"
   ```
4. Push:

   ```bash
   git push origin feature/new-feature
   ```
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## 🙌 Acknowledgments

* [BCC](https://github.com/iovisor/bcc)
* [ipgeolocation.io](https://ipgeolocation.io)
* [AbuseIPDB](https://abuseipdb.com)
* Flask + SocketIO
* Bootstrap + Chart.js

> Built as a learning project to explore **eBPF**, **network security**, and **real-time dashboards**.

⭐ Feel free to star the repo or open issues for feedback!
