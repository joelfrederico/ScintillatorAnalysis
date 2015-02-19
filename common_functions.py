import numpy as np

# ====================================
# Define magnification and object
# ====================================
def mag(h_img,h_obj):
    return h_img/h_obj

def obj(f,m):
    return (1.0-1.0/m)*f

# ====================================
# Aperture function
# ====================================
# aperture fraction
def ap_fr(f,N,o):
    lens_area = np.pi*np.power(f/(2.0*N),2.0)
    sphere_area = 4.0*np.pi*np.power(o,2.0)
    return lens_area/sphere_area

def ap_fr_mag(N,m):
    return np.power(m/((m-1.0)*4.0*N),2.0)

# ====================================
# Full counts function
# ====================================
def counts(rho,se,N,mag,px_length,QE):
    return rho*se*ap_fr_mag(N,mag)*np.power(px_length/mag,2)*QE