#!/usr/bin/env python3
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
h_lanex    = 35.4e-2
h_img_GigE = -5.27e-3
h_img_Ham  = -13e-3

# ====================================
# Get magnifications
# ====================================
m_GigE = mag(h_img_GigE, h_lanex)
m_Ham  = mag(h_img_Ham, h_lanex)

# ====================================
# Get object distance as a
# fxn of focal length
# ====================================
f_cont      = np.linspace(10, 85, 100)*1e-3
o_cont_GigE = obj(f=f_cont, m=m_GigE)
o_cont_Ham  = obj(f=f_cont, m=m_Ham)

f_list      = np.array([20, 24, 28, 35, 50, 60, 85])*1e-3
o_list_GigE = obj(f=f_list, m=m_GigE)
o_list_Ham  = obj(f=f_list, m=m_Ham)

# ====================================
# Plot results
# ====================================
figs         = np.empty(2, dtype=object)
savepaths    = np.empty(2, dtype=object)
savepaths[0] = 'figs/Distance_to_Screen.pdf'

fig     = plt.figure()
figs[0] = fig
gs      = gridspec.GridSpec(1, 1)
ax      = fig.add_subplot(gs[0, 0])

plt1 = ax.plot(f_cont/1e-3, o_cont_GigE, 'b-', label='_GigE')
plt2 = ax.plot(f_list/1e-3, o_list_GigE, 'b-o', label='GigE')

plt3 = ax.plot(f_cont/1e-3, o_cont_Ham, 'r-', label='_Ham')
plt4 = ax.plot(f_list/1e-3, o_list_Ham, 'r-o', label='Hamamatsu')

mt.addlabel(axes=ax, xlabel='Focal Length [mm]', ylabel='Object distance [m]', toplabel='Distance to Screen')

gs.tight_layout(fig)

ax.legend(loc=0)

# ====================================
# Get object FOV as a
# fxn of distance from object
# for GigE
# ====================================
savepaths[1] = 'figs/FOV_of_Screen.png'
fig          = plt.figure()
figs[1]      = fig

ax = fig.add_subplot(gs[0, 0])

o_cont = np.linspace(0.5, 4, 100)
f = 50e-3
# h = -h_img_GigE * o_cont / img(f=f, o=o_cont)
h = h_obj(f=f, o=o_cont, h_img = h_img_GigE)

o_ideal_Ham = obj(f=f, m=m_Ham)

o_likely_GigE = 6.0 * 12.0 * 2.54e-2/1.0
h_likely_GigE = h_obj(f=f, o=o_likely_GigE , h_img = h_img_GigE)

plt1 = ax.plot(o_cont, h, label='GigE Setup')
plt2 = ax.plot(o_ideal_Ham, h_lanex, 'g-o', label='_Ideal Hamamatsu Setup')
plt3 = ax.plot(o_likely_GigE, h_likely_GigE, 'r-o', label='_Likely GigE Setup')

plt.annotate(
    s='Ideal Hamamatsu',
    xy=(o_ideal_Ham, h_lanex), xytext = (20, 20),
    textcoords = 'offset points',
    arrowprops = dict(arrowstyle = '-|>', connectionstyle = 'arc3,rad=0', relpos = (0, 0)))
plt.annotate(
    s='Likely GigE Setup',
    xy=(o_likely_GigE, h_likely_GigE), xytext = (20, -20),
    textcoords = 'offset points',
    arrowprops = dict(arrowstyle = '-|>', connectionstyle = 'arc3,rad=0', relpos = (0, 1)))


mt.addlabel(axes=ax, xlabel='Object Distance (Distance to Screen) [m]', ylabel='Object Height [m]', toplabel='Field of View for GigE with 50mm Lens')

gs.tight_layout(fig)
ax.legend(loc=0)

print('Likely GigE Setup: {} m object, {} m FOV'.format(o_likely_GigE, h_likely_GigE))
print('Likely GigE Setup: {} ft object, {}" FOV'.format(o_likely_GigE * 1.0/2.54e-2 * 1.0/12.0, h_likely_GigE * 1.0/2.54e-2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a plot of object length vs. focal length.')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='enable verbose mode')
    parser.add_argument('-o', '--output', action='store_true',
            help='save file')

    arg = parser.parse_args()

    if arg.output:
        for fig, savepath in zip(figs, savepaths):
            fig.savefig(savepath)
    
    plt.show()
