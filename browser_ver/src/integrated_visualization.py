import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def vs_integrated_by_test_case(data_for_vs):
	fig = plt.figure()
	ax = sns.boxplot(x = "packet_loss_rate", y = "throughput", hue="delay", data = data_for_vs, palette="PRGn")
	#ax.set_title(title)
	#ax.set_ylim([250, 600])
	ax.set_ylabel("throughput(bit/sec)")
	ax.set_xlabel("Packet Loss Rate(%)")
	#sns.despine(offset = 10, trim= True)
	
	plt.show()

def vs_line_std_of_plt_by_test_case(data_for_vs, xlabel_txt, ylabel_txt):
	delay_list = [10,50, 100, 150, 200]
	label_tup = ()
	marker_list = ['o-', '^-','v-', 's-', '*-' ]
	count = 0
	for delay in delay_list:
		tmp_df = data_for_vs.loc[data_for_vs['delay']==delay,]
		fi_list = []
		loss_rate_list = tmp_df['packet_loss_rate'].drop_duplicates().tolist()
		for plr in loss_rate_list:
			df_by_plr = tmp_df.loc[tmp_df['packet_loss_rate'] == plr,]
			fi_list.append(df_by_plr['fi'].median())

		label_txt = "RTT "+str(delay)+" ms"

		if delay == 10:
			label_txt += " (Wired LAN)"
		elif delay == 100:
			label_txt += " (LTE)"
		elif delay == 150:
			label_txt += " (WiFi)"
		elif delay == 200:
			label_txt += " (3G)"

		plt.plot(tmp_df['packet_loss_rate'].drop_duplicates().tolist(), fi_list,marker_list[count], label = label_txt, linewidth=2.5)
		label_tup = label_tup+(label_txt,)
		count += 1

	plt.xticks([0.1,0.5,1, 3, 5])
	plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
	plt.xlabel(xlabel_txt, fontsize = 15)
	plt.ylabel(ylabel_txt, fontsize = 15)
	plt.ylim(ymin=0.0, ymax = 1.2)
	plt.legend(label_tup)
	plt.savefig("../graph/ebay/jain_fairness_index.png")
	plt.show()

def main():
	data_path = "../data/ebay/jain_fairness_index_for_vs.csv"
	xlabel_txt = "Packet loss rate(%)"
	ylabel_txt = "Fairness Index"
	vs_line_std_of_plt_by_test_case(pd.read_csv(data_path), xlabel_txt, ylabel_txt)

	"""data_path = "../data/ebay/std_compare.csv"
	xlabel_txt = "Packet loss rate"
	ylabel_txt = "Standard deviation of PLT"
	vs_line_std_of_plt_by_test_case(pd.read_csv(data_path), xlabel_txt, ylabel_txt)"""

if __name__ == "__main__":
	main()