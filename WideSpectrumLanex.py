#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mytools as mt
import argparse
from common_functions import *
import shlex,subprocess
import scipy as sp

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
m_Ham = 0.03990413185798549

# ====================================
# Beam information
# ====================================
# Peak beam density
# nC/mm^2
sigma_peak           = 47e-9/np.power(1e-3,2)
sigma_peak_C_per_mm2 = sigma_peak * 1e-6

# ====================================
# Scintillator information
# ====================================
# Lanex scintillator efficiency
# photons/pC
SE = 1.75e9/1e-12*4*np.pi

# ====================================
# Camera Information
# ====================================
# GigE QE
QE_GigE = 0.5
QE_Ham  = 0.6

# Maximum counts, Hamamatsu
counts_max_Ham = 30e3

px_length = 6.5e-6

# ====================================
# Simplified counts function
# ====================================
def plot_counts(N,m_Ham,sigma):
    counts_cont = counts(
            sigma        = sigma,
            SE         = SE,
            N          = N,
            mag        = m_Ham,
            px_length  = px_length,
            QE         = QE_Ham
            )

    #  sigma_cont_nC_per_mm2 = sigma_cont*1e9/np.power(1e3,2)
    count_cont_frac = counts_cont/counts_max_Ham
    return count_cont_frac

# ====================================
# Beam density variable
# ====================================
# Needs to be in C/m^2
sigma           = np.logspace(-16,-7,100)/(1e-6)
sigma_C_per_mm2 = sigma * 1e-6

# ====================================
# m=-1 Analysis
# ====================================
#  f=24e-3
N = np.sqrt(8.0)
#  m_1 = -1.0
m_1 = -0.62
count_frac_m1 = plot_counts(N,m_1,sigma)

# ====================================
# 30cm FOV Analysis
# ====================================
#  f = 100e-3
N_30cm = np.sqrt(2.0)
count_frac_30cm = plot_counts(N_30cm,m_Ham,sigma)

# ====================================
# Create axis
# ====================================
fig = plt.figure()
gs  = gridspec.GridSpec(1,1)
ax  = fig.add_subplot(gs[0,0])

# ====================================
# Common plot config options
# ====================================
linewidth = 2

# ====================================
# Plot lines
# ====================================
plt100        = ax.loglog(sigma_C_per_mm2,count_frac_m1,label='Current ELANEX (m={:0.3f})'.format(m_1),linewidth=linewidth)
plt24         = ax.loglog(sigma_C_per_mm2,count_frac_30cm,label='Current WLANEX (m={:0.3f})'.format(m_Ham),linewidth=linewidth)
plt_Ham_max   = ax.loglog(sigma_C_per_mm2,np.ones(sigma.size),label='Hamamatsu Saturation Level',linewidth=linewidth)
plt_Ham_noise = ax.loglog(sigma_C_per_mm2,np.ones(sigma.size)*40/np.power(2,16),'orange',label='Hamamatsu Noise Level',linewidth=linewidth)

# ====================================
# Calculate points of interest
# ====================================
counts_peak_m_1    = plot_counts(N,m_1,sigma_peak)
counts_peak_30cm   = plot_counts(N_30cm,m_Ham,sigma_peak)
sigma_low            = 5e-4*1e-12/1e-6
sigma_low_C_per_mm2  = sigma_low*1e-6
counts_low         = plot_counts(N,m_1,sigma_low)
counts_low_cam     = counts_low*np.power(2,16)

sigma_guess = 1e-11/1e-6
sat_opt = sp.optimize.minimize(lambda x:np.power(plot_counts(N=N_30cm,m_Ham=m_Ham,sigma=x*sigma_guess)-1.0,2),x0=1)
sigma_sat = sigma_guess*sat_opt.x[0]
sigma_sat_C_per_mm2 = sigma_sat*1e-6
counts_sat = plot_counts(N=N_30cm,m_Ham=m_Ham,sigma=sigma_sat)

# ====================================
# Add points of interest
# ====================================
plt_m1     = ax.loglog(sigma_peak_C_per_mm2,counts_peak_m_1,'bo',label='_Peak density, 1:1 mag')
plt_30cm   = ax.loglog(sigma_peak_C_per_mm2,counts_peak_30cm,'go',label='_Peak density, 30-cm FOV')
plt_single = ax.loglog(sigma_low_C_per_mm2,counts_low,'bo',label='_Single count density')
plt_sat    = ax.loglog(sigma_sat_C_per_mm2,counts_sat,'ro',label='_Saturated')

# ====================================
# Annotate points of interest
# ====================================
ax.annotate(
        s          = 'Peak density,\n30-cm FOV',
        xy         = (sigma_peak_C_per_mm2,counts_peak_30cm),
        xytext     = (-100,-10),
        textcoords = 'offset points', ha = 'center', va = 'center',
        bbox       = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(1.05,0.5),arrowstyle='-',connectionstyle='arc3,rad=0.15',mutation_scale = 20,color='k')
        )

ax.annotate(
        s          = 'Peak density,\n1:1 mag.',
        xy         = (sigma_peak_C_per_mm2,counts_peak_m_1),
        xytext     = (-45,-80),
        textcoords = 'offset points', ha = 'center', va = 'center',
        bbox       = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(0.5,1.2),arrowstyle='-',connectionstyle='arc3,rad=0.15',mutation_scale = 20,color='k')
        )

ax.annotate(
        s          = r'Saturation {:0.2f} pC/mm$^2$'.format(sigma_sat_C_per_mm2*1e12),
        xy         = (sigma_sat_C_per_mm2,counts_sat),
        xytext     = (-100,30),
        textcoords = 'offset points', ha = 'center', va = 'center',
        bbox       = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(1.03,0.5),arrowstyle='-',connectionstyle='arc3,rad=-0.15',mutation_scale = 20,color='k')
        )

