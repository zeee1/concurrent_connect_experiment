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

def mean_ttfb_by_protocol(valid_dataset):
	http1_df = valid_dataset.loc[valid_dataset['protocol'] == "http1",]
	http2_df = valid_dataset.loc[valid_dataset['protocol'] == "http2",]

	http1_mean_ttfb = http1_df['ttfb'].mean()
	http2_mean_ttfb = http2_df['ttfb'].mean()

	http1_networkTime = http1_df['networkTime'].mean()
	http2_networkTime = http2_df['networkTime'].mean()

	http1_renderingTime = http1_df['computationTime'].mean()
	http2_renderingTime = http2_df['computationTime'].mean()

	http1_plt = http1_df['plt'].mean()
	http2_plt = http2_df['plt'].mean()
	

	return [(http1_plt, http1_mean_ttfb,http1_networkTime,http1_renderingTime), (http2_plt,http2_mean_ttfb, http2_networkTime, http2_renderingTime)]

def main():
	test_case_list = ["h1_0_h2_10", "h1_3_h2_7", "h1_5_h2_5", "h1_7_h2_3", "h1_10_h2_0"]
	data_path = "../data/ebay/plr_5/"
	resultDF = pd.DataFrame()
	
	for test_case in test_case_list:
		# merge all client's log
		test_case_data_path = data_path+test_case+"/"
		merged_df = merge_all_client_log(test_case_data_path)
		# get 10 rows from log of each client.
		valid_dataset = extract_valid_logs_from_each_client(merged_df)

		
		for key, value in valid_dataset.items():
			mean_ttfb =mean_ttfb_by_protocol(value)
			resultDF = resultDF.append({'plt':mean_ttfb[0][0],'ttfb': mean_ttfb[0][1],'networkTime':mean_ttfb[0][2],'renderingTime':mean_ttfb[0][3], 'protocol':'http1', 'test_case':test_case}, ignore_index = True)
			resultDF = resultDF.append({'plt':mean_ttfb[1][0],'ttfb': mean_ttfb[1][1],'networkTime':mean_ttfb[1][2],'renderingTime':mean_ttfb[1][3], 'protocol':'http2', 'test_case':test_case}, ignore_index = True)
		

	resultDF.to_csv("../data/ebay/default_ebay_data_for_vs.csv")
	return 1

if __name__ == "__main__":
	main()