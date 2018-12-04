import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def vs_ttfb_by_test_case(ttfb_for_vs, fileName):
	fig = plt.figure()
	ax = sns.boxplot(x = "protocol_ratio", y = "ttfb", hue="protocol", data = ttfb_for_vs, palette="PRGn")
	ax.set_title(title)
	#ax.set_ylim([500,1500])
	ax.set_ylabel("PLT(ms)")
	ax.set_xlabel("Ratio Of Protocol")
	#sns.despine(offset = 10, trim= True)
	fig.savefig('../graph/'+fileName)
	plt.show()

def vs_networktime_by_test_case(ttfb_for_vs, fileName):
	fig = plt.figure()
	ax = sns.boxplot(x = "protocol_ratio", y = "networkTime", hue="protocol", data = ttfb_for_vs, palette="PRGn")
	#ax.set_title(title)
	#ax.set_ylim([250, 600])
	#ax.set_xticks(["H1:0\nH2:10","H1:3\nH2:7","H1:5\nH2:5","H1:7\nH2:3","H1:10\nH2:0"])
	ax.set_ylabel("Object Downloading Time(ms)")
	ax.set_xlabel("Ratio Of Protocol")
	#sns.despine(offset = 10, trim= True)
	fig.savefig('../graph/'+fileName)
	#plt.show()

def vs_renderingtime_by_test_case(ttfb_for_vs, fileName):
	fig = plt.figure()
	ax = sns.boxplot(x = "protocol_ratio", y = "renderingTime", hue="protocol", data = ttfb_for_vs, palette="PRGn")

	#ax.set_ylim([500,1500])
	ax.set_ylabel("PLT(ms)")
	ax.set_xlabel("Ratio Of Protocol")
	#sns.despine(offset = 10, trim= True)
	fig.savefig('../graph/'+fileName)
	#plt.show()

def vs_plt_by_test_case(ttfb_for_vs, fileName):
	ttfb_for_vs['plt_s'] = ttfb_for_vs['plt']/1000
	ttfb_for_vs = ttfb_for_vs.replace({'protocol':{'http1':'HTTP/1.1', 'http2':'HTTP/2'}})
	#ttfb_for_vs = ttfb_for_vs.replace({'protocol_ratio':{'h1_0_h2_10':'H1:0\nH2:10', 'h1_3_h2_7':'H1:3\nH2:7', 'h1_5_h2_5':'H1:5\nH2:5', 'h1_7_h2_3':'H1:7\nH2:3', 'h1_10_h2_0':'H1:10\nH2:0'}})
	ttfb_for_vs = ttfb_for_vs.replace({'protocol_ratio':{'h1_0_h2_10':1, 'h1_3_h2_7':2, 'h1_5_h2_5':3, 'h1_7_h2_3':4, 'h1_10_h2_0':5}})
	fig = plt.figure()
	ax = sns.boxplot(x = "protocol_ratio", y = "plt_s", hue="protocol", data = ttfb_for_vs, palette="PRGn")
	ax.set_ylim([0,35])
	#ax.axvline(2,linestype = '--')
	print(ttfb_for_vs)
	ax.set_ylabel("PLT(sec)")
	ax.set_xlabel("Ratio Of Protocol")
	#ax.legend(bbox_to_anchor = (0.225, 0.15))
	#sns.despine(offset = 10, trim= True)
	plt.subplots_adjust(bottom = 0.15)
	plt.gca().legend().set_title('')
	plt.axvline(x = 0.5, color = "gray", linestyle = '--')
	plt.axvline(x = 1.5, color = "gray", linestyle = '--')
	plt.axvline(x = 2.5, color = "gray", linestyle = '--')
	plt.axvline(x = 3.5, color = "gray", linestyle = '--')
	plt.xticks([0,1,2,3,4], ['H1:0\nH2:10','H1:3\nH2:7','H1:5\nH2:5', 'H1:7\nH2:3','H1:10\nH2:0'])
	fig.savefig('../graph/'+fileName)
	plt.show()

def main():
	ttfb_for_vs = pd.read_csv("../data/ebay/del_10_plr_1_ebay_data_for_vs.csv")
	#vs_networktime_by_test_case(ttfb_for_vs,"Network Time of http1/http2 when multi-user = 10 on Delay = 100ms")
	#ttfb_for_vs = pd.read_csv("../data/ebay/default_sp_data_for_vs.csv")
	fileName = "ebay/del_10_plr_1_ebay_plt.png"
	vs_plt_by_test_case(ttfb_for_vs, fileName)
	#fileName = "ebay/del_150_ebay_rendering.png"
	#vs_renderingtime_by_test_case(ttfb_for_vs, fileName)
	#fileName = "ebay/del_150_ebay_network.png"
	#vs_networktime_by_test_case(ttfb_for_vs, fileName)



if __name__ =="__main__":
	main()