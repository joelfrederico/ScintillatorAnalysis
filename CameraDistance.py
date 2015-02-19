#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mytools as mt
import argparse
from common_functions import *

# ====================================
# Close all plots (for iPython)
# ====================================
plt.close('all')

# ====================================
# Define FOV for GigE and Hamamatsu
# ====================================
h_obj      = 30e-2
h_img_GigE = -5.27e-3
h_img_Ham = -13e-3

# ====================================
# Get magnifications
# ====================================
m_GigE = mag(h_img_GigE,h_obj)
m_Ham  = mag(h_img_Ham,h_obj)

# ====================================
# Get object distance as a
# fxn of focal length
# ====================================
f_cont      = np.linspace(10,85,100)*1e-3
o_cont_GigE = obj(f_cont,m_GigE)
o_cont_Ham  = obj(f_cont,m_Ham)

f_list      = np.array([20,24,28,35,50,60,85])*1e-3
o_list_GigE = obj(f_list,m_GigE)
o_list_Ham  = obj(f_list,m_Ham)

# ====================================
# Plot results
# ====================================
fig = plt.figure()
gs  = gridspec.GridSpec(1,1)
ax  = fig.add_subplot(gs[0,0])

plt1 = ax.plot(f_cont/1e-3,o_cont_GigE,'b-',label='_GigE')
plt2 = ax.plot(f_list/1e-3,o_list_GigE,'b-o',label='GigE')

plt3 = ax.plot(f_cont/1e-3,o_cont_Ham,'r-',label='_Ham')
plt4 = ax.plot(f_list/1e-3,o_list_Ham,'r-o',label='Hamamatsu')

mt.addlabel(axes=ax,xlabel='Focal Length [mm]',ylabel='Object distance [m]',toplabel='Distance to Screen')

gs.tight_layout(fig)

ax.legend(loc=0)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Creates a plot of object length vs. focal length.')
    parser.add_argument('-v','--verbose',action='store_true',
            help='enable verbose mode')
    parser.add_argument('-o','--output',action='store_true',
            help='save file')

    arg=parser.parse_args()

    if arg.output:
        fig.savefig('Distance_to_Screen.pdf')
    
    plt.show()
