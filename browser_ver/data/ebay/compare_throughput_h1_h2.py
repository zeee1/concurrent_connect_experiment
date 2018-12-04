import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

def vs_compare_throughput(h1_log, h2_log):
	fig = plt.figure(figsize=(7,5))
	ax = fig.add_subplot(111)
	fig.subplots_adjust(left = 0.15)
	
	ax.boxplot([h1_log['throughput'].tolist(), h2_log['throughput'].tolist()])
	ax.set_xticklabels(['HTTP/1.1', 'HTTP/2'])
	ax.set_ylabel("Throughput(bit/s)")
	plt.show()
	return 1

def main():
	resultDF = pd.DataFrame()
	data_path = "./del_100_plr_5/"
	protocol_ratio = "h1_5_h2_5/"
	data_path = data_path+protocol_ratio
	size_of_page = 20971520

	client_log_list = glob(data_path+"*")
	throughput_dictionary = []

	for client_log in client_log_list:
		throughput_info_dict = {}
		fileName = client_log.split("/")[-1:]
		client_ip = fileName[0].split("_")[0]
		data = pd.read_csv(client_log)
		data['throughput'] = size_of_page/(data['plt']/1000)
		data['client_ip'] = client_ip
		throughput_info_dict['avg_throughput'] = data['throughput'].mean()
		throughput_info_dict['std_throughput'] = data['throughput'].std()
		throughput_info_dict['client_ip'] = client_ip
		throughput_dictionary.append(throughput_info_dict)
		resultDF = resultDF.append(data)

	h1_client_list = ['100', '102', '103', '104', '105']
	h2_client_list = ['106', '107', '108', '109', '110']

	min_std_h1 = '103'
	min_std_h2 = '106'

	h1_candidate = resultDF.loc[resultDF['client_ip'] == '103',]
	h2_candidate = resultDF.loc[resultDF['client_ip'] == '106',]

	print("h1 throughput mean : ",h1_candidate['throughput'].mean())
	print("h2 throughput mean : ",h2_candidate['throughput'].mean())

	print("diff: ", h1_candidate['throughput'].mean()- h2_candidate['throughput'].mean())
	print(h1_candidate['throughput'].mean()/h2_candidate['throughput'].mean())

	#vs_compare_throughput(h1_candidate, h2_candidate)

	return 1
if __name__ == "__main__":
	main()