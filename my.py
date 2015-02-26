#!/usr/bin/env python

import ElegantPy
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import mytools as mt
import numpy as np
import os
import slactrac as sltr

# ======================================
# Start logger
# ======================================
#  logger = mt.mylogger(filename='worksheet')

# ======================================
# Define beamline
# ======================================
# Beamline elements
#  ECOLQS   : ECOL, L= 0.00,X_MAX= 25.8E-3,Y_MAX= 25.8E-3
#  TOR3255  : ECOL, L= 0.00, X_MAX= 1.11E-2,Y_MAX= 1.11E-2
#  RCOLBEND: RCOL, L=0.00,XMAX= 2.23E-2,YMAX= 4.78E-2


LPEXT2QS0     = sltr.Drift( name = 'LPEXT2QS0'     , length = 2.65)
QS0           = sltr.Quad(  name = 'QS0'           , length = 4.61E-01    , K1=-0.8416    , INTEGRATION_ORDER=4 , N_KICKS=8 )
LQS02TOR3255  = sltr.Drift( name = 'LQS02TOR3255'  , length = 1.729                                                         )
LTOR2QS1      = sltr.Drift( name = 'LTOR2QS1'      , length = 0.26                                                          )
QS1           = sltr.Quad(  name = 'QS1'           , length = 1.0E-00     , K1=0.3738     , INTEGRATION_ORDER=4 , N_KICKS=8 )
LQS12QS2      = sltr.Drift( name = 'LQS12QS2'      , length = 4.00E+00                                                      )
QS2           = sltr.Quad(  name = 'QS2'           , length = 1.0E-00     , K1=-0.1302    , INTEGRATION_ORDER=4 , N_KICKS=8 )
LQS22BEND     = sltr.Drift( name = 'LQS22BEND'     , length = 0.7428E+00                                                    )
B5D36         = sltr.Bend(  name = 'B5D36'         , length = 9.779E-01   , angle=6.0E-03 , EDGE1_EFFECTS=1     , E1=3.0E-3  , EDGE2_EFFECTS=1 , E2=3.0E-3 , HGAP=3E-02 , rotate=90, SYNCH_RAD = 0)
LBEND2DUMP1   = sltr.Drift( name = 'LBEND2DUMP1'   , length = 8.795E+00 )
LDUMP12ELANEX = sltr.Drift( name = 'LDUMP12ELANEX' , length = 0.06      )
LELANEX2DUMP2 = sltr.Drift( name = 'LELANEX2DUMP2' , length = 0.06      )

gamma    = np.float_(39824)
emitx = 0.001363/gamma
betax = 1
alphax = 0
beam = sltr.BeamParams(
        beta  = 0.5,
        alpha = 0,
        emit = emitx
        )

supersimpledumpline=sltr.Beamline(
        element_list=[
            LPEXT2QS0,
            #  ECOLQS,
            QS0,
            #  ECOLQS,
            LQS02TOR3255,
            #  TOR3255,
            LTOR2QS1,
            #  ECOLQS,
            #  ECOLQS,
	    QS1,
            #  ECOLQS,
            LQS12QS2,
            #  ECOLQS,
	    QS2,
            #  ECOLQS,
            LQS22BEND,
            #  RCOLBEND,
            B5D36,
            #  RCOLBEND,
            LBEND2DUMP1,
            #  DUMP1,
            LDUMP12ELANEX
            #  ELANEX,
            #  ELANEXDUMP,
            #  LELANEX2DUMP2,
            #  DUMP2,
            #  LDUMP22CHERNEAR,
            #  CHERNEAR,
            #  LCHERNEAR2AERO,
            #  AEROGEL,
            #  LAERO2CHERFAR,
            #  CHERFAR
            ],
        gamma  = gamma,
        beam_x = beam,
        beam_y = beam
 )

# ======================================
# Run elegant and load simulation
# ======================================

dir_elegant = os.path.join(os.getcwdu(),'temp')
path,root,ext = sltr.elegant_sim(
        beamline              = supersimpledumpline   ,
        beam_pCentral         = sltr.GeV2gamma(20.35) ,
        lattice_pCentral      = sltr.GeV2gamma(20.35) ,
        n_particles_per_bunch = 5e5                   ,
        sigma_dp              = 0.2                   ,
        dir                   = dir_elegant           ,
        filename              = os.path.join(dir_elegant,'out.ele')
        )

ele_path = os.path.join(path,root+ext)

ESim = ElegantPy.ElegantSim(ele_path)

# ======================================
# Create plots
# ======================================
# fig = plt.figure(figsize=(8*3,6))
# gs = gridspec.GridSpec(1,3)
# 
# ele_bunch = ESim.Bunch
# 
# bool_x = (np.abs(ele_bunch.x) < 0.01)
# bool_y = (ele_bunch.y > -0.041)
# bool = np.logical_and(bool_x,bool_y)
# ax = fig.add_subplot(gs[0,0])
# ax.hist2d(ele_bunch.x[bool],ele_bunch.y[bool],bins=200)
# 
# ax2 = fig.add_subplot(gs[0,1])
# ax2.hist2d(ele_bunch.x[bool],ele_bunch.delta[bool],bins=200)
# 
# ax3 = fig.add_subplot(gs[0,2])
# ax3.hist(ele_bunch.delta,bins=100)
# 
# gs.tight_layout(fig)
# 
# plt.show()
