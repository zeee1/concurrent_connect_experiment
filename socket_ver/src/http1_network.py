import http.client
import socket
import concurrent.futures
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import pandas as pd
import os
import netifaces as ni

download_complete_ts = []

# create single http1 connection between server and client
def create_connection(url, port):
	connection = http.client.HTTPSConnection(url, port)
	return connection

# send request and receive response and return response data
def request_and_response(connection_obj, webobj_path):
	connection_obj.request('GET', webobj_path)
	response = connection_obj.getresponse()
	return response

# thread function - create 6 http connection and request web object parellel
def multiple_connection_thread_func(connection_list, request_distribution):
	MAX_CONNECTION = 6
	executor = ThreadPoolExecutor(max_workers=MAX_CONNECTION)
	for i in range(0,MAX_CONNECTION):
		executor.submit(request_multi_obj, connection_list[i], request_distribution['connection_'+str(i)])


# request multiple web object(webobj_path_list) on single connection(connection_obj) and record received data on file
def request_multi_obj(connection_obj, webobj_path_list):
	global download_complete_ts
	for webobj_path in webobj_path_list:
		#connection_obj.request('GET',"/pageLoadTest/"+webobj_path)
		connection_obj.request('GET', "/alexa_top/ebay/"+webobj_path[2:])
		response = connection_obj.getresponse()
		response.read()

	download_complete_ts.append(time.time())
	connection_obj.close()

def html_parse(html_data):
	web_obj_list = list()
	soup = BeautifulSoup(html_data, 'html.parser')
	
	#get src from img or script or iframe
	js_list = soup.find_all("script")
	js_src_list = list()

	for js in js_list:
		try:
			js_src = js['src']
			js_src_list.append(js_src)
		except KeyError:
			continue

	web_obj_list += js_src_list

	img_list = soup.find_all("img")
	img_src_list = list()

	for img in img_list:
		try:
			img_src = img['src']
			img_src_list.append(img_src)
		except KeyError:
			continue

	web_obj_list += img_src_list

	iframe_list = soup.find_all("iframe")
	iframe_src_list = list()

	for iframe in iframe_list:
		try:
			iframe_src = iframe['src']
			iframe_src_list.append(iframe_src)
		except KeyError:
			continue

	web_obj_list += iframe_src_list

	link_list = soup.find_all("link")
	link_src_list = list()

	for link in link_list:
		try:
			if link['href'].startswith("./"):
				link_src_list.append(link['href'])
		except KeyError:
			continue

	web_obj_list += link_src_list

	return web_obj_list

def main():
	# create multiple connection
	start_ts = time.time()
	global download_complete_ts
	url = "opendata.cnu.ac.kr"
	#html_path = "/pageLoadTest/test_50kb.html"
	html_path = "/alexa_top/ebay/ebay.html"
	port = 80
	MAX_CONNECTION = 6
	connection_list = list()

	load_start_ts = time.time()

	for i in range(0, MAX_CONNECTION):
		connection_list.append(create_connection(url, port))

	# request html -> get response data -> parse html and get another object url
	html_data = request_and_response(connection_list[0],html_path)
	html_data = html_data.read()

	web_obj_list = html_parse(html_data)

	request_distribution = {"connection_0":list(),"connection_1":list(),"connection_2":list(),"connection_3":list(),"connection_4":list(),"connection_5":list()}

	count = 0

	for web_obj in web_obj_list:
		connection_id = "connection_"+str(count % 6)
		request_distribution[connection_id].append(web_obj)
		count += 1


	# request another object using 6 connections
	# process parellel task using thread
	multiple_connection_thread_func(connection_list, request_distribution)

	while True:
		if len(download_complete_ts) == 6:
			break

	download_time = max(download_complete_ts) - load_start_ts

	#record loading time to file
	crnt_dict = {'timestamp': start_ts, 'loadingTime':(download_time)*1000, 'protocol':'http1'}
	crnt_df = pd.DataFrame()
	crnt_df = crnt_df.append(crnt_dict, ignore_index = True)

	local_ip = ni.ifaddresses('enp0s10')[ni.AF_INET][0]['addr']
	splited_ip = local_ip.split('.')
	client_id = splited_ip[len(splited_ip)-1]


	log_file_dir = "/home/minjiwon/socket_concurrent_connect/loading_time_data/plr_5/h1_10_h2_0/"
	log_file_name = client_id+"_http1_ldt.csv"
	log_file_path = log_file_dir+log_file_name
	
	"""if os.path.isfile(log_file_path):
		with open(log_file_path, 'a') as f:
			crnt_df.to_csv(f, header = False)
	else:
		crnt_df.to_csv(log_file_path)"""

if __name__== "__main__":
	main()