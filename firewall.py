import subprocess

def add_rule(ip):
    cmd = f"sudo nft add rule inet filter input ip saddr {ip} drop"
    subprocess.run(cmd, shell=True)

def remove_rule(ip):
    cmd = f"sudo nft delete rule inet filter input handle <handle_id>"
    subprocess.run(cmd, shell=True)