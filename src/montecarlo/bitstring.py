import numpy as np
import math      
import copy as cp       


class BitString:
    """
    Simple class to implement a config of bits
    """
    def __init__(self, N):
        self.N = N
        self.config = np.zeros(N, dtype=int) 

    def __repr__(self):
        out = ""
        for i in self.config:
            out += str(i)
        return out

    def __eq__(self, other):        
        return all(self.config == other.config)
    
    def __len__(self):
        return len(self.config)

    def on(self):
        """
        Return number of bits that are on
        """
        on = sum(self.config == 1)
        return on 

    def off(self):
        """
        Return number of bits that are off
        """
        off = sum(self.config == 0)
        return off

    def flip_site(self,i):
        """
        Flip the bit at site i
        """
        if i >= 0 and i < self.N:    # index has to be positive or zero and less than n which is number of digits
            self.config[i] = 1 - self.config[i]  # if 1: 1-1=0,  if 0: 1-0=1  both are flipped 
        else:
            print("Index out of bounds")  # index would either be negative or greater than length of bitsring
    
    def integer(self):
        """
        Return the decimal integer corresponding to BitString
        """
        decInt = 0   # initializing variable 
        for i in range(self.N):   # for each digit in bitstring, multiplies it by 2 set to correct exponent to get integer
            decInt += self.config[i] * (2**(self.N - 1 - i))
        return decInt
    

    def set_config(self, s:list[int]):
        """
        Set the config from a list of integers
        """
        len(s) == self.N  # length is just equal tp total number of digits 
        self.config = np.array(s)  # stores list of integers as configured as bitstring 


    def set_integer_config(self, dec:int, digits: int = None):
        """
        convert a decimal integer to binary
    
        Parameters
        ----------
        dec    : int
            input integer
            
        Returns
        -------
        Bitconfig
        """
        if digits is None: # digits is optional so if not provided just use imported number of digits
            length = self.N
        else: 
            length = digits  # if digits is provided use integer 
        
        if dec < 2**length:  # verifying that the integer if less than the max binary value based on bitstring length
            binary = bin(dec) # converts decimal to binary
            binary = binary[2:]  # removes first 2 characters which are ob 
            binary = binary.zfill(length)  # fills the front of the binary string with zeroes until it is t he right length
            self.config = np.array([int(b) for b in binary]) # takes binary string and converts it into an array of digits
        else: print ("The integer is too big") 