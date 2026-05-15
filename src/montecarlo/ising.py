import numpy as np
import math
import networkx as nx
from .bitstring import BitString

class IsingHamiltonian:

    def __init__(self, G: nx.Graph):   # getting data from G and setting up empty array for mu values
        self.G = G
        self.N = G.number_of_nodes()
        self.mu = np.zeros(self.N)  
        self.J = np.zeros(self.N)   # have to put this to pass check in monte_carlo file 

    def set_mu(self, mus: np.ndarray):   # fillign out empty array with given mu values 
        self.mu = mus

    def energy(self,bs: BitString):  # same thing as old energy function but had to add self parameter and G is already saved from self function
        """Compute energy of configuration, `bs`

        .. math::
            E = \\left<\\hat{H}\\right>

        Parameters
        ----------
        bs   : Bitstring
        input configuration
        G    : Graph
        input graph defining the Hamiltonian
        Returns
        -------
        energy  : float
        Energy of the input configuration
        """
        E = 0    # initializing energy as zero 
        for i, j, data in self.G.edges(data=True):     # for loop running through every edge and taking each node as well as weights 
            if bs.config[i] == 1:               # checking whether node i is going up or down, then assigning 1(up/1) or -1(down/0) to s
                si = 1
            else:
                si = -1
            if bs.config[j] == 1:             #doing same evaluation as for i node but for j node 
                sj = 1
            else:
                sj = -1
            weight = data['weight']       # doesnt do anythign because weight is 1.0 for all the edges, but if there were varying weights it would factor in for each edge 
            E = E + si * sj * weight                   # does the sigma/sum function by adding calculation at current i and j to all others 

        for i in range(self.N):    # adding in the mu term for the equation 
                if bs.config[i] == 1:
                    si = 1
                else:
                    si = -1
                E += self.mu[i] * si
        return E

    def compute_average_values(self, T: float):  # same as old function, just changed parameters because they are already saved in class, had to update some functions with self
        
        E  = 0.0
        M  = 0.0
        Z  = 0.0
        EE = 0.0
        MM = 0.0

        # Write your function here!
        #k = 1.38064852 * (10**(-23))  # initializing values for beta, number of spins and configurations based on given values
        B = 1 / (T)
        bs = BitString(self.N)  
        numSpins = self.N
        numConfigs = 2**numSpins #number of all possible combinations 

        for i in range(numConfigs): # for loop traversing every possible configuration for the bitstring 
            bs.set_integer_config(i)         # setting configuration and energy using functions already made 
            Energy = self.energy(bs)

            spinUp = 0  
            spinDown = 0
            for j in bs.config:    # for loop traversing bitstrng counting 1s as upward spins and 0s as downward spins 
                if j == 1:
                    spinUp = spinUp + 1
                else:
                    spinDown = spinDown + 1
            magnet = spinUp - spinDown   # M for this configuation based on up/down spins 
            boltz = math.exp(-B * Energy)  # boltzman probability for configuration, can't divide by Z yet
        
            Z = Z + boltz               # add boltzman for this configuration to sum of all to get Z and divide all E and M by Z at the end 
            E  = E  + (boltz * Energy)    # running totals for all initialized values based on equations 
            M  = M  + (boltz * magnet)
            EE = EE + (boltz * (Energy**2))   # squared values used in heat capacity and magneiic susceptibility equations 
            MM = MM + (boltz * (magnet**2))
    
        E  = E  / Z   # dividing all calculated values by Z after loop is done, which should work because every term in each equation is just divided by Z so sum of all divided by Z should be the same thing 
        M  = M  / Z
        EE = EE / Z
        MM = MM / Z

        HC = (EE - E**2) / (T**2)  # calculating Heat capacity and Magnetic Susceptibility based on the given euations 
        MS = (MM - M**2) / T


        return E, M, HC, MS