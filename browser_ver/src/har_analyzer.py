from haralyzer import HarPage, HarParser, MultiHarParser
import json
import dateutil
import datetime
import json
from haralyzer import HarParser, HarPage
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import  plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np


def parse_har(data_path):
	#test_runs = []
	df_data = pd.DataFrame()

	with open(data_path, 'r') as f1:
		#test_runs.append(f1.read())
		har_data = f1.read()
	json_har_data = eval(har_data)
	har_log = json_har_data['log']
	har_log_entries=  har_log['entries']

	for entry in har_log_entries:
		url = entry['request']['url']
		status = entry['response']['status']
		if "opendata.cnu.ac.kr" in url and status == 200:
			start_datetime = entry['startedDateTime']
			load_time = entry['time']
			splited_url = url.split("/")
			object_name = splited_url[-1:]
			df_data = df_data.append({'start_datetime':start_datetime, 'load_time':load_time, 'object_name':object_name}, ignore_index = True)

	return df_data

def vs_page_load(processed_har_log):
	return 1

def main():
	data_path = '../data/ebay_har/del_150_plr_5_ebay_h1.har'
	extracted_df = parse_har(data_path)
	extracted_df.to_csv("../data/ebay_har/del_150_plr_5_ebay_h1.csv")

	data_path = '../data/ebay_har/del_150_plr_5_ebay_h2.har'
	extracted_df = parse_har(data_path)
	extracted_df.to_csv("../data/ebay_har/del_150_plr_5_ebay_h2.csv")


	h1_data = pd.read_csv("../data/ebay_har/del_150_plr_5_ebay_h1.csv")
	h2_data = pd.read_csv("../data/ebay_har/del_150_plr_5_ebay_h2.csv")

	h1_data['start_datetime'] = pd.to_datetime(h1_data['start_datetime'])
	start_dt_list = h1_data['start_datetime'].tolist()
	duration_time_list = h1_data['load_time'].tolist()
	h1_data = h1_data.to_dict('records')

	min_start_dt = min(start_dt_list)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	y_pos = 135
	for i in h1_data:
		start_ts = i['start_datetime']-min_start_dt
		left_value = start_ts.seconds*1000+start_ts.microseconds/1000
		i['left_value'] = left_value
		ax.barh(y_pos, i['load_time'], left = left_value, height = 1, align = 'center', color = 'blue')
		y_pos -=1

	#h1_data = pd.DataFrame(h1_data)
	#ax.barh(np.arange(135), h1_data['load_time'].tolist(), h1_data['left_value'].tolist(), align = 'center')

	plt.show()

	h2_data['start_datetime'] = pd.to_datetime(h2_data['start_datetime'])
	start_dt_list = h2_data['start_datetime'].tolist()
	duration_time_list = h2_data['load_time'].tolist()
	h2_data['end_datetime'] = [start_dt_list[i]+datetime.timedelta(0, 0, duration_time_list[i]) for i in range(0, len(start_dt_list))]
	h2_data = h2_data.to_dict('records')

	min_start_dt = min(start_dt_list)

	fig = plt.figure()
	# ax = fig.add_axes([0.15,0.2,0.75,0.3]) #[left,bottom,width,height]
	ax = fig.add_subplot(111)

	y_pos = 135
	print('-------------------------------------------')
	for i in h2_data:
		start_ts = i['start_datetime']-min_start_dt
		left_value = start_ts.seconds*1000+start_ts.microseconds/1000
		ax.barh(y_pos, i['load_time'], left = left_value, height = 1, align = 'center', color = 'blue')
		y_pos -= 1

	plt.show()



if __name__ == "__main__":
	main()