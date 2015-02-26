#!/usr/bin/env python
import ButterflyEmittancePython as bt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mytools as mt
import numpy as np
import os
import ElegantPy
import shlex
import slactrac as sltr
import subprocess
import sys

import jinja2 as jj
import ipdb

# ======================================
# Start logger
# ======================================
logger = mt.mylogger(filename='worksheet')

# ======================================
# Set up initial beam
# ======================================
energy_offset=np.float(3)
energy0 = np.float(20.35)
gamma = sltr.GeV2gamma(energy0+energy_offset)
emitx = np.float(100e-6)
emity = emitx

QS1_K1_default = 3.8743331090707228e-1
QS2_K1_default = -2.5439067538354171e-1
PEXT_Z = 1994.97
QS1_Z = 1998.71
AL_Z = 2015.16
BE_Z = 1996.34
ELANEX_Z = 2015.22
# IP2QS1_length = 5.4217
IP2QS1_length = QS1_Z-PEXT_Z

beam_x = sltr.BeamParams(
        beta  = 0.5,
        alpha = 0,
        emit = emitx
        )
beam_y = sltr.BeamParams(
        beta  = 5,
        alpha = 0,
        emit = emity
        )

# ======================================
# Set up spectrometer quadrupoles
# ======================================
setQS = mt.hardcode.setQS(energy_offset=energy_offset)
QS1_K1 = setQS.QS1.K1
QS2_K1 = setQS.QS2.K1

#  From Sebastien
#  QS1_K1 = 0.3856
#  QS2_K1 = -0.2474

# ======================================
# Get beamline for initial beam,
# spectrometer config
# ======================================
beamline=bt.beamlines.IP_to_lanex(
        beam_x = beam_x,
        beam_y = beam_y,
        QS1_K1 = QS1_K1,
        QS2_K1 = QS2_K1
        )
beamline.gamma=gamma

# ======================================
# Run elegant simulation
# ======================================
dir_elegant = os.path.join(os.getcwdu(),'temp')
path,root,ext = sltr.elegant_sim(
        beamline              = beamline              ,
        beam_pCentral         = sltr.GeV2gamma(20.35) ,
        lattice_pCentral      = sltr.GeV2gamma(20.35) ,
        n_particles_per_bunch = 5e5                   ,
        sigma_dp              = 0.2                   ,
        dir                   = dir_elegant
        )

# ======================================
# Open sim folder
# ======================================
command = 'open {}'.format(path)
subprocess.call(shlex.split(command))

# ======================================
# Open sim files
# ======================================
final_path = os.path.join(dir_elegant,'{}.fin'.format(root))
bunch_file = os.path.join(dir_elegant,'{}.out'.format(root))
mat_file   = os.path.join(dir_elegant,'{}.mat'.format(root))

ele_final  = ElegantPy.Final(final_path )
ele_bunch  = ElegantPy.Bunch(bunch_file )
ele_matrix = ElegantPy.Matrix(mat_file   )

# ======================================
# Print R matrix
# ======================================
np.set_printoptions(linewidth=140)

print ele_final.R
print beamline.R
print (ele_final.R-beamline.R)

# ======================================
# Create plots
# ======================================
fig = plt.figure(figsize=(8*3,6))
gs = gridspec.GridSpec(1,3)

bool = (ele_bunch.y > -0.041)
ax = fig.add_subplot(gs[0,0])
ax.hist2d(ele_bunch.x[bool],ele_bunch.y[bool],bins=200)

ax2 = fig.add_subplot(gs[0,1])
ax2.hist2d(ele_bunch.x,ele_bunch.delta,bins=200)

ax3 = fig.add_subplot(gs[0,2])
ax3.hist(ele_bunch.delta,bins=100)

gs.tight_layout(fig)

plt.show()
