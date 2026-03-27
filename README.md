DoS Attack Detection and Mitigation
This is a project I built as part of my Post Graduate Diploma in Advanced Secure Software Development (PG-DASSD) at CDAC. The idea came from wanting to understand how DoS attacks actually work at a network level and how we can stop them in real time using Python and Linux firewall rules.
What This Project Does
The project has three main parts:
A simple HTTP server that accepts connections and logs every request with the IP address and timestamp
An attack script that floods the server with HTTP and SYN requests to simulate a real DoS attack
A mitigation script that watches the log file and automatically blocks any IP that sends too many requests using iptables
The idea is to run all three together in a lab setup and see the detection and blocking happen in real time.
Files in This Project
File
What it does
server.py
Custom HTTP server built using socket programming. Logs all incoming connections to request_log.txt
mitigation.py
Reads the log every second, counts requests per IP, and blocks attackers using iptables
attack.py
Simulates a combined HTTP flood and SYN flood attack using multiprocessing and threading
index.html
Simple web page that the server serves
request_log.txt
Auto-generated when the server runs. Stores timestamp, IP, and request type
How to Run It
You need Ubuntu Linux ,Kali Linux and Python 3. No extra libraries to install — everything uses the standard Python library.
Terminal 1 — Start the server:
python3 server.py in Ubuntu Linux
Terminal 2 — Start the mitigation engine (needs root):
sudo python3 mitigation.py in Ubuntu Linux 
Terminal 3 — Run the attack (from another machine or terminal):
python3 attack.py Kali Linux 
Once the attack starts, you will see the mitigation script detecting the flood and blocking the attacker IP automatically. The block lasts 60 seconds and then the IP is unblocked.
Detection Logic
The mitigation script checks how many requests each IP sent in the last 3 seconds
If any IP crosses 30 requests in that window, it gets blocked immediately via iptables
After 60 seconds the block is removed automatically
All iptables rules are cleaned up when you stop the script with CTRL+C
What I Learned
How DoS attacks work at the socket level (HTTP flood vs SYN flood)
How to use Python's socket module to build a basic HTTP server from scratch
How iptables works on Linux to block/drop packets from specific IPs
How to use multiprocessing and threading together to generate high traffic
Real-time log monitoring and sliding window based detection logic
Setup I Used
I ran this on two virtual machines connected via a host-only network in VirtualBox:
Server VM: Ubuntu — ran server.py and mitigation.py
Attacker VM: Kali — ran attack.py
The server IP in my setup was 192.168.56.101 and the attacker was 192.168.56.102. You can change these in the scripts based on your setup.
Note
This project is only for learning purposes. I built and tested it in a closed lab environment. Please don't use the attack script on any real server or network.
Contact
Shubhash Pisike
Email: shubhashh27@gmail.com
LinkedIn: https://www.linkedin.com/in/shubhash-pisike-4815bb255
Portfolio: https://shubhashh.github.io/Portfolio/
