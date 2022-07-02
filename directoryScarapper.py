import threading
import requests
import time
from queue import Queue


global_Switch = True
q = Queue()
threadCount = 10
URL = 'http://10.11.1.133/'
dirb_common_wordlist = '/usr/share/wordlists/dirb/common.txt'
dirb_big_wordlist = '/usr/share/wordlists/dirb/big.txt'
response_length = 99


def checkURL(url):
    page = requests.get(url)
    if(len(page.text) != response_length):
        print(url + ' - ' + str(len(page.text)))

def process():
    while(global_Switch or (q.qsize != 0)):
        try:
            url = q.get()
            checkURL(url)
        except q.empty:
            print('Queue found empty, sleeping.')
            time.sleep(2)
    print('Ending thread.')

def parser():
    print('Initiating parsing.')
    for line in open(dirb_common_wordlist, 'r', encoding="ISO-8859-1"):
        line = line.strip()
        q.put(str(URL + line))
        #q.put(str(URL + line + '.txt'))
        #q.put(str(URL + line + '.php'))
        #q.put(str(URL + line + '.asp'))
    global_Switch = False
    print('Done Parsing')
    while(q.not_empty):
        print(q.qsize())
        time.sleep(30)

parserThread = threading.Thread(target=parser)
for i in range(threadCount):
    scrapperThread = threading.Thread(target=process)
    scrapperThread.start()
parserThread.start()