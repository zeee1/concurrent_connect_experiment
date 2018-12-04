import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import os
import subprocess


def iperf_get_bandwidth(server_ip):
	iperf_cmd = "iperf -c "+server_ip
	proc = subprocess.Popen(iperf_cmd.split(), stdout = subprocess.PIPE)
	out, err = proc.communicate()

	output_str = out.decode()
	output_by_line = output_str.split("\n")
	numeric_data = output_by_line[len(output_by_line)-2]
	numeric_value = numeric_data.split()

	crnt_bandwidth = float(numeric_value[len(numeric_value)-2])
	time.sleep(3)
	return crnt_bandwidth
	
def measure_plt(chromedriver, url, fileDir,index, protocol):
	chromedriver.get(url)
	time.sleep(5)
	result_df = pd.DataFrame()

	pltSC = "return performance.timing.loadEventEnd - performance.timing.navigationStart;"
	ntSC = "return performance.timing.responseEnd - performance.timing.fetchStart;"
	dltSC = "return performance.timing.loadEventEnd - performance.timing.domLoading;"

	plt = chromedriver.execute_script(pltSC)
	nt = chromedriver.execute_script(ntSC)
	dlt = chromedriver.execute_script(dltSC)

	result_df = result_df.append({'plt':plt,'networkTime':nt,'computationTime':dlt}, ignore_index=True)
	fileName = protocol+"_"+str(index)+"_plt.csv"
	filePath = fileDir + fileName
	print(filePath)
	chromedriver.quit()

	result_df.to_csv(filePath)


def main():
	#pool = ProcessPoolExecutor(5)
	http2_url = "https://opendata.cnu.ac.kr:443/pageLoadTest/test_50kb.html"
	http1_url = "https://opendata.cnu.ac.kr:80/pageLoadTest/test_50kb.html"
	server_ip = "168.188.129.94"

	driver_dict = []
	
	first_bandwidth = 62.2
	print("First Bandwidth : ", first_bandwidth)

	test_count = 0
	browser_used = True

	while True:
		if browser_used == True:
			print("Start to load chrome browser...")
			for i in range(0, 30):
				chrome_options = webdriver.ChromeOptions()
				chrome_options.add_argument("--incognito")
				chrome_options.add_argument('headless')
				chrome_options.add_argument('window-size=1920x1080')
				chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
				driver = webdriver.Chrome("../../linux_driver/chromedriver",chrome_options=chrome_options)

				driver_dict.append(driver)
			
			time.sleep(3)
			browser_used = False
			print("Complete loading browsers..")

		crnt_bandwidth = iperf_get_bandwidth(server_ip)
		print("Current Bandwidth : ",crnt_bandwidth)
		
		if abs(crnt_bandwidth - first_bandwidth) < 1:
			print("Start Test")
			test_count += 1
			with concurrent.futures.ThreadPoolExecutor(max_workers = 30) as executor:
				"""for i in range(0, 10):
					executor.submit(measure_plt, driver_dict[i], http1_url, "./client30/h1_10_h2_20_plr_2/test_"+str(test_count)+"/",i, "http1")"""
				for i in range(0, 30):
					executor.submit(measure_plt, driver_dict[i], http2_url, "./client30/h1_0_h2_30_plr_2/test_"+str(test_count)+"/",i, "http2")

			time.sleep(15)
			driver_dict = []
			browser_used = True


		if test_count == 10:
			break
		
		

	

	

if __name__== "__main__":
	main()