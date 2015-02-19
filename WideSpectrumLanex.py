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

#  fig.savefig('GigE_Distance_to_Screen.pdf')

# ====================================
# Beam information
# ====================================
# Peak beam density
# nC/mm^2
rho_peak = 47e-9/np.power(1e-3,2)
rho_peak_C_per_mm2 = rho_peak * 1e-6

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
QE_Ham = 0.6

# Maximum counts, Hamamatsu
counts_max_Ham = 30e3

px_length = 6.5e-6

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
def counts(rho,se,N,mag,px_length,QE):
    return rho*se*ap_fr_mag(N,mag)*np.power(px_length/mag,2)*QE

# ====================================
# Simplified counts function
# ====================================
def plot_counts(N,m_Ham,rho):
    counts_cont = counts(
            rho       = rho,
            se        = SE,
            N         = N,
            mag       = m_Ham,
            px_length = px_length,
            QE        = QE_Ham
            )

    #  rho_cont_nC_per_mm2 = rho_cont*1e9/np.power(1e3,2)
    count_cont_frac = counts_cont/counts_max_Ham
    return count_cont_frac

# ====================================
# Beam density variable
# ====================================
# Needs to be in C/m^2
rho           = np.logspace(-16,-7,100)/(1e-6)
rho_C_per_mm2 = rho * 1e-6

# ====================================
# m=-1 Analysis
# ====================================
#  f=24e-3
N = np.sqrt(8.0)
m_1 = -1.0
count_frac_m1 = plot_counts(N,m_1,rho)

# ====================================
# 30cm FOV Analysis
# ====================================
#  f = 100e-3

count_frac_30cm = plot_counts(N,m_Ham,rho)

fig=plt.figure()
ax=fig.add_subplot(gs[0,0])

plt100=ax.loglog(rho_C_per_mm2,count_frac_m1,label='1:1 Magnification (ELANEX?)')
plt24=ax.loglog(rho_C_per_mm2,count_frac_30cm,label='30-cm FOV')
plt_Ham_max=ax.loglog(rho_C_per_mm2,np.ones(rho.size),label='Hamamatsu Saturation Level')
plt_Ham_noise=ax.loglog(rho_C_per_mm2,np.ones(rho.size)*40/np.power(2,16),'orange',label='Hamamatsu Noise Level')

counts_peak_m_1 = plot_counts(N,m_1,rho_peak)
counts_peak_30cm = plot_counts(N,m_Ham,rho_peak)
rho_low = 5e-4*1e-12/1e-6
rho_low_C_per_mm2 = rho_low*1e-6
rho_low_pC_per_mm2 = rho_low*1e-6*1e12
counts_low = plot_counts(N,m_1,rho_low)
counts_low_cam = counts_low*np.power(2,16)

plt_m1=ax.loglog(rho_peak_C_per_mm2,counts_peak_m_1,'bo',label='_Peak density, 1:1 mag')
plt_30cm=ax.loglog(rho_peak_C_per_mm2,counts_peak_30cm,'go',label='_Peak density, 30-cm FOV')
plt_30cm=ax.loglog(rho_low_C_per_mm2,counts_low,'bo',label='_Single count density')

ax.annotate(
        s='Peak density, 30-cm FOV',
        xy=(rho_peak_C_per_mm2,counts_peak_30cm),
        xytext = (0,15),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(0.5,-0.3),arrowstyle='-',connectionstyle='arc3,rad=0.15',mutation_scale = 20,color='k')
        )

ax.annotate(
        s='Peak density, 1:1 mag.',
        xy=(rho_peak_C_per_mm2,counts_peak_m_1),
        xytext = (0,-130),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(0.5,1.3),arrowstyle='-',connectionstyle='arc3,rad=0.15',mutation_scale = 20,color='k')
        )

ax.annotate(
        s=r'$\rho=$5$\times$10$^{{-4}}$ pC/mm$^2$ = {:0.2f} counts'.format(counts_low_cam),
        xy=(rho_low_C_per_mm2,counts_low),
        xytext = (40,0),
        textcoords = 'offset points', ha = 'left', va = 'top',
        bbox = dict(boxstyle='round,pad=0.5',fc='white',alpha=0.75),
        arrowprops = dict(relpos=(0,0.5),arrowstyle='-',connectionstyle='arc3,rad=-0.15',mutation_scale = 20,color='k')
        )


ax.grid(True,which='Both')
ax.legend(loc=0,framealpha=0.75)

mt.addlabel(axes=ax,xlabel='Beam density [C/mm^2]',ylabel='Fractional Well Fill Level',toplabel='Hamamatsu Fraction of Well Depth in a Single Pixel')

ax2=ax.twinx()

ylims = np.array([1e-6,1e5])
ax.set_ylim(ylims)
ax2.set_ylim(ylims*np.power(2,16))
ax2.set_yscale('log')
mt.addlabel(axes=ax2,ylabel='Counts')

gs.tight_layout(fig)

print 'Counts for {:0.2e} pC/mm^2: {:0.2f} counts'.format(rho_low_pC_per_mm2, counts_low_cam) 

fig.savefig('Hamamatsu_Fraction.pdf')
plt.show()
