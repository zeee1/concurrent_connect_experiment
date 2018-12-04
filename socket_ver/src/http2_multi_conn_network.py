from hyper import HTTPConnection
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import pandas as pd
import os

download_complete_ts = []

## create connection
def create_connection(url, port):
	connection = HTTPConnection(url, port)
	return connection

def request_html_and_response(connection_obj, webobj_path):
	request = connection_obj.request('GET', webobj_path)
	response = connection_obj.get_response(request)
	
	return response

def request_webobj_and_response(connection_obj, webobj_path):
	global download_complete_ts
	request = connection_obj.request('GET', "/pageLoadTest/"+webobj_path)
	response = connection_obj.get_response(request)

	download_complete_ts.append(time.time())

def multiplex_stream_task(connection_obj, webobj_path_list):
	#while len(webobj_path_list) != 0:
	for webobj_path in webobj_path_list:
		#webobj_path = webobj_path_list.pop(0)
		request = connection_obj.request('GET', "/alexa_top/ebay/"+webobj_path[2:])
		
	response = connection_obj.get_response(request)

	download_complete_ts.append(time.time())


def multiple_connection_task(connection_list, webobj_path_list):
	executor = ThreadPoolExecutor(max_workers=len(connection_list))
	splited_list = [webobj_path_list[:int(len(webobj_path_list)/2)],webobj_path_list[int(len(webobj_path_list)/2):]]

	for i in range(0, 2):
		executor.submit(multiplex_stream_task,connection_list[i], splited_list[i])

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
	global download_complete_ts
	url = "opendata.cnu.ac.kr"
	html_path = "/alexa_top/ebay/ebay.html"
	port = 443

	load_start_ts = time.time()
	# create two http2 connection
	connection_1 = create_connection(url, port)
	connection_2 = create_connection(url, port)

	# request html and parse it
	html_response = request_html_and_response(connection_1, html_path)
	html_data = html_response.read()

	web_obj_list = html_parse(html_data)

	multiple_connection_task([connection_1, connection_2], web_obj_list)

	while True:
		if len(download_complete_ts) == 2:
			break
	
	load_end_ts = max(download_complete_ts)

	#record loading time to file
	crnt_dict = {'timestamp': time.time(), 'loadingTime':(load_end_ts - load_start_ts)*1000, 'protocol':'http2_multi'}
	crnt_df = pd.DataFrame()
	crnt_df = crnt_df.append(crnt_dict, ignore_index = True)
	print(crnt_df)

	"""log_file_dir = "/home/minjiwon/socket_concurrent_connect/loading_time_data/h1_7_h2_3/"
	log_file_name = "http2_multi_ldt.csv"
	log_file_path = log_file_dir+log_file_name
	
	if os.path.isfile(log_file_path):
		with open(log_file_path, 'a') as f:
			crnt_df.to_csv(f, header = False)
	else:
		crnt_df.to_csv(log_file_path)"""

if __name__== "__main__":
	main()
