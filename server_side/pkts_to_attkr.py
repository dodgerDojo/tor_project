from scapy.all import *
import sys

print "looking for ip: ", sys.argv[1]

while True:
    x = sniff(50)
    for pkt in x:
        if IP in pkt and Raw in pkt and pkt[IP].dst == sys.argv[1]:
            print 'sending...'
            pktdump = PcapWriter("my_packet.pcap", append=False)
            pktdump.write(pkt)
            pkt.show2()
            print 'done!'
            exit()
