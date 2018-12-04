import os

client_ip_addr = ["192.168.0.100", "192.168.0.102", "192.168.0.103", "192.168.0.104", "192.168.0.105", "192.168.0.106", "192.168.0.107", "192.168.0.108", "192.168.0.109", "192.168.0.110"]

# save http1_network.py on 10 clients.
for i in range(0, 10):
    cmd = "sshpass -p '1234' scp http1_network.py "+client_ip_addr[i]+":/home/minjiwon/socket_concurrent_connect/src"
    os.system(cmd)

# save http2_network.py on 10 clients.
"""for i in range(7, 10):
    cmd = "sshpass -p '1234' scp http2_network.py "+client_ip_addr[i]+":/home/minjiwon/socket_concurrent_connect/src"
    os.system(cmd)"""
