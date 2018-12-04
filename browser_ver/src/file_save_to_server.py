import os

client_ip_addr = ["192.168.0.100", "192.168.0.102", "192.168.0.103", "192.168.0.104", "192.168.0.105", "192.168.0.106", "192.168.0.107", "192.168.0.108", "192.168.0.109", "192.168.0.110"]

# save http1_network.py on 10 clients.


for i in range(0, 5):
    cmd = "sshpass -p '1234' scp packet_capture_h1.py "+client_ip_addr[i]+":/home/minjiwon/browser_concurrent_connect/packet_capture_test"
    os.system(cmd)

# save http2_network.py on 10 clients.
for i in range(5, 10):
	cmd = "sshpass -p '1234' scp packet_capture_h2.py "+client_ip_addr[i]+":/home/minjiwon/browser_concurrent_connect/packet_capture_test"
	os.system(cmd)
  