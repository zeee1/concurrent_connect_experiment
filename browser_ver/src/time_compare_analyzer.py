import pandas as pd

def time_analyzer(_filePath):
	data = pd.read_csv(_filePath)
	test_case = ["h1_0_h2_10", "h1_3_h2_7", "h1_5_h2_5", "h1_7_h2_3", "h1_10_h2_0"]

	for tc in test_case:
		print(" * Test Case : ", tc)
		data_on_tc = data.loc[data['protocol_ratio'] == tc, ]
		http1_data = data_on_tc.loc[data_on_tc['protocol'] == 'http1',]
		http2_data = data_on_tc.loc[data_on_tc['protocol'] == 'http2',]

		median_nt_http1 = http1_data['plt'].median()
		median_nt_http2 = http2_data['plt'].median()

		print("Median Network Time of HTTP1 : ", median_nt_http1, " ms")
		print("Median Network Time of HTTP2 : ", median_nt_http2, " ms")

		if median_nt_http1 < median_nt_http2:
			diff = median_nt_http2 - median_nt_http1
			print("Time gap : ", diff)
			print("NT of HTTP1 < NT of HTTP2 : ",diff/median_nt_http1*100,"%")
		else:
			diff = median_nt_http1 - median_nt_http2
			print("Time gap : ", diff)
			print("NT of HTTP1 > NT of HTTP2 : ",diff/median_nt_http2*100,"%")

		print("--------------------------------------------------------------------------")


def main():
	filePath = "../data/ebay/del_200_plr_1_ebay_data_for_vs.csv"
	time_analyzer(filePath)

if __name__ == "__main__":
	main()