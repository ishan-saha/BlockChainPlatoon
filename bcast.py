from socket import *

class BroadCastReceiver:
    """ This class is to start a bcast reveiver that starts on port 9090 and returns address and the data reveived form the listner. 
    this class is built to keep this loop and iteration friendly """

    def __init__(self,port=9090,msg_length=2048):
        # setting up a constructor with default message length to expect for 
        # setting up a UDP socket
        self.SOCKET=socket(AF_INET,SOCK_DGRAM)
        # making the socket reusable
        self.SOCKET.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        # binding the socket for port 9090 on all interfaces
        self.SOCKET.bind(("",port))
        #setting the msg length
        self.msg_length=msg_length
    
    def __iter__(self):
        # returns the current object for iteration
        return self
    
    def __next__(self):
        # try to fetch the data and return the data + sender_address if the final step the close with stopiteration 
        try:
            address, data = self.SOCKET.recvfrom(self.msg_length)
            return (address, data)
        except Exception as e:
            print(e)
            raise StopIteration
    
    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_value, traceback):
        # the destructor to make the socket reusable again
        self.SOCKET.close()