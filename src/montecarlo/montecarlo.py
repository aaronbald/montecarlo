import numpy as np
from .bitstring import BitString
from .ising import IsingHamiltonian


class MonteCarlo:

    def __init__(self, ham: IsingHamiltonian):
        self.ham = ham       # store the Hamiltonian to call ham.energy()
        self.N = ham.N       # number of spin sites

    def run(self, T: float, n_samples: int, n_burn: int = 100):
        
        # Initialize a random starting configuration
        bs = BitString(self.N)
        bs.set_config(list(np.random.randint(0, 2, self.N)))
        curr_E = self.ham.energy(bs)

        # Burn-in phase: let system equilibrate, discard these steps
        for _ in range(n_burn):
            for i in range(self.N):
                bs.flip_site(i)
                prop_E = self.ham.energy(bs)
                dE = prop_E - curr_E

                if dE <= 0:
                    curr_E = prop_E           # always accept lower energy
                else:
                    r = np.random.random()
                    if r < np.exp(-dE / T):
                        curr_E = prop_E       # accept higher energy probabilistically
                    else:
                        bs.flip_site(i)       # reject: flip back

        # Sampling phase: record E and M at each step
        E_samples = np.zeros(n_samples)
        M_samples = np.zeros(n_samples)

        for idx in range(n_samples):
            for i in range(self.N):
                bs.flip_site(i)
                prop_E = self.ham.energy(bs)
                dE = prop_E - curr_E

                if dE <= 0:
                    curr_E = prop_E
                else:
                    r = np.random.random()
                    if r < np.exp(-dE / T):
                        curr_E = prop_E
                    else:
                        bs.flip_site(i)       # reject: flip back

            # Record current state after sweeping all sites
            E_samples[idx] = curr_E
            M_samples[idx] = bs.on() - bs.off()   # up spins minus down spins

        return E_samples, M_samples