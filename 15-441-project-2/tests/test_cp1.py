from __future__ import print_function

import subprocess
from scapy.all import *
import pwd
import os
from fabric import Connection
import time
import socket

PCAP = '/home/ubuntu/environment/cmutcp-starter-code/15-441-project-2/tests/test.pcap'

FIN_MASK = 0x2
ACK_MASK = 0x4
SYN_MASK = 0x8

TIMEOUT = 3

"""
These tests assume there is only one connection in the PCAP
and expects the PCAP to be collected on the server.
All of the basic tests pass on the starter code, without
you having to make any changes. You will need to change these
tests as you add functionality to your implementation.
"""

HOST_PORT = 1234
TESTING_HOST_PORT = 15441

# we can make CMUTCP packets using scapy
class CMUTCP(Packet):
    name = "CMU TCP"
    fields_desc=[IntField("identifier",15441),
                 ShortField("source_port",HOST_PORT),
                 ShortField("destination_port",TESTING_HOST_PORT),
                 IntField("seq_num",0),
                 IntField("ack_num",0),
                 ShortField("hlen",25),
                 ShortField("plen",25),
                 ByteEnumField("flags" , 0,
                      { FIN_MASK: "FIN",
                        ACK_MASK: "ACK" ,
                        SYN_MASK: "SYN" ,
                        FIN_MASK | ACK_MASK: "FIN ACK",
                        SYN_MASK | ACK_MASK: "SYN ACK"} ),
                 ShortField("advertised_window",1),
                 ShortField("extension_length",0),
                 StrLenField("extension_data", None,
                            length_from=lambda pkt: pkt.extension_length)]

    def answers(self, other):
        return (isinstance(other, CMUTCP))

def test_pcap_packets_max_size():
    """Basic test: Check packets are smaller than max size"""
    print("Running test_pcap_packets_max_size()")
    print("Please note that it's now testing on a sample test.pcap file. "
          "You should generate your own pcap file and run this test.")
    packets = rdpcap(PCAP)
    if len(packets)<=10:
         print("Test Failed")
         return
    for pkt in packets:
        if CMUTCP in pkt:
            if len(pkt[CMUTCP]) > 1400:
                print("Found packet with length greater than max size")
                print("Test Failed")
                return
    print("Test passed")

def test_pcap_acks():
    """Basic test: Check that every data packet sent has a corresponding ACK
    Ignore handshake packets.
    """
    print("Running test_pcap_acks()")
    print("Please note that it's now testing on a sample test.pcap file. "
          "You should generate your own pcap file and run this test.")
    packets = rdpcap(PCAP)
    if len(packets)<=10:
        print("Test Failed")
        return
    seq_nums = []
    ack_nums = []
    for pkt in packets:
        if CMUTCP in pkt:
            # ignore handshake packets, should test in a different test
            if (pkt[CMUTCP].flags == 0):
                seq_nums.append(pkt[CMUTCP].seq_num)
            elif (pkt[CMUTCP].flags == ACK_MASK):
                ack_nums.append(pkt[CMUTCP].ack_num-1)
    # probably not the best way to do this test!
    if set(seq_nums) == set(ack_nums):
        print("Test Passed")
    else:
        print("Test Failed")

# this will run try to run the server and client code
def test_run_server_client():
    """Basic test: Run server and client, and initiate the file transfer process."""
    print("Running test_run_server_client()")
    start_server_cmd = 'tmux new -s pytest_server -d /home/ubuntu/environment/cmutcp-starter-code/15-441-project-2/server'
    start_client_cmd = 'tmux new -s pytest_client -d /home/ubuntu/environment/cmutcp-starter-code/15-441-project-2/client'
    start_mitm_cmd = 'tmux new -s pytest_mitm -d /home/ubuntu/environment/cmutcp-starter-code/15-441-project-2/utils/mitm'
    stop_server_cmd = 'tmux kill-session -t pytest_server'
    stop_client_cmd = 'tmux kill-session -t pytest_client'
    stop_mitm_cmd = 'tmux kill-session -t pytest_mitm'

    failed = False
    
    try:
        os.system(start_mitm_cmd)
        os.system('tmux has-session -t pytest_mitm')
        os.system(start_client_cmd)
        os.system('tmux has-session -t pytest_client')
        os.system(start_server_cmd)
        os.system('tmux has-session -t pytest_server')
        # exit when server finished receiving file
        os.system('while tmux has-session -t pytest_server; do sleep 1; done')
    except:
        failed = True
    finally:
        try:
            os.system(stop_client_cmd)
        except Exception as e:
            pass # Ignore error here that may occur if client already shut down
        try:
            os.system(stop_server_cmd)
        except Exception as e:
            pass # Ignore error here that may occur if server already shut down
        try:
            os.system(stop_mitm_cmd)
        except Exception as e:
            pass # Ignore error here
        if failed:
            print("Test failed")
        else:
            print("Test passed") 

            
def test_basic_reliable_data_transfer():
    """Basic test: Check that when you run server and client starter code
    that the input file equals the output file
    """
    # Can you think of how you can test this? Give it a try!
    pass

def test_basic_retransmit():
    """Basic test: Check that when a packet is lost, it's retransmitted"""
    # Can you think of how you can test this? Give it a try!
    pass

if __name__=='__main__':
     test_pcap_packets_max_size()
     test_pcap_acks()
     test_run_server_client()
