from TorCtl import TorCtl
import urllib2
import time
import sys
import csv
import os

import signal
import sys

TARGET_FILE_SIZE_IN_BYTES = 1073741824

PORT = 8003
URL = r'http://ec2-35-162-72-168.us-west-2.compute.amazonaws.com'
FILENAME = r'test.img'
HTTP_GET_REQ = r"{0}:{1}/{2}".format(URL, PORT, FILENAME)

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}

WRITE_DOWN_EVENT = False

def download_file(url):
    file = 'test.img'
    print 'started@@@@@@'
    start = time.time()
    response = urllib2.urlopen(url)
    print 'done@@@@@@@@@'
    CHUNK = 16 * 1024
    with open(file, 'wb') as f:

        dl = 0
        done = 0

        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            dl += len(chunk)
            f.write(chunk)
            done = int(50 * dl / TARGET_FILE_SIZE_IN_BYTES)

            time_passed = (time.time() - start)
            bps = dl//time_passed


            with open('results.csv', 'a') as fp:
                a = csv.writer(fp, delimiter=',')
                data = [[time_passed, bps]]
                a.writerows(data)

            global WRITE_DOWN_EVENT
            if WRITE_DOWN_EVENT:
                print('Handled sigusr1!')
                WRITE_DOWN_EVENT = False
                with open('events.csv', 'a') as fp:
                    a = csv.writer(fp, delimiter=',')
                    data = [[time_passed, bps]]
                    a.writerows(data)



            sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), bps))
            print ''
        print 'total time:', time.time() - start

def _set_urlproxy():
    proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)

def request(url):
    print "url: ", url
    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

def renew_connection():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051)
    conn.send_signal("NEWNYM")
    conn.close()


def signal_handler(signal, frame):
        global WRITE_DOWN_EVENT
        print('Got sigusr1!')
        WRITE_DOWN_EVENT = True

signal.signal(signal.SIGUSR1, signal_handler)
open('results.csv', 'w')
open('events.csv', 'w')
file('client_pid.txt', 'w').write(str(os.getpid()))
renew_connection()
_set_urlproxy()
download_file(HTTP_GET_REQ)
