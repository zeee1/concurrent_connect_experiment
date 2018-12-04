import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def preprocess_by_plr():
	result = pd.DataFrame()
	filePath_list = ["plr_1_ebay_data_for_vs.csv","plr_2_ebay_data_for_vs.csv","plr_3_ebay_data_for_vs.csv","plr_4_ebay_data_for_vs.csv","plr_5_ebay_data_for_vs.csv"]
	data_path = "../data/ebay/"
	test_case = "h1_5_h2_5"

	for filePath in filePath_list:
		path = data_path+filePath

		data = pd.read_csv(path)
		test_case_data = data.loc[data['test_case'] == test_case,]
		loss_rate = filePath[0:5]
		loss_rate = loss_rate[-1:]
		test_case_data['packet_loss_rate'] = loss_rate+"%"

		result = result.append(test_case_data, ignore_index = True)
	
	return result

def vs_networktime_by_test_case(data_for_vs):
	fig = plt.figure()
	ax = sns.boxplot(x = "packet_loss_rate", y = "networkTime", hue="protocol", data = data_for_vs, palette="PRGn")
	#ax.set_title(title)
	ax.set_ylim([300,600])
	ax.set_ylabel("Object Downloading Time(ms)")
	ax.set_xlabel("Packet Loss rate")
	#sns.despine(offset = 10, trim= True)
	
	plt.show()

def main():
	data_for_vs = preprocess_by_plr()
	#print(data_for_vs)
	vs_networktime_by_test_case(data_for_vs)
	return 1

if __name__ == "__main__":
	main()