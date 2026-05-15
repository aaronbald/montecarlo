import numpy as np
from .bitstring import BitString
from .ising import IsingHamiltonian


class MonteCarlo:

    def __init__(self, ham: IsingHamiltonian):
        self.ham = ham       # storing hamiltonian
        self.N = ham.N       # number of spin sites

    def run(self, T: float, n_samples: int, n_burn: int = 100):
        
        bs = BitString(self.N)   # random starting bitstring configuration 
        bs.set_config(list(np.random.randint(0, 2, self.N)))  # randomly initialize spins
        currentE = self.ham.energy(bs)    # initial eneegy 

        for _ in range(n_burn): # burning values that dont affect real probability 
            for i in range(self.N):    # loop over every spin site
                bs.flip_site(i)
                proposedE = self.ham.energy(bs)  # energy of flipped state 
                dE = proposedE - currentE         # difference in energy between proposed and current 

                if dE <= 0:
                    currentE = proposedE           # always accept lower energy
                else:
                    r = np.random.random()
                    if r < np.exp(-dE / T):
                        currentE = proposedE       # accept higher energy probabilistically
                    else:
                        bs.flip_site(i)       # reject and flip spin 

        E_samples = np.zeros(n_samples)     # arrays to store samples 
        M_samples = np.zeros(n_samples)

        for idx in range(n_samples):   # loop over samples 
            for i in range(self.N):
                bs.flip_site(i)
                proposedE = self.ham.energy(bs)   # same thing calculating proposed energy and comparing to current 
                dE = proposedE - currentE

                if dE <= 0:
                    currentE = proposedE
                else:
                    r = np.random.random()
                    if r < np.exp(-dE / T):
                        curr_E = prop_E
                    else:
                        bs.flip_site(i)      

            E_samples[idx] = curr_E
            M_samples[idx] = bs.on() - bs.off()   # up spins minus down spins

        return E_samples, M_samples