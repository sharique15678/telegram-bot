import requests
list = open('Proxy_data.txt', 'r')
proxies = list.readlines()
list.close()

def fetchData(channel='sharique156789testing', post='2'):
    r = requests.get('https://t.me/'+channel+'/'+post +
                     '?embed=1', verify=False, timeout=20)
    cookie = r.headers['set-cookie'].split(';')[0]
    key = r.text.split('data-view="')[1].split('"')[0]
    return {'key':key,'cookie':cookie}

def addViewToPost(channel='sharique156789testing', post='2', key=None, cookie=None):
    r = requests.get('https://t.me/v/?views='+key, timeout=40, headers={
    'x-requested-with':'XMLHttpRequest',
    'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'referer':'https://t.me/'+channel+'/'+post+'?embed=1',
    'cookie':cookie}
    )
    print('https://t.me/v/?views='+key)
    return r.text


for proxy in proxies :
    pass

s = fetchData()
if (type(s) is dict):
    l = addViewToPost(key=s['key'], cookie=s['cookie'])
    if l != False: 
        print(l)
        print('Proxy finished its job successfully!')

