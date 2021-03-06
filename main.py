import requests
import threading
import sys
import csv
import urllib3

from time import time,sleep
urllib3.disable_warnings()

max = threading.Semaphore(value=500) # Increase Or Decrease this value according to your cpu/ram usage.
threads = []
list = open('Proxy_data.txt', 'r')
proxies_raw = list.readlines()
list.close()
proxies = []
for proxy in proxies_raw:
    p = proxy.split('\n')[0]
    proxies.append(p)



global channel_list
channel_list = [('Channel ID', "last_post", "views_required")] 
# its just to initialize a variable we will update its value with file later

# some variable to hold values
channel_id = ""
post_id = ""
no_of_views = ""

# function to validate channels and posts
def validate(channel=None,post="1") :
    try :
        r = requests.get('https://t.me/'+channel+'/'+post +'?embed=1', verify=False, timeout=20)
        cookie = r.headers['set-cookie'].split(';')[0]
        key = r.text.split('data-view="')[1].split('"')[0]
        if 'stel_ssid' in cookie: 
            return True
        else :
            return False
    except Exception as e :
        if str(e) == "list index out of range" :
            return False

# functions to take all required information
def get_channel_id() :
    global channel_id
    channel_id = input("Enter Channel ID (Press enter to start immediately) ~> ")
    if channel_id == "":  # if it is blank
        main()
    else:  # if it is any other name
        result = validate(channel_id)
        if result == True :
            channel_id = channel_id
        else :
            print('Invalid Channel Id, Please Try Again!')
            get_channel_id()

def get_post_id() :
    global post_id
    post_id = input("Enter Post ID (Press enter for All Posts) ~> ")
    if post_id == "":  # if it is blank
        post_id = 0
    else:  # if it is any other name
        result = validate(channel=channel_id,post=str(post_id))
        if result == True :
            post_id = int(post_id)
        else :
            print('Invalid post number, Please Try Again!')
            get_post_id()

def get_no_of_views() :
    global no_of_views
    no_of_views = input('Enter Number Of Views Required [number only] ~> ')
    try :
        no_of_views = int(no_of_views)
    except :
        print('Input is Not A number')
        get_no_of_views()

def save_as_csv(data_tuple) :
    global channel_list
    for channel in channel_list[1:] :
        print(channel[0],data_tuple[0])
        if data_tuple[0] == channel[0]:
            print('removed')
            delete_csv(channel) #first remove then update new values
            channel_list.append(data_tuple)
            break
        else:
            channel_list.append(data_tuple)
            break
    if len(channel_list) == 1:
        channel_list.append(data_tuple)    
    print(channel_list)
    channel_list = [t for t in channel_list if t]
    with open('channels_data.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerows(channel_list)

def delete_csv(data_tuple) :
    try :
        channel_list.remove(data_tuple)
    except :
        pass


#functions for views increment
def fetchData(channel='google', post='1', proxy=None):
    try:
        r = requests.get('https://t.me/'+channel+'/'+post+'?embed=1', verify=False, timeout=20, proxies={'https':proxy})
        cookie = r.headers['set-cookie'].split(';')[0]
        key = r.text.split('data-view="')[1].split('"')[0]
        if 'stel_ssid' in cookie:
            return {'key':key,'cookie':cookie}
        else :
            return False
    except Exception as e :
        if str(e) == "list index out of range":
            print(f"Post {post} does not exist")
            return False

def addViewToPost(channel=None, post=None, key=None, cookie=None, proxy=None):
    try:
        r = requests.get('https://t.me/v/?views='+key, timeout=40, headers={
		'x-requested-with':'XMLHttpRequest',
		'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
		'referer':'https://t.me/'+channel+'/'+post+'?embed=1',
		'cookie':cookie}, proxies={'https':proxy}
		)
        return r.text
    except Exception as e :
        return False

def run(channel, post, proxy):
    max.acquire()
    s = fetchData(channel, post, 'http://'+proxy)
    if (type(s) is dict):
        l = addViewToPost(channel, post, s['key'], s['cookie'], 'http://'+proxy)
        if l != False:
            print('Proxy '+proxy+' finished its job successfully!')
    max.release()
    print('Thread with proxy '+proxy+' has been terminated.')

def run_channel(channel,post):
    max.acquire()
    #now get the number of views required for this
    views = int(channel[2])
    if views > len(proxies) :
        print("No of views are More than Proxies. This will Create Problems")
        for proxy in proxies :
            thread = threading.Thread(target=run,args=(channel[0], str(post), proxy))
            threads.append(thread)
            thread.start()
    else :
        for i in range(views) :
            thread = threading.Thread(target=run,args=(channel[0], str(post), proxies[i]))
            threads.append(thread)
            thread.start()
    global last_post
    last_post = post
    max.release()
    print('Thread for post '+str(post)+' has been terminated.')

# here our main program starts
def main() :
    global channel_list
    global last_post
    global invalid_post_flag
    global post
    invalid_post_flag = False
    last_post_flag = False
    post = 0
    with open('channels_data.csv') as f:
        channel_list=[tuple(line) for line in csv.reader(f)] #update with the file
    channel_list = [t for t in channel_list if t] #remove any empty tuple
    while True : #an infinite loop 
        if len(channel_list) < 2 :
            sys.exit("No Channel Data Found!. Exiting...")
        start_time = int(time())
        with open('channels_data.csv') as f:
            channel_list=[tuple(line) for line in csv.reader(f)] #update with the file
        channel_list = [t for t in channel_list if t] #remove any empty tuple
        for channel in channel_list[1:] : #get everything except headers
            last_post = int(channel[1])
            while True :
                post = last_post + 1
                result = validate(channel=channel[0],post=str(post)) # check if it is valid or invalid post
                if result == True:
                    run_channel(channel,post)
                    thread = threading.Thread(target=run_channel,args=(channel,post))
                    threads.append(thread)
                    thread.start()
                else : # if it is invalid post
                    channel_list.append((channel[0],last_post,channel[2]))
                    channel_list.remove(channel)
                    print("All New Posts Were Given Views to channel "+ channel[0] +",All Threads Terminated...")
                    break
            channel_list = [t for t in channel_list if t] 
            with open('channels_data.csv','w') as out:
                csv_out=csv.writer(out)
                csv_out.writerows(channel_list)
        #checking if operation took more than 60 secs
        if int(time()) - start_time > 60:
            pass #do nothing and restart the cycle
        else :
            print("In Hibernation ctrl + C to Quit...")
            sleep(60-(int(time()) - start_time))

def get_and_save_data():
    global channel_list
    try:
        with open('channels_data.csv') as f:
            channel_list=[tuple(line) for line in csv.reader(f)]
        channel_list = [t for t in channel_list if t] #remove any empty tuple
    except: #eception will raise if file is not found
        with open('channels_data.csv','w') as out:
            csv_out=csv.writer(out)
            csv_out.writerows(channel_list)
    #prints External IP of machine for whitelisting
    IP = requests.get('https://api.ipify.org').text
    print('Your IP Is ' + IP + ' Please Whitelist It First...')
    print("press ctrl + C to exit...")
    #get data about channels and save them
    get_channel_id()
    get_post_id()
    get_no_of_views()
    data_tuple = (channel_id,post_id,no_of_views)
    save_as_csv(data_tuple)
    with open('channels_data.csv') as f:
        channel_list=[tuple(line) for line in csv.reader(f)]

get_and_save_data()
# # start execution
main()
