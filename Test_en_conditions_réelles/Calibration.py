import numpy as np
import matplotlib.pyplot as plt

# Données de calibration (obtenues avec des lasers de longueurs d'onde connues)
pixel_means = np.array([39, 1933, 2240, 2581,2894,3976])
uncertainties = np.array([24.27325211, 32.08567438, 25.84706858, 51.10744416, 22.99862671, 64.65646317])
wavelengths = np.array([405, 532, 555, 571, 593, 650])

# Estimation de la pente
X = np.column_stack((pixel_means, np.ones_like(pixel_means)))
beta, _, _, _ = np.linalg.lstsq(X, wavelengths, rcond=None) 
m = beta[0]  

# Régression linéaire pour des incertitudes non-uniformes

def regression_poids(x, y, alpha_x, alpha_y, slope_estimate):
    # Retourne l'incertitude sur la pente et l'ordonnée à l'origine « à la Ménard »

    alpha_y_tot = np.sqrt((alpha_y **2 + (alpha_x * slope_estimate)**2))

    weights = np.divide(1,alpha_y_tot**2)

    Delta_prime = np.sum(weights)*np.sum(weights * x**2) - (np.sum(weights*x))**2

    m = ((np.sum(weights)*np.sum(weights*x*y)) - np.sum(weights*x)*np.sum(weights*y))/Delta_prime
    c = ((np.sum(weights*x**2)*np.sum(weights*y)) - np.sum(weights*x)*np.sum(weights*x*y))/Delta_prime

    alpha_c = np.sqrt(np.sum(weights*x**2)/Delta_prime)
    alpha_m = np.sqrt(np.sum(weights)/Delta_prime)

    return [m,c,alpha_m, alpha_c]

[m,c,alpha_m, alpha_c] = regression_poids(pixel_means, wavelengths, uncertainties, 0, m)

pixel_value = np.linspace(1,4000,100)

plt.errorbar(pixel_means, wavelengths, xerr = uncertainties, yerr=0, fmt='o', capsize=5, label = "Mesures expérimentales")
plt.plot(pixel_value, pixel_value*m + c, label = "Régression linéaire")
plt.xlabel(r"Position en $x$ sur le détecteur (pixel)", fontsize = 12)
plt.ylabel("Longueur d'onde (nm)", fontsize = 12)
plt.legend(fontsize = 12)
plt.tight_layout()
#plt.show()


### Conversion de pixels (sans unité) à longueur d'onde (nm), avec incertitudes.

# Pour une longueur d'onde

pixel_value = 1300

wavelength_value = m * pixel_value + c

# Ajout en quadrature de l'incertitude sur x et y
wavelength_uncertainty = np.sqrt((pixel_value * alpha_m)**2 + alpha_c**2)

#print(f"Pour le pixel {pixel_value}, la valeur de longueur d'onde assosciée est ({wavelength_value:.2f} ± {wavelength_uncertainty:.2f})nm")

# Pour calculer la résolution

# 405 -> 39, 24.27325211
# 555 -> 2240, 25.84706858
# 571 -> 2581, 51.10744416
# 650 -> 3976, 64.65646317

pixel_value1 = 39 - 24.27325211
pixel_value2 = 39 + 24.27325211

#pixel_value1 = 723 # Borne inférieure (filtre)
#pixel_value2 = 1524 # Borne supérieure (filtre)
 
wavelength_value1 = m * pixel_value1 + c
wavelength_value2 = m * pixel_value2 + c

# Ajout en quadrature de l'incertitude sur x et y
wavelength_uncertainty1 = pixel_value1 * alpha_m
wavelength_uncertainty2 = pixel_value2 * alpha_m

print(f"La résolution est de {wavelength_value2 - wavelength_value1}, et l'incertitude sur la résolution est de {(pixel_value2 - pixel_value1)*alpha_m})}")
