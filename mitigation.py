#!/usr/bin/env python3

import signal
import sys
import time
import subprocess
import os
from collections import defaultdict

LOG_FILE = 'request_log.txt'
THRESHOLD = 30         
TIME_WINDOW = 3        
INTERVAL = 1
BLOCK_TIME = 60
blocked_ips = {}
running = True

def cleanup(sig=None, frame=None):
    print("\n[!] Cleaning up iptables...")
    for ip in list(blocked_ips.keys()):
        unblock_ip(ip)
    
    subprocess.run("iptables -F", shell=True, stderr=subprocess.DEVNULL)
    print("[+] All rules removed. Clean exit.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def block_ip(ip):
    
    subprocess.run(f"iptables -I INPUT -s {ip} -j DROP", shell=True)
    subprocess.run(f"iptables -I INPUT -s {ip} -p tcp --dport 8080 -j REJECT", shell=True)
    
    subprocess.run(f"ss -K dst {ip}", shell=True, stderr=subprocess.DEVNULL)
    blocked_ips[ip] = time.time() + BLOCK_TIME
    print(f"     BLOCKED: {ip} for {BLOCK_TIME}s")

def unblock_ip(ip):
    subprocess.run(f"iptables -D INPUT -s {ip} -j DROP", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -D INPUT -s {ip} -p tcp --dport 8080 -j REJECT", shell=True, stderr=subprocess.DEVNULL)
    if ip in blocked_ips:
        del blocked_ips[ip]
    print(f"     UNBLOCKED: {ip}")

def check_unblock():
    for ip in list(blocked_ips.keys()):
        if time.time() >= blocked_ips[ip]:
            unblock_ip(ip)

def count_requests():
    counts = defaultdict(int)
    current = time.time()
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    ts, ip = float(parts[0]), parts[1]
                    if current - ts <= TIME_WINDOW:
                        counts[ip] += 1
    except:
        pass
    return counts

def monitor():
    
    subprocess.run("iptables -F", shell=True, stderr=subprocess.DEVNULL)
    print("=" * 50)
    print("   DoS MITIGATION (HTTP + SYN)")
    print("=" * 50)
    print(f"[*] Threshold: {THRESHOLD} req/{TIME_WINDOW}s")
    print(f"[*] Block time: {BLOCK_TIME}s")
    print("[*] Press CTRL+C to stop\n")
    
    while running:
        check_unblock()
        counts = count_requests()
        ts = time.strftime('%H:%M:%S')
        print(f"\n[{ts}] Monitoring...")
        
        for ip, count in counts.items():
            if ip in blocked_ips:
                remain = int(blocked_ips[ip] - time.time())
                print(f"     {ip} BLOCKED ({remain}s left)")
            elif count >= THRESHOLD:
                print(f"     ATTACK: {ip} -> {count} requests")
                block_ip(ip)
            else:
                print(f"     {ip} -> {count} requests")
        
        if not counts and not blocked_ips:
            print("    No traffic")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[ERROR] Must run as root: sudo python3 mitigation.py")
        sys.exit(1)
    monitor()
