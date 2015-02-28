#!/usr/bin/env python

import ElegantPy
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import mytools as mt
import numpy as np
import os
import slactrac as sltr
import copy

# ======================================
# Start logger
# ======================================
logger = mt.mylogger(filename='worksheet')

# ======================================
# Define beamline
# ======================================
# Beamline elements
#  ECOLQS   : ECOL, L= 0.00,X_MAX= 25.8E-3,Y_MAX= 25.8E-3
#  TOR3255  : ECOL, L= 0.00, X_MAX= 1.11E-2,Y_MAX= 1.11E-2
#  RCOLBEND: RCOL, L=0.00,XMAX= 2.23E-2,YMAX= 4.78E-2

QS0_K1 = -8.411e-1
QS1_K1 = 3.647850372034315e-01
QS2_K1 = -1.223335345241937e-01

LPEXT2QS0     = sltr.Drift( name = 'LPEXT2QS0'     , length = 2.65)
QS0           = sltr.Quad(  name = 'QS0'           , length = 4.61E-01    , K1=QS0_K1    , INTEGRATION_ORDER=4 , N_KICKS=8 )
LQS02TOR3255  = sltr.Drift( name = 'LQS02TOR3255'  , length = 1.729                                                         )
LTOR2QS1      = sltr.Drift( name = 'LTOR2QS1'      , length = 0.26                                                          )
QS1           = sltr.Quad(  name = 'QS1'           , length = 1.0E-00     , K1=QS1_K1     , INTEGRATION_ORDER=4 , N_KICKS=8 )
LQS12QS2      = sltr.Drift( name = 'LQS12QS2'      , length = 4.00E+00                                                      )
QS2           = sltr.Quad(  name = 'QS2'           , length = 1.0E-00     , K1=QS2_K1    , INTEGRATION_ORDER=4 , N_KICKS=8 )
LQS22BEND     = sltr.Drift( name = 'LQS22BEND'     , length = 0.7428E+00                                                    )
B5D36         = sltr.Bend(  name = 'B5D36'         , length = 9.779E-01   , angle=6.0E-03 , EDGE1_EFFECTS=1     , E1=3.0E-3  , EDGE2_EFFECTS=1 , E2=3.0E-3 , HGAP=3E-02 , rotate=90, SYNCH_RAD = 0)
LBEND2DUMP1   = sltr.Drift( name = 'LBEND2DUMP1'   , length = 8.795E+00 )
LDUMP12ELANEX = sltr.Drift( name = 'LDUMP12ELANEX' , length = 0.06      )
LELANEX2DUMP2 = sltr.Drift( name = 'LELANEX2DUMP2' , length = 0.06      )

gamma    = np.float_(39824)
#  gamma = sltr.GeV2gamma(30.0)
emit = 100e-6/gamma
beam_x = sltr.BeamParams(
        beta  = 0.5,
        alpha = 0,
        emit = emit
        )
beam_y = sltr.BeamParams(
        beta  = 5.0,
        alpha = 0,
        emit = emit
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
        beam_x = beam_x,
        beam_y = beam_y
 )

# ======================================
# Run elegant and load simulation
# ======================================

dir_elegant = os.path.join(os.getcwdu(),'temp')
#  path,root,ext = sltr.elegant_sim(
#         beamline              = supersimpledumpline   ,
#         beam_pCentral         = sltr.GeV2gamma(20.35) ,
#         lattice_pCentral      = sltr.GeV2gamma(20.35) ,
#         n_particles_per_bunch = 5e5                   ,
#         sigma_dp              = 0                   ,
#         dir                   = dir_elegant           ,
#         filename              = os.path.join(dir_elegant,'out.ele')
#         )

# ele_path = os.path.join(path,root+ext)
# 
# ESim = ElegantPy.ElegantSim(ele_path)

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

# ======================================
# Offset energies
# ======================================

energy_list_GeV = np.linspace(10,80,501)
energy_list_gamma = sltr.GeV2gamma(energy_list_GeV)

rho = np.zeros(energy_list_gamma.size)
sigx = np.zeros(energy_list_gamma.size)
sigy = np.zeros(energy_list_gamma.size)

orig_beamline = copy.deepcopy(supersimpledumpline)

for i,energy_gamma in enumerate(energy_list_gamma):
    beamline = copy.deepcopy(supersimpledumpline)
    beamline.gamma = energy_gamma
    runelegant = False
    if runelegant:
        path,root,ext = sltr.elegant_sim(
                beamline              = beamline,
                beam_pCentral         = energy_gamma        ,
                lattice_pCentral      = energy_gamma        ,
                n_particles_per_bunch = 1e5                 ,
                sigma_dp              = 0                   ,
                dir                   = dir_elegant         ,
                filename              = 'out_{:02.0f}.ele'.format(i)
                )
        
        ele_path = os.path.join(path,root+ext)
        
        ESim = ElegantPy.ElegantSim(ele_path)

        sigx[i] = np.std(ESim.Bunch.x)
        sigy[i] = np.std(ESim.Bunch.y)
    else:
        sigx[i] = beamline.beam_x_end.spotsize
        sigy[i] = beamline.beam_y_end.spotsize

    rho[i] = 1.0/(sigx[i]*sigy[i])

fig=plt.figure()
gs=gridspec.GridSpec(1,1)
ax = fig.add_subplot(gs[0,0])

sigx_inv = 1.0/sigx
sigy_inv = 1.0/sigy
sigx_inv_norm = sigx_inv/np.max(sigx_inv)
sigy_inv_norm = sigy_inv/np.max(sigy_inv)

ax.semilogy(energy_list_GeV,rho/np.max(rho),'-',label='$1/(\sigma_x \sigma_y)$')
ax.semilogy(energy_list_GeV,sigx_inv_norm,'-',label='$\sigma_x$')
ax.semilogy(energy_list_GeV,sigy_inv_norm,'-',label='$\sigma_y$')
plt.legend(loc=0)

mt.addlabel(ax=ax,xlabel='GeV',ylabel='[Normalized]',toplabel='Visibility, Design Energy {:02.2f} GeV'.format(sltr.gamma2GeV(gamma)))

ax.grid(which='Both',color='0.7',linestyle='-')
ax.set_axisbelow(True)

gs.tight_layout(fig)

#  fig.savefig('Visibility.tiff')
fig.savefig('Visibility_DesignE_{:0.2f}GeV.png'.format(sltr.gamma2GeV(gamma)))

plt.show()
