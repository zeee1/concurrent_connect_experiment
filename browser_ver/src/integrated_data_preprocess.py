import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from glob import glob

def merge_all_client_log(test_case_data_path):
	resultDF = pd.DataFrame()
	all_log_file_path = glob(test_case_data_path+"*")
	sorted_client_file_path_list = sorted(all_log_file_path)
	
	for file_path in sorted_client_file_path_list:
		log_df = pd.read_csv(file_path)
		splited_file_path = file_path.split("/")
		client_ip = splited_file_path[len(splited_file_path)-1][:3]
		log_df["client"] = client_ip

		resultDF = resultDF.append(log_df, ignore_index = True)

	return resultDF

def get_unique_timestamp_list(_data):
	unique_ts = _data['timestamp'].drop_duplicates().tolist()

	prev_ts = 0
	ts_list = []
	tmp_list = []
	for ts in unique_ts:
		if ts - prev_ts <= 3:
			ts_list[-1:][0].append(ts)

		else:
			ts_list.append([ts,])

		prev_ts= ts

	return ts_list

"""
	func : collect_valid_test_result
	- collect valid 10 test result, store it in dictionary and return dictionary
"""
def extract_valid_logs_from_each_client(merged_log_df):
	prev_dataset = ""
	prev_lower_lim = 0 
	prev_upper_lim = 0
	sorted_merge_data = merged_log_df.sort_values('timestamp')
	pd.options.display.float_format = '{:f}'.format

	test_count = 0
	
	# collect valid 10 test result and store it in dictionary
	result_dict = {}

	# groub by timestamp
	# get unique timestamp from merged data
	unique_ts_list = get_unique_timestamp_list(sorted_merge_data)

	for ts in unique_ts_list:
		if test_count == 10:
			break

		tmp_df = pd.DataFrame()
		if len(ts) >=  2:
			for i in ts:
				tmp_df_t = sorted_merge_data.loc[sorted_merge_data['timestamp'] == int(i),]
				#tmp_df_2 = sorted_merge_data.loc[sorted_merge_data['timestamp'] == ts[1],]
				tmp_df = tmp_df.append(tmp_df_t)
		else:
			tmp_df = sorted_merge_data.loc[sorted_merge_data['timestamp'] == ts[0],]

		if tmp_df["client"].count()< 9:
			continue

		is_valid = bool_contain_outlier(tmp_df)

		if is_valid[0] == False:
			continue
		#if is_valid[3] < prev_lower_lim or is_valid[3] > prev_upper_lim:
		#	continue
				
		else:
			result_dict[str(ts[0])] = tmp_df
			test_count += 1
			prev_dataset = tmp_df
			prev_lower_lim = is_valid[1]
			prev_upper_lim = is_valid[2]

	return result_dict

def bool_contain_outlier(dataset):
	count_of_dataset = 10

	http1_df = dataset.loc[dataset['protocol'] == "http1",]
	http2_df = dataset.loc[dataset['protocol'] == "http2",]
	
	nt_list = dataset['networkTime'].tolist()
	nt_list.sort()
	nt_median = dataset['networkTime'].median()
	nt_lower_quartile = nt_list[int((count_of_dataset+1)/4)]
	nt_upper_quartile = nt_list[int((count_of_dataset+1)*3/4)]
	inter_quartile_range = nt_upper_quartile - nt_lower_quartile
	lower_limit = nt_lower_quartile - 1.5*inter_quartile_range
	upper_limit = nt_upper_quartile + 1.5*inter_quartile_range

	for nt in nt_list:
		if nt < lower_limit or nt > upper_limit:
			return (False,)

	return (True, lower_limit, upper_limit, nt_median)

def calculate_jain_fairness_index(test_case_data, num_of_client):

	size_of_page = 20971520

	test_case_data['throughput'] = size_of_page/(test_case_data['plt']/1000)

	fair_throughput = size_of_page/(test_case_data['plt'].mean())
	print("fair_throughput: ", fair_throughput)
	fair_obj_nt = size_of_page/fair_throughput

	test_case_data['normalized_throughput'] = test_case_data['throughput']/fair_throughput

	sqrt_of_sum_of_nt = (test_case_data['normalized_throughput'].sum())**2

	throughput_list = test_case_data['normalized_throughput'].tolist()
	sum_of_sqrt_of_nt = 0
	
	for i in throughput_list:
		sum_of_sqrt_of_nt += (i*i)

	print("up side value : ", sqrt_of_sum_of_nt)
	print("down side value : ", (num_of_client*sum_of_sqrt_of_nt))
	fairness_index = sqrt_of_sum_of_nt/(num_of_client*sum_of_sqrt_of_nt)

	return fairness_index

