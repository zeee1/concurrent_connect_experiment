import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def preprocess_by_plr():
	result = pd.DataFrame()
	filePath_list = ["del_100_ebay_data_for_vs.csv","del_150_ebay_data_for_vs.csv","del_200_ebay_data_for_vs.csv"]
	data_path = "../data/ebay/"
	test_case = "h1_5_h2_5"

	for filePath in filePath_list:
		path = data_path+filePath

		data = pd.read_csv(path)
		test_case_data = data.loc[data['test_case'] == test_case,]
		delay = filePath[0:7]
		delay = delay[-3:]
		test_case_data['delay'] = delay+"ms"

		result = result.append(test_case_data, ignore_index = True)
	
	return result

def vs_networktime_by_test_case(data_for_vs):
	fig = plt.figure()
	ax = sns.boxplot(x = "delay", y = "networkTime", hue="protocol", data = data_for_vs, palette="PRGn")
	#ax.set_title(title)
	ax.set_ylabel("Object Downloading Time(ms)")
	ax.set_xlabel("Delay")
	#sns.despine(offset = 10, trim= True)
	
	plt.show()

def main():
	data_for_vs = preprocess_by_plr()
	#print(data_for_vs)
	vs_networktime_by_test_case(data_for_vs)
	return 1

if __name__ == "__main__":
	main()