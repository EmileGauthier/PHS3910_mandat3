import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def wavelength_to_rgb(wavelength, gamma=0.8):
    '''This converts a given wavelength of light to an \n",
    approximate RGB color value. The wavelength must be given\n",
    in nanometers in the range from 380 nm through 750 nm\n",
    (789 THz through 400 THz).\n",
\n",
    Based on code by Dan Bruton\n",
    http://www.physics.sfasu.edu/astro/color/spectra.html\n",
    '''
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    return (int(R), int(G), int(B))


plt.rcParams['figure.dpi'] = 150

# Paramètres
lbd = 1e-9 * np.linspace(400,700,1000) # longueur d'onde (m)
f1 = 50e-3 # focale de la 1ere lentille (m)
f2 = 30e-3 # focale de la 2e lentille (m)
L = 100e-6 # taille de l'ouverture (m)
Lambda = 1e-3 * (600)**(-1) # pas du réseau (m)
print(Lambda)

# Positions spatiales du premier ordre en fonction de la longueur d'onde :
x2 = (lbd*f2/Lambda) * 1

# Calcul des couleurs RGB en fonction de la longueur d'onde
rgb_colors = np.zeros([1,len(lbd),3])
for i in range(len(lbd)):
    rgb_colors[0,i,:] = wavelength_to_rgb(1e9*lbd[i])

# Normalisation et aggrandissement de l'image
rgb_colors = np.repeat(rgb_colors, int(len(lbd)/4), axis=0) / 255

# Affichage de l'image
extent_values = [0,1e3*(np.max(x2)-np.min(x2)),0,1e3*(np.max(x2)-np.min(x2))/4]
plt.imshow(rgb_colors, extent=extent_values)
plt.xlabel(r"Position en $x$ (mm)", fontsize = 12)
plt.ylabel(r"Position en $y$ (mm)", fontsize = 12)
plt.show()


  
