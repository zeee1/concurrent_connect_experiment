from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import browsermobproxy as mob
import json
from urllib.parse import urlparse

BROWSERMOB_PROXY_PATH = "../browsermob-proxy-2.1.4/bin/browsermob-proxy"
test_url = "https://naver.com"

def capture_waterfall_chart():
	server = mob.Server(BROWSERMOB_PROXY_PATH)
	print(server)
	server.start()
	proxy = server.create_proxy()
	#url = urlparse(proxy.proxy).path
	proxy.new_har()

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument('window-size=1920x1080')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
	chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
	driver = webdriver.Chrome("../linux_driver/chromedriver",chrome_options=chrome_options)
	
	#proxy.new_har(test_url, options={'captureHeaders':True})
	driver.get(test_url)
	print(str(proxy.har))
	server.stop()
	driver.quit()

def main():
	capture_waterfall_chart()

if __name__ == "__main__":
	main()