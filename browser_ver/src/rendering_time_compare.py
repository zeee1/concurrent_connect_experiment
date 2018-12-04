import pandas as pd
from glob import glob

def merge_all_client_log(test_case_data_path):
	resultDF = pd.DataFrame()
	all_log_file_path = glob(test_case_data_path+"/*")
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
	for ts in unique_ts:
		if ts - prev_ts == 1:
			ts_list = ts_list[:-1]
			ts_list.append((prev_ts, ts))
		else:
			ts_list.append([ts,])

		prev_ts= ts

	return ts_list

"""
	func : collect_valid_test_result
	- collect valid 10 test result, store it in dictionary and return dictionary
"""
def extract_valid_logs_from_each_client(merged_log_df):
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
		if len(ts) == 2:
			tmp_df_1 = sorted_merge_data.loc[sorted_merge_data['timestamp'] == ts[0],]
			tmp_df_2 = sorted_merge_data.loc[sorted_merge_data['timestamp'] == ts[1],]
			tmp_df = tmp_df_1.append(tmp_df_2)
		else:
			tmp_df = sorted_merge_data.loc[sorted_merge_data['timestamp'] == ts[0],]
		
		if tmp_df["client"].count()< 9:
			continue

		else:
			result_dict[str(ts[0])] = tmp_df
			test_count += 1

	return result_dict

def get_rendering_time_by_protocol(test_case, test_case_data_path):
	merged_df = merge_all_client_log(test_case_data_path)
	valid_dataset = extract_valid_logs_from_each_client(merged_df)
	resultDF = pd.DataFrame()

	for key, value in valid_dataset.items():
		# get median rendering time of h1 and h2
		http1_df = value.loc[value['protocol'] == 'http1',]
		http2_df = value.loc[value['protocol'] == 'http2',]
		mean_of_rendering_time_h1 = http1_df['computationTime'].mean()
		mean_of_rendering_time_h2 = http2_df['computationTime'].mean()
		resultDF = resultDF.append({'test_case' : test_case, 'h1_rendering_time':mean_of_rendering_time_h1, 'h2_rendering_time':mean_of_rendering_time_h2}, ignore_index = True)

	return resultDF

def get_network_time_by_protocol(test_case, test_case_data_path):
	merged_df = merge_all_client_log(test_case_data_path)
	valid_dataset = extract_valid_logs_from_each_client(merged_df)
	resultDF = pd.DataFrame()

	for key, value in valid_dataset.items():
		# get median rendering time of h1 and h2
		http1_df = value.loc[value['protocol'] == 'http1',]
		http2_df = value.loc[value['protocol'] == 'http2',]
		mean_of_network_time_h1 = http1_df['networkTime'].mean()
		mean_of_network_time_h2 = http2_df['networkTime'].mean()
		resultDF = resultDF.append({'test_case' : test_case, 'h1_network_time':mean_of_rendering_time_h1, 'h2_network_time':mean_of_rendering_time_h2}, ignore_index = True)

	return resultDF

def main():
	data_path = "../data/third/default/"
	test_case_list = ["h1_3_h2_7", "h1_5_h2_5", "h1_7_h2_3"]

	for test_case in test_case_list:
		path = data_path+test_case
		data = get_rendering_time_by_protocol(test_case, path)
		print("h1 - min/avg/max : ", data['h1_rendering_time'].min(), "/", data['h1_rendering_time'].mean(),"/", data['h1_rendering_time'].max())
		print("h2 - min/avg/max : ", data['h2_rendering_time'].min(), "/", data['h2_rendering_time'].mean(),"/", data['h2_rendering_time'].max())

if __name__ == "__main__":
	main()