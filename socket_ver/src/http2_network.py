from hyper import HTTPConnection
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import pandas as pd
import os
import netifaces as ni

download_complete_ts = []

def create_connection(url, port):
	connection = HTTPConnection(url, port)
	return connection

def request_html_and_response(connection_obj, webobj_path):
	request = connection_obj.request('GET', webobj_path)
	response = connection_obj.get_response(request)

	print("Download Complete : ", webobj_path)
	
	return response

"""def request_webobj_and_response(connection_obj, webobj_path):
	global download_complete_ts
	print(webobj_path)
	request = connection_obj.request('GET', "/pageLoadTest/"+webobj_path)
	response = connection_obj.get_response(request)

	download_complete_ts.append(time.time())
	print("Download Complete : ", webobj_path)"""


def request_webobj_and_response(connection_obj, webobj_path_list):
	loading_st = time.time()

	for webobj_path in webobj_path_list:
		#request = connection_obj.request('GET', "/pageLoadTest/"+webobj_path)
		request = connection_obj.request('GET', "/alexa_top/ebay/"+webobj_path[2:])

	response = connection_obj.get_response(request)
	print(response.read())

	return (time.time() - loading_st)

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
	start_ts = time.time()
	global download_complete_ts
	url = "opendata.cnu.ac.kr"
	#html_path = "/pageLoadTest/test_50kb.html"
	html_path = "/alexa_top/ebay/ebay.html"
	port = 443

	load_start_ts = time.time()
	# create single http2 connection
	connection = create_connection(url, port)

	# request html and parse it
	html_data = request_html_and_response(connection,html_path)
	html_data = html_data.read()

	web_obj_list = html_parse(html_data)

	#initial_number_of_tags = len(web_obj_list)
	loading_time = request_webobj_and_response(connection, web_obj_list)

	#record loading time to file
	crnt_dict = {'timestamp': start_ts, 'loadingTime':(loading_time)*1000, 'protocol':'http2'}
	crnt_df = pd.DataFrame()
	crnt_df = crnt_df.append(crnt_dict, ignore_index = True)

	local_ip = ni.ifaddresses('enp0s10')[ni.AF_INET][0]['addr']
	splited_ip = local_ip.split('.')
	client_id = splited_ip[len(splited_ip)-1]

	log_file_dir = "/home/minjiwon/socket_concurrent_connect/loading_time_data/plr_5/h1_7_h2_3/"
	log_file_name = client_id+"_http2_ldt.csv"
	log_file_path = log_file_dir+log_file_name
	
	"""if os.path.isfile(log_file_path):
		with open(log_file_path, 'a') as f:
			crnt_df.to_csv(f, header = False)
	else:
		crnt_df.to_csv(log_file_path)"""

if __name__== "__main__":
	main()

