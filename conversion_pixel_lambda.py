import numpy as np
import matplotlib.pyplot as plt

# Données de calibration (obtenues avec des lasers de longueurs d'onde connues)
pixel_means = np.array([562,770,863,1026])
uncertainties = np.array([12.83798508, 15.2689612, 22.58015907,21.15126552])
wavelengths = np.array([432,571,593,650])

#plt.scatter(wavelengths,pixel_means, marker='D')
#plt.plot(wavelengths,pixel_means)
#plt.show()

# Construction du modèle linéaire

X = np.column_stack((pixel_means, np.ones_like(pixel_means)))
beta, _, _, _ = np.linalg.lstsq(X, wavelengths, rcond=None) 
m = beta[0]  
c = beta[1]

# Calcul des incertitudes sur la pente et l'ordonnée à l'origine

def incertitudes(x, y, slope, intercept):
    # Retourne l'incertitude sur la pente et l'ordonnée à l'origine « à la Ménard »

    N = len(x)
    moy_x = np.mean(x)
    alpha_y = np.sqrt(np.sum((y - (slope * x + intercept))**2) / (N - 2))
    Delta = N * np.sum((x-moy_x)**2)

    alpha_m = alpha_y * np.sqrt(N/Delta)
    alpha_c = alpha_y * np.sqrt(np.sum(x**2)/Delta)

    return [alpha_m, alpha_c]

[alpha_m, alpha_c] = incertitudes(pixel_means, wavelengths, m, c)

### Conversion de pixels (sans unité) à longueur d'onde (nm), avec incertitudes.

pixel_value = 600

wavelength_value = m * pixel_value + c
wavelength_uncertainty = alpha_m * pixel_value + alpha_c

print(f"Pour le pixel {pixel_value}, la valeur de longueur d'onde assosciée est ({wavelength_value:.2f} ± {wavelength_uncertainty:.2f})nm")









