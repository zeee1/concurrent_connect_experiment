#!/usr/bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import os
import netifaces as ni
import browsermobproxy as mob
import subprocess
import signal



def measure_plt(url, protocol,dump_file_name):
	cmd = "sudo tcpdump -i enp0s10 -w "+dump_file_name

	pro = subprocess.Popen(cmd.split(), stdout = subprocess.PIPE)
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument('headless')
	chrome_options.add_argument('window-size=1920x1080')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
	#chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
	driver = webdriver.Chrome("/home/minjiwon/browser_concurrent_connect/chromedriver/chromedriver",chrome_options=chrome_options)
	#driver = webdriver.Chrome("/home/minjiwon/Documents/concurrent_connect_expriment/browser_ver/linux_driver/chromedriver",chrome_options=chrome_options)

	ts = round(time.time())
	driver.get(url)
	#print(driver.page_source)
	time.sleep(5)
	result_df = pd.DataFrame()

	navigationstart_ts = "return performance.timing.navigationStart;"
	fetchstart_ts = "return performance.timing.fetchStart;"
	requeststart_ts = "return performance.timing.requestStart;"
	responsestart_ts = "return performance.timing.responseStart;"
	domloading_ts = "return performance.timing.domLoading;"
	responseend_ts = "return performance.timing.responseEnd;"
	loadeventend_ts = "return performance.timing.loadEventEnd;"

	navigationstart_ts = driver.execute_script(navigationstart_ts)
	fetchstart_ts = driver.execute_script(fetchstart_ts)
	requeststart_ts = driver.execute_script(requeststart_ts)
	responsestart_ts = driver.execute_script(responsestart_ts)
	domloading_ts = driver.execute_script(domloading_ts)
	responseend_ts = driver.execute_script(responseend_ts)
	loadeventend_ts = driver.execute_script(loadeventend_ts)

	plt = loadeventend_ts - navigationstart_ts
	nt = responseend_ts - fetchstart_ts
	rt = loadeventend_ts - domloading_ts

	loading_ts = {'navigationstart_ts' : navigationstart_ts, 'fetchstart_ts' : fetchstart_ts, 'requeststart_ts':requeststart_ts,
	'responsestart_ts':responsestart_ts,'domloading_ts':domloading_ts,'responseend_ts':responseend_ts,'loadeventend_ts':loadeventend_ts,'plt':plt,'networkTime':nt,'computationTime':rt,'ttfb':(responsestart_ts - navigationstart_ts), 'timestamp':ts, 'protocol':protocol}
	result_df = result_df.append(loading_ts, ignore_index=True)

	driver.quit()
	os.killpg(os.getpgid(pro.pid), signal.SIGTERM) 
	return result_df
	
def main():
	#http1_url = "https://opendata.cnu.ac.kr:80/pageLoadTest/test_50kb.html"
	#http2_url = "https://opendata.cnu.ac.kr:443/pageLoadTest/test_50kb.html"
	http2_url = "https://opendata.cnu.ac.kr:443/alexa_top/ebay/ebay.html"

	local_ip = ni.ifaddresses('enp0s10')[ni.AF_INET][0]['addr']
	splited_ip = local_ip.split('.')
	client_id = splited_ip[len(splited_ip)-1]
	ts = round(time.time())

	dump_file_name = client_id+"_"+str(ts)+"_dump_h2.dump"
	data = measure_plt(http2_url, "http2", dump_file_name)

	#fileDir = "/home/minjiwon/browser_concurrent_connect/data/ebay_plt_data/del_200_plr_5/h1_5_h2_5/"
	#fileName = client_id+"_http1_plt.csv"
	#filePath = fileDir+fileName

	"""if os.path.isfile(filePath):
		with open(filePath, 'a') as f:
			data.to_csv(f, header = False)
	else:
		data.to_csv(filePath)"""


if __name__ == "__main__":
	main()
