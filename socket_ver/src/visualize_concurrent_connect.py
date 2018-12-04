from glob import glob
from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

"""
	func : merge_Client_PLT(dirName)
	- merge all data from client and return
	- dirName : the path of client log data
"""
def merge_Client_PLT(dirName):
	# plt_df : dataframe storing all records from all client
	plt_df = pd.DataFrame()
	# get path of all client
	print(dirName)
	subDir_list = glob(dirName+"*/")
	# sort sub directory path by character
	sorted_subDir_list = sorted(subDir_list)

	for dirName in subDir_list:
		# get file path - log of PLT from each client
		filePath = glob(dirName+"*")[0]
		print(filePath)
		# client_ip : C class address of each client. used for identification
		client_ip = dirName.split("/")[3]
		# get log of PLT from each client
		data = pd.read_csv(filePath)
		# add "client" attribute and assign client_ip
		data["client"] = client_ip

		if "http1" in filePath:
			data['protocol'] = "http1"
		elif "http2" in filePath:
			data['protocol'] = "http2"

		plt_df = plt_df.append(data, ignore_index=True)

	return plt_df

"""
	func : sort_by_timestamp
	- sort merged data by timestamp
"""
def sort_by_timestamp(_data):
	# sort merged data by timestamp
	sorted_data = _data.sort_values('timestamp')
	pd.options.display.float_format = '{:.2f}'.format

	return sorted_data

"""
	func : get_unique_timestamp_list
	- return unique timestamp list
"""
def get_unique_timestamp_list(_data):
	unique_ts = _data['timestamp'].drop_duplicates().tolist()

	prev_ts = 0
	ts_list = []
	for ts in unique_ts:
		if ts - prev_ts == 1:
			ts_list = ts_list[:-1]
			ts_list.append((int(prev_ts), int(ts)))
		else:
			ts_list.append([int(ts),])

		prev_ts= int(ts)

	return ts_list

"""
	func : collect_valid_test_result
	- collect valid 10 test result, store it in dictionary and return dictionary
"""
def collect_valid_test_result(sorted_merge_data):
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

"""
	func : reassemble_data
	- _data : 10 test plt set. Each test plt set consists of n http1 plt and (10-n) http2 plt
	- calculate average of PLT on http1 and http2 by each test
"""
def reassemble_data(_data):
	result_dict = {"http1":[], "http2":[]}

	for key in _data.keys():
		# key is timestamp
		tmp_df = _data[key]

		# split by protocol
		splitDf_h1 = tmp_df.loc[tmp_df['protocol'] == "http1", ]
		splitDf_h2 = tmp_df.loc[tmp_df['protocol'] == "http2", ]

		if splitDf_h1["protocol"].count() != 0:
			result_dict["http1"].append(splitDf_h1['loadingTime'].mean())
		if splitDf_h2["protocol"].count() != 0:
			result_dict["http2"].append(splitDf_h2['loadingTime'].mean())

	return result_dict

"""
	func : convertToDF
	- dict_data : summarized test data from reassemble_data
	- testName : the name of test_Case
	- convert dict_data(dictionary) to pandas Dataframe
"""
def convertToDF(dict_data, testName):
	data = pd.DataFrame()
	data['plt'] = dict_data["http1"]
	data['protocol'] = "http1"
	data = data.append(pd.DataFrame({"plt":dict_data["http2"], "protocol" : "http2"}))
	data["testName"] = testName
	return data

def mergeDF(src, dest):
	if src['plt'].count() == 0:
		return dest
	elif dest['plt'].count() == 0:
		return src
	else:
		src = src.append(dest, ignore_index = True)
		return src

def visualize_and_analyze( h1_10_h2_0,h1_7_h2_3, h1_5_h2_5, h1_3_h2_7, h1_0_h2_10):
	total_result_set = mergeDF(convertToDF(h1_10_h2_0),convertToDF(h1_7_h2_3, "h1:7_h2:3")
	total_result_set = mergeDF(total_result_set, convertToDF(h1_5_h2_5, "h1:5_h2:5"))
	total_result_set = mergeDF(total_result_set, convertToDF(h1_3_h2_7, "h1:3_h2:7"))
	total_result_set = mergeDF(total_result_set, convertToDF(h1_0_h2_10, "h1:0_h2:10"))
	print(total_result_set)
	a = total_result_set.groupby("testName")
	fig = plt.figure()
	ax = sns.boxplot(x = "testName", y = "networktime", hue="protocol", data = total_result_set, palette="PRGn")
	ax.set_title("PLT of http1/http2 when multi-user = 10")
	#ax.set_ylim([500,1500])
	ax.set_ylabel("PLT(ms)")
	ax.set_xlabel("Ratio Of Protocol")
	#sns.despine(offset = 10, trim= True)
	
	plt.show()

"""def visualize_and_analyze(h1_7_h2_3, h1_5_h2_5, h1_3_h2_7):
	total_result_set = mergeDF(convertToDF(h1_7_h2_3, "h1:7_h2:3"), convertToDF(h1_5_h2_5, "h1:5_h2:5"))
	total_result_set = mergeDF(total_result_set, convertToDF(h1_3_h2_7, "h1:3_h2:7"))

	a = total_result_set.groupby("testName")
	fig = plt.figure()
	ax = sns.boxplot(x = "testName", y = "plt", hue="protocol", data = total_result_set, palette="PRGn")
	ax.set_title("PLT of http1/http2 when multi-user = 10")
	#ax.set_ylim([500,1500])
	ax.set_ylabel("PLT(ms)")
	ax.set_xlabel("Ratio Of Protocol")
	#sns.despine(offset = 10, trim= True)
	
	plt.show()"""


def main():
	test_case_list = ["h1_10_h2_0", "h1_7_h2_3", "h1_5_h2_5", "h1_3_h2_7", "h1_0_h2_10"]
	
	test_list = []
	for test_case in test_case_list:
		# merge all client's log of PLT on same test_case
		merged_client_data = merge_Client_PLT("../data/"+test_case+"/")
		
		# sort by timestamp
		sorted_merge_data = sort_by_timestamp(merged_client_data)
		sorted_merge_data.timestamp = sorted_merge_data.timestamp.astype(int)


		# collect valid 10 test set
		result_dict = collect_valid_test_result(sorted_merge_data)
		# reasseamble splited dictionary to pandas dataframe. (result_dict -> pandas)
		valid_testset = reassemble_data(result_dict)

		test_list.append(valid_testset)

	#visualize_and_analyze(test_list[0], test_list[1], test_list[2])
	visualize_and_analyze(test_list[0], test_list[1], test_list[2], test_list[3])



	"""data = merge_Client_PLT("h1_5_h2_5_del_200/")
	test_data = sort_by_timestamp(data)
	h1_5_h2_5 = reassemble_data(test_data)
	print(h1_5_h2_5)
	print("-------------------------")


	data = merge_Client_PLT("h1_0_h2_10_del_200/")
	test_data = sort_by_timestamp(data)
	print(test_data)
	h1_0_h2_10 = reassemble_data(test_data)
	print(h1_0_h2_10)
	print("-------------------------")

	visualize_and_analyze(h1_5_h2_5,h1_0_h2_10)"""

if __name__ == "__main__":
	main()