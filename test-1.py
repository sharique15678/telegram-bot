import requests

def fetchData(channel='sharique156789testingfrweewr', post='10'):
	global postValid
	try:
		r = requests.get('https://t.me/'+channel+'/'+post+'?embed=1', verify=False, timeout=20)
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
print(fetchData())