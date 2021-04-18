import requests
import threading
import sys

max = threading.Semaphore(value=5) # Decrease this value if you encount problems with your cpu/ram usage.
threads = []
list = open('http_proxies.txt', 'r')
proxies = list.readlines()
list.close()

def fetchData(channel='google', post='1', proxy=None):
	global postValid
	try:
		r = requests.get('https://t.me/'+channel+'/'+post+'?embed=1', verify=False, timeout=20, proxies={'https':proxy})
		cookie = r.headers['set-cookie'].split(';')[0]
		key = r.text.split('data-view="')[1].split('"')[0]
		if 'stel_ssid' in cookie: 
			return {'key':key,'cookie':cookie}
		else:
			return False
	except Exception as e:
		if str(e) == "list index out of range":
			print(f"Post {post} is not exist")
			postValid = False
		return False
		
def addViewToPost(channel='google', post='1', key=None, cookie=None, proxy=None):
	try:
		r = requests.get('https://t.me/v/?views='+key, timeout=40, headers={
		'x-requested-with':'XMLHttpRequest',
		'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
		'referer':'https://t.me/'+channel+'/'+post+'?embed=1',
		'cookie':cookie}, proxies={'https':proxy}
		)
		return r.text
	except Exception as e:
		return False
		
def run(channel, post, proxy):
	max.acquire()
	s = fetchData(channel, post, 'http://'+proxy)
	if (type(s) is dict):
		l = addViewToPost(channel, post, s['key'], s['cookie'], 'http://'+proxy)
		if l != False: print('Proxy '+proxy+' finished its job successfully!')
	max.release()
	print('Thread with proxy '+proxy+' has been terminated.')



channelName = sys.argv[1]
postStart = int(sys.argv[2])
postValid = True

for post in range(postStart, postStart + 1000):
	if postValid == False:
		break
	for proxy in proxies:
		if postValid == False:
			break
		p = proxy.split('\n')[0]
		thread = threading.Thread(target=run,args=(channelName, str(post), p))
		# thread = threading.Thread(target=run,args=("newtestpython","7",p))
		threads.append(thread)
		thread.start()
		print('Started new thread with proxy '+p)

for t in threads:
	t.join()

print("End")