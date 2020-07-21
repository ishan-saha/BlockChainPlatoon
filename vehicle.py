#!/usr/bin/env python3

# importing all the libraries needed
import socket
import time
import random
import bcast
import blockchain

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# this is a sample vehicle with the following ID and port number for communication
print("[!] Setting up the values ;)")
ID = ("Vehicle-"+str(random.randint(1,999)),)
platoon = list()
chain=list()
temp =''
# this is the Server ip address and port, broadcast and the receiver and self IP Addr
SERVER = ('vehicleserver.domain.name',9090) # add vehicleserver.domain.name to the /etc/hosts file for the vehicle OS corrosponding to the ip of the server
BROADCAST = ("255.255.255.255",9092)
ME = (get_ip(),9091)
Receiver=bcast.BroadCastReceiver(9092)

# sending to the broadcast server about the veicle-ID after setting up a UDP socket and receiving the platoon
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as SOCKET:
    print("[!] Sent the ID to the server!")
    SOCKET.sendto(ID[0].encode(),SERVER)
    SOCKET2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    SOCKET2.bind(ME)
    temp = SOCKET2.recvfrom(2048)
    print('[!] Received the peers from the server :)')
    SOCKET2.close()
    SOCKET.close()

# fetching all the platoon data
for x in temp[0].decode().split("|"):
    platoon.append(x.split(":"))

# start time
start = time.time()
print('[!] Started the chain! :)')
# initiating the chain

NewChain = blockchain.Chain()

# creating the genesis block with the ips and all as the transaction detials
NewChain.add_block(temp[0].decode())
print('[!] Yay! Made the first block!')
# geting the copy of the chain
chain=NewChain.ret_chain()

Sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # socket for sending the data
Sender.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) # to send msg to broadcast otherwise UDP socket cant send to broadcast

speedlist=[]

for count in range(5):
    # this will set the speed to random integer between the given range
    # we need to create only 5 as the peer network is of 5 only
    Speed = str(random.randint(50,80))
    if platoon[count][0]==ID[0]: 
        # if it is this machines trun then it will make a block and send it
        # it will use the speed variable that is random as the transaction detail
        print('[!] Just sent my Speed to the peers! I am speed! ;D')
        speedlist.append(Speed)
        NewChain.add_block(Speed)
        time.sleep(1)
        Sender.sendto(ID[0].encode()+b":"+NewChain.ret_chain()[-1],BROADCAST)
    else:
        # it will wait for other peers to send the block and them mine the data
        # the speed will be stored in the list
        print('[!] Waiting for my peers!')
        for block, addr in Receiver:
            speedlist.append(NewChain.validated_block(block.split(":")[-1]))
            print("[!] Just added another block to the chain!")
            break

platoon_leader=platoon[speedlist.index(max(speedlist))][0]

# adding the last 7th block having the platoon leader information 
NewChain.add_block("The platoon leader is"+platoon_leader)
chain=NewChain.ret_chain()

# end time 
end=time.time()

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as SOCKET:
    SOCKET.sendto(ID[0].encode()+b":leader|"+str(end-start-5).encode(),SERVER)
    SOCKET.close()

with open('block.dat','w') as file:
    file.writelines(chain)
print("[!] Bye!")
