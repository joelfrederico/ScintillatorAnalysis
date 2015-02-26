#!/usr/bin/env python

import slactrac as sltr
import numpy as np
import os
import ElegantPy
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

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
        filename              = 'out.ele'
        )

ele_path = os.path.join(path,root+ext)

ESim = ElegantPy.ElegantSim(ele_path)

# ======================================
# Rotation matrix
# ======================================

theta = np.pi/2
phi   = np.pi/2
psi   = 0

c_theta = np.cos(theta)
c_phi   = np.cos(phi)
c_psi   = np.cos(psi)

s_theta = np.sin(theta)
s_phi   = np.sin(phi)
s_psi   = np.sin(psi)

R = np.zeros((3,3))
R[0,0] = c_theta*c_psi
R[0,1] = c_phi*s_psi + s_phi*s_theta*c_psi
R[0,2] = s_phi*s_psi - c_phi*s_theta*c_psi
R[1,0] = -c_theta*s_psi
R[1,1] = c_phi*c_psi - s_phi*s_theta*s_psi
R[1,2] = s_phi*c_psi + c_phi*s_theta*s_psi
R[2,0] = s_theta
R[2,1] = -s_phi*c_theta
R[2,2] = c_phi*c_theta

# ======================================
# Generate tons of histograms
# ======================================

# ds = 0.002
# 
# gs = gridspec.GridSpec(1,1)
# xmin = -0.002
# xmax = 0.002
# xrange = xmax-xmin
# ymin = -0.1
# ymax = 0.05
# yrange = ymax-ymin
# 
# for i in range(0,2001):
#     s     = np.float(-1) + (i*ds)
#     titlestr = '{:01.3f} meters'.format(s)
#     print titlestr
#     x_new = ESim.Bunch.x + ESim.Bunch.xp * s
#     y_new = ESim.Bunch.y + ESim.Bunch.yp * s
# 
#     x_ind = np.logical_and(x_new > xmin, x_new < xmax)
#     y_ind = np.logical_and(y_new > ymin, y_new < ymax)
#     ind   = np.logical_and(x_ind,y_ind)
# 
#     fig = plt.figure(figsize=(2,7.5))
#     ax  = fig.add_subplot(gs[0,0])
#     ax.hist2d(x_new[ind],y_new[ind],bins=500,range=[[xmin,xmax],[ymin,ymax]])
# 
#     gs.tight_layout(fig)
#     ax.set_title(titlestr)
# 
#     fig.savefig('{:04d}.png'.format(i))
#     plt.close(fig)

# ======================================
# 
# ======================================
