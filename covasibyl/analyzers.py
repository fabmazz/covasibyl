import numpy as np
import matplotlib.pyplot as pl

import sciris as sc
from covasim.analysis import Analyzer


class store_seir(Analyzer):

    def __init__(self, printout=False, *args, **kwargs):
        super().__init__(*args, **kwargs) # This is necessary to initialize the class properly
        self.t = []
        self.S = []
        self.E = []
        self.I = []
        self.R = []
        self.Q = []
        self.IND = []
        self.Efree = []
        self.printout=printout
        return

    def apply(self, sim):
        ppl = sim.people # Shorthand
        self.t.append(sim.t)
        self.S.append(ppl.susceptible.sum())
        self.E.append(ppl.exposed.sum() - ppl.infectious.sum())
        self.I.append(ppl.infectious.sum())
        self.R.append(ppl.recovered.sum() + ppl.dead.sum())
        self.Q.append(ppl.quarantined.sum())
        self.IND.append((ppl.infectious & (~ppl.diagnosed)).sum())  
        self.Efree.append((ppl.exposed & (~ppl.infectious) & (~ppl.diagnosed)).sum() )
        EIfree = self.IND[-1]+self.Efree[-1]
        if (self.printout):
            print(f"day {sim.t} -> I (free): {self.I[-1]} ({self.IND[-1]}),"+\
                f" E+I (free): {self.I[-1]+self.E[-1]} ({EIfree}) R: {self.R[-1]}")      
        return

    def plot(self, **args):
        pl.figure()
        pl.plot(self.t, self.S, label='S')
        pl.plot(self.t, self.E, label='E')
        pl.plot(self.t, self.I, label='I')
        pl.plot(self.t, self.R, label='R')
        pl.legend()
        pl.xlabel('Day')
        pl.ylabel('People')
        sc.setylim() # Reset y-axis to start at 0
        sc.commaticks() # Use commas in the y-axis labels
        return

    def out_save(self):
        
        return np.array(list(zip(self.t, self.S, self.E, self.I, self.R, self.Q, self.IND, self.Efree)),
            dtype=[(i,np.int_) for i in ["t","S","E","I","R", "Q", "nondiag","Enondiag"]])
