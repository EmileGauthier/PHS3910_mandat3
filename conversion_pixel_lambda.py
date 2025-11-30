import numpy as np
import matplotlib.pyplot as plt

# Données de calibration (obtenues avec des lasers de longueurs d'onde connues)
pixel_means = np.array([343,1762,2415,2708,3324])
uncertainties = np.array([29.70196341, 188.83664198, 124.30615492,159.96283316,83.97334868])
wavelengths = np.array([405,532,571,593,650])

plt.plot(pixel_means,wavelengths)
plt.scatter(pixel_means,wavelengths)
plt.show()

# Construction du modèle linéaire

X = np.column_stack((pixel_means, np.ones_like(pixel_means)))
beta, _, _, _ = np.linalg.lstsq(X, wavelengths, rcond=None) 
m = beta[0]  
c = beta[1]

# Calcul des incertitudes sur la pente et l'ordonnée à l'origine

def incertitudes_poids(x, y, alpha_x, alpha_y, slope):
    # Retourne l'incertitude sur la pente et l'ordonnée à l'origine « à la Ménard »

    alpha_y_tot = np.sqrt((alpha_y **2 + (alpha_x * slope)**2))

    weights = np.divide(1,alpha_y_tot**2)

    Delta_prime = np.sum(weights)*np.sum(weights * x**2) - (np.sum(weights*x))**2

    alpha_c = np.sqrt(np.sum(weights*x**2)/Delta_prime)
    alpha_m = np.sqrt(np.sum(weights)/Delta_prime)

    return [alpha_m, alpha_c]

[alpha_m, alpha_c] = incertitudes_poids(pixel_means, wavelengths, 0.5, uncertainties, m)


### Conversion de pixels (sans unité) à longueur d'onde (nm), avec incertitudes.

pixel_value = np.linspace(0,4000,100)

wavelength_value = m * pixel_value + c
wavelength_uncertainty = np.sqrt((pixel_value * alpha_m)**2 + alpha_c**2 )

plt.plot(wavelength_value, wavelength_uncertainty)
plt.show()

#print(f"Pour le pixel {pixel_value}, la valeur de longueur d'onde assosciée est ({wavelength_value:.2f} ± {wavelength_uncertainty:.2f})nm")