ax.annotate(
        s          = r'$\sigma=$5$\times$10$^{{-4}}$ pC/mm$^2$ = {:0.2f} counts'.format(counts_low_cam),
        xy         = (sigma_low_C_per_mm2,counts_low),
        xytext     = (40,0),
        textcoords = 'offset points', ha = 'left', va = 'top',
        bbox       = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(0,0.5),arrowstyle='-',connectionstyle='arc3,rad=-0.15',mutation_scale = 20,color='k')
        )


# ====================================
# Format plot
# ====================================
ax.grid(which='Both',color='0.7',linestyle='-')
ax.set_axisbelow(True)
ax.legend(loc=0,framealpha=0.75)

mt.addlabel(axes=ax,xlabel='Beam density [C/mm^2]',ylabel='Fractional Well Fill Level',toplabel='Hamamatsu Fraction of Well Depth in a Single Pixel')

ax2=ax.twinx()

ylims = np.array([1e-6,1e5])
ax.set_ylim(ylims)
ax2.set_ylim(ylims*np.power(2,16))
ax2.set_yscale('log')
mt.addlabel(axes=ax2,ylabel='Counts')

gs.tight_layout(fig)

# ====================================
# Calculate region
# ====================================
res = 1000
N_vector = np.linspace(np.sqrt(2),4,res)
FOV_vector = np.linspace(5e-2,40e-2,res)
FOV_vector_cm = FOV_vector * 1e2

NN, FOV = np.meshgrid(N_vector,FOV_vector)
FOV_cm = FOV*1e2

def performance(N,FOV):
    m = mag(h_img_Ham,FOV)
    return ap_fr_mag(N,m) * np.power(px_length/m,2)

rel = performance(NN,FOV)

norm_factor = np.max(rel)
rel = rel/norm_factor

#  fig2 = plt.figure(figsize=(16,12))
fig2 = plt.figure()

gs   = gridspec.GridSpec(2,2)
ax01 = fig2.add_subplot(gs[0,1])

plt01 = ax01.pcolormesh(NN,FOV_cm,rel,cmap='Blues_r')
ax01.axhline(30,linestyle='--',color='r',linewidth=linewidth)
ax01.axvline(np.sqrt(8),linestyle='--',color='r',linewidth=linewidth)

ylims = [FOV_vector_cm[0],FOV_vector_cm[-1]]
xlims = [N_vector[0],N_vector[-1]]
ax01.set_ylim(ylims)
ax01.set_xlim(xlims)
#  mt.addlabel(axes=ax01,xlabel='F-number',
#          ylabel='Field of View'
#          )
cb=fig2.colorbar(plt01)
mt.addlabel(cb=cb,clabel='Normalized Counts')

linewidth=1

# ====================================
# Lineout at N=2.8
# ====================================
ax00 = fig2.add_subplot(gs[0,0])

rel_f28 = performance(N=np.sqrt(8),FOV=FOV_vector_cm)
ax00.plot(rel_f28/norm_factor,FOV_cm,'b',linewidth=linewidth)
mt.addlabel(axes=ax00,xlabel='Normalized Counts',ylabel='Field of View [cm]')
ax00.set_xlim((0,0.3))
ax00.invert_xaxis()
#  ax00.grid(which='Both',color='0.7',linestyle='-')
#  ax00.set_axisbelow(True)

# ====================================
# Lineout at FOV=30 cm
# ====================================
ax11 = fig2.add_subplot(gs[1,1])

rel_30cm = performance(N=N_vector,FOV=30e-2)
N_list = np.array([np.sqrt(2),1.8,2,np.sqrt(8)])
rel_list = performance(N=N_list,FOV=30e-2)

ax11.plot(N_vector,rel_30cm/norm_factor,'b',N_list,rel_list/norm_factor,'bo',linewidth=linewidth)
ax11.set_xlim(xlims)
mt.addlabel(axes=ax11,ylabel='Normalized Counts',xlabel='Aperture f-number')

layout_rect = [0,0,1,0.95]
fig2.suptitle('Normalized Light Performance due to Magnification, F-number',fontsize=14,weight='bold')
gs.tight_layout(fig2,rect=layout_rect)

rel_list = rel_list/np.max(rel_list)

# ====================================
# DOF
# ====================================
def hyperfocal(f,N,c):
    return np.power(f,2)/(N*c)+f

def DOF(f,N,c,m):
    return 2.0*N*c*(m+1) / (np.power(m,2)-np.power(N*c/f,2))

c=px_length
N_vector = np.linspace(1.4,4,100)
f_vector = np.linspace(20e-3,50e-3,100)

NN, ff = np.meshgrid(N_vector,f_vector)

dof_vector = DOF(ff,NN,c,m_Ham)

# fig3 = plt.figure()
# gs = gridspec.GridSpec(1,1)
# axD = fig3.add_subplot(gs[0,0])
# 
# plt1 = axD.pcolormesh(NN,ff,dof_vector,cmap='Blues_r')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Creates a plot of object length vs. focal length.')
    parser.add_argument('-v','--verbose',action='store_true',
            help='enable verbose mode')
    parser.add_argument('-s','--save',action='store_true',
            help='save file')

    arg=parser.parse_args()

    if arg.save:
        fig.savefig('figs/Hamamatsu_Fraction.pdf')
        fig2.savefig('figs/Lens_Light_Performance.tiff')
        command = 'open figs'
        args = shlex.split(command)
        subprocess.call(args)

    
    plt.show()
