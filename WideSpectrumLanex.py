#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mytools as mt

# ====================================
# Close all plots (for iPython)
# ====================================
plt.close('all')

# ====================================
# Define magnification and object
# ====================================
def mag(h_img,h_obj):
    return h_img/h_obj

def obj(f,m):
    return (1.0-1.0/m)*f

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

print m_GigE

# ====================================
# Get object distance as a
# fxn of focal length
# ====================================
f_cont = np.linspace(10,85,100)*1e-3
o_cont_GigE = obj(f_cont,m_GigE)
o_cont_Ham = obj(f_cont,m_Ham)

f_list = np.array([20,24,28,35,50,60,85])*1e-3
o_list_GigE = obj(f_list,m_GigE)
o_list_Ham = obj(f_list,m_Ham)

# ====================================
# Plot results
# ====================================
fig = plt.figure()
gs = gridspec.GridSpec(1,1)
ax = fig.add_subplot(gs[0,0])
plt1 = ax.plot(f_cont/1e-3,o_cont_GigE,'b-',label='_GigE')
plt2 = ax.plot(f_list/1e-3,o_list_GigE,'b-o',label='GigE')

plt3 = ax.plot(f_cont/1e-3,o_cont_Ham,'r-',label='_Ham')
plt4 = ax.plot(f_list/1e-3,o_list_Ham,'r-o',label='Hamamatsu')

mt.addlabel(axes=ax,xlabel='Focal Length [mm]',ylabel='Object distance [m]',toplabel='Distance to Screen')

gs.tight_layout(fig)

ax.legend(loc=0)

fig.savefig('GigE_Distance_to_Screen.pdf')

# ====================================
# Beam information
# ====================================
# Peak beam density
# nC/mm^2
rho_peak = 47e-9/(1e-3**2.0)

# ====================================
# Scintillator information
# ====================================
# Lanex scintillator efficiency
# photons/nC
SE = 1.75e9/1e-9*4*np.pi
SE_SI_units = SE

# ====================================
# Camera Information
# ====================================
# GigE QE
QE_GigE = 0.5
QE_Ham = 0.6

# Maximum counts, Hamamatsu
counts_max_Ham = 30e3

px_area = np.power(6.5e-6,2)

# ====================================
# Aperture function
# ====================================
# aperture fraction
def ap_fr(f,N,o):
    lens_area = np.pi*np.power(f/(2.0*N),2.0)
    sphere_area = 4*np.pi*np.power(o,2)
    return lens_area/sphere_area

def ap_fr_mag(N,m):
    return np.power(m/((m-1.0)*4*N),2)

# ====================================
# Full counts function
# ====================================
def counts(rho,se,N,mag,px_area,QE):
    return rho*se*ap_fr_mag(N,mag)*(px_area/np.absolute(mag))*QE

# ====================================
# Simplified counts function
# ====================================
def plot_counts(f,N,m_Ham,rho):
    counts_cont = counts(
            rho     = rho,
            se      = SE_SI_units,
            N       = N,
            mag     = m_Ham,
            px_area = px_area,
            QE      = QE_Ham
            )

    #  rho_cont_nC_per_mm2 = rho_cont*1e9/np.power(1e3,2)
    count_cont_frac = counts_cont/counts_max_Ham
    return count_cont_frac

# ====================================
# Beam density variable
# ====================================
# Needs to be in C/m^2
rho           = np.logspace(-12,-7,100)/(1e-6)
rho_C_per_mm2 = rho * 1e-6

# ====================================
# 24mm Lens Analysis
# ====================================
f=24e-3
N = 2.8
count_frac_24 = plot_counts(f,N,m_Ham,rho)

# ====================================
# 100mm Lens Analysis
# ====================================
f = 100e-3
m_1 = -1.0

count_frac_100 = plot_counts(f,N,m_1,rho)

fig=plt.figure()
ax=fig.add_subplot(gs[0,0])

plt100=ax.loglog(rho_C_per_mm2,count_frac_100,label='100mm Lens, zoomed in (ELANEX)')
plt24=ax.loglog(rho_C_per_mm2,count_frac_24,label='24mm Lens (Wide Lanex)')


ax.grid(True,which='Both')
ax.legend(loc=0)

mt.addlabel(axes=ax,xlabel='Beam density [C/mm^2]',ylabel='Count Fraction',toplabel='Hamamatsu Fraction of Max Count in a Single Pixel')
gs.tight_layout(fig)

plt.show()
