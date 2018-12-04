import pandas as pd
from glob import glob

def main():
	data_path = "../data/third/default/"
	test_case_list = ["h1_3_h2_7", "h1_5_h2_5", "h1_7_h2_3"]

	for test_case in test_case_list:
		path = data_path+test_case
		client_log_path_list = glob(path+"/*")
		print(client_log_path_list)

		for client_log in client_log_path_list:
			data = pd.read_csv(client_log)
			(data[['domloading_ts', 'responsestart_ts']]).to_csv("../data/third/default/compare_timestamp.csv")
	return 1

if __name__ == "__main__":
	main()