def calculate_throughput_fairness_index(test_case_data):
	size_of_page = 20971520
	test_case_data['throughput'] = size_of_page/(test_case_data['networkTime']/1000)
	number_of_client = 10

	h1_df = test_case_data.loc[test_case_data['protocol'] == 'http1',]
	h2_df = test_case_data.loc[test_case_data['protocol'] == 'http2',]

	h1_mean_throughput = h1_df['throughput'].mean()
	h2_mean_throughput = h2_df['throughput'].mean()

	return h2_mean_throughput - h1_mean_throughput


def calculate_std_of_plt(test_case_data):
	print(test_case_data['plt'].tolist())
	return test_case_data['plt'].std()

def calculate_jain_fairness_index_2(client_throughput_list, num_of_client):

	size_of_page = 20971520

	fair_throughput = sum(client_throughput_list)/num_of_client
	print("fair_throughput: ", fair_throughput)
	fair_obj_nt = size_of_page/fair_throughput

	normalized_throughput_list = []
	for i in client_throughput_list:
		normalized_throughput_list.append(i/fair_throughput)

	sqrt_of_sum_of_nt = (sum(normalized_throughput_list))**2

	sum_of_sqrt_of_nt = 0
	
	for i in normalized_throughput_list:
		sum_of_sqrt_of_nt += (i*i)

	print("up side value : ", sqrt_of_sum_of_nt)
	print("down side value : ", (num_of_client*sum_of_sqrt_of_nt))
	fairness_index = sqrt_of_sum_of_nt/(num_of_client*sum_of_sqrt_of_nt)

	return fairness_index

def main():
	result = pd.DataFrame()
	test_case_list = ["del_10","del_100","del_10_plr_0.1","del_10_plr_0.5","del_10_plr_1","del_10_plr_3","del_10_plr_5","del_50","del_50_plr_0.1","del_50_plr_0.5","del_50_plr_1","del_50_plr_3","del_50_plr_5","del_100_plr_0.1","del_100_plr_0.5","del_100_plr_1","del_100_plr_3","del_100_plr_5", "del_150", "del_150_plr_0.1", "del_150_plr_0.5", "del_150_plr_1", "del_150_plr_3", "del_150_plr_5", "del_200", "del_200_plr_0.1", "del_200_plr_0.5","del_200_plr_1", "del_200_plr_3", "del_200_plr_5"]
	protocol_ratio= "h1_5_h2_5"
	#test_case_list = ["h1_3_h2_7", "h1_5_h2_5", "h1_7_h2_3"]
	data_path = "../data/ebay/"
	resultDF = pd.DataFrame()
	
	for test_case in test_case_list:
		# merge all client's log
		test_case_data_path = data_path+test_case+"/"+protocol_ratio+"/"
		print(test_case)
		splited_test_case = test_case.split("_")

		if len(splited_test_case) < 3:
			delay = int(splited_test_case[1])
			packet_loss_rate = 0
		else:
			delay = int(splited_test_case[1])
			packet_loss_rate = float(splited_test_case[3])
		merged_df = merge_all_client_log(test_case_data_path)
		
		# get 10 rows from log of each client.
		valid_dataset = extract_valid_logs_from_each_client(merged_df)
		
		for key, value in valid_dataset.items():
			if value.shape[0] == 10:
				fi = calculate_jain_fairness_index(value, 10)
				print(fi)
				result = result.append({'fi':fi, 'test_case':test_case, 'packet_loss_rate':packet_loss_rate, 'delay':delay}, ignore_index = True)

		#print("-----------------------------------------------------------")

	result.to_csv("../data/ebay/jain_fairness_index_for_vs.csv")

if __name__ == "__main__":
	main()	

