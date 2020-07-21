import hashlib
import base64 

class Block():
    """ This class is to create a block that can be later added to the chain. 
        its not including the time in the hash as the clock sync is not implemented. """
    def __init__(self,I,P,PH,T): 
        self.index = str(I)  
        self.proof = str(P)  
        self.previous_hash = PH  
        self.transaction = T
        self.block=b''

    def Hash(self):
        block_string="{}{}{}{}".format(self.index,self.proof,self.transaction,self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def generate(self):
        temp="|".join((self.index,str(self.previous_hash),self.transaction,self.proof))
        self.block = base64.b64encode(temp.encode()) # just for the sake of proving the point this value is being converted into a base 64 
        return self.block


class Chain:
    """This is to create a chain of the blocks.
    The blocks will be added and then the next logical proof of work will be created.
    The genesis block has hash proof and index value as 0.
    The mine function will be used to mine the block received and will return all the values.
    The values returned from the mine() will be validated and then the block will be added if the values of hash and proof match the current value.
    Once the block has been validated it then will be added to the chain itself.
    Post the addition of the block the block can be fetched after running the ret_chain()[-1]
    """
    def __init__(self):
        self.chain=list()
        self.hashlist=[0]
        self.proof=['0']
        self.index=[0]

    
    @staticmethod
    def proof_of_work(proof):
        """proof of work based of the previous proof .... the new proof must be divisible by 5"""
        temp = int(proof)+1
        while (temp+int(proof)) % 5 != 0:
            temp+=1
        return str(temp)

    def add_block(self,T):
        NewBlock = Block(self.index[-1],self.proof[-1],self.hashlist[-1],T)
        self.chain.append(NewBlock.generate())
        self.hashlist.append(NewBlock.Hash())# this is to create the list of hashes and the last hash will be used to verify the comming block 
        self.index.append(self.index[-1]+1) # this will keep the index updated
        self.proof.append(Chain.proof_of_work(self.proof[-1])) # this will keep the next proof of work ready to check from the new block that will come from other vehicles and can be validated
    
    
    @staticmethod
    def mine(block):
        temp = base64.b64decode(block)
        I, PH, T, P = temp.decode().split("|")
        return int(I), str(PH), T, int(P)
    
    def validated_block(self,block):
        I, PH, T, P = Chain.mine(block)
        if I == int(self.index[-1]) and P == int(self.proof[-1]) and PH == self.hashlist[-1]:
            self.add_block(T)
            return str(T)
        else:
            return False

    def ret_chain(self):
        return self.chain
    def get_current(self):
        print(self.index[-1],self.proof[-1],self.hashlist[-1])
