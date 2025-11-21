import numpy as np
import matplotlib.pyplot as plt

# Fonction rectangulaire
def rect(x):
    return np.where(np.abs(x) <= 0.5, 1.0, 0.0)

# Fonction U2
def U2(x2, lambda0, f1, f2, a, d):
    arg = -f1 / (f2 * a) * (x2 - (lambda0 * f2 / d))
    return ((lambda0 * f1) / a) * rect(arg)

# Paramètres fixes
lambda0 = 500e-6  # Longueur d'onde en mm (500 nm)
f1 = 50  # mm
a = 0.1  # Largeur de fente en mm
d = 1/300  # Pas du réseau en mm (300 traits/mm)

# Gamme de f2
f2_values = np.linspace(10, 150, 300)  # f2 de 10 à 150 mm
fwhm_values = []

# Calcul de la FWHM pour chaque f2
for f2 in f2_values:
    # Position du centre de la fonction rectangulaire
    center = lambda0 * f2 / d
    
    # Largeur totale du rectangle (déterminée par la condition |arg| <= 0.5)
    width = (f2 * a) / f1  # Largeur totale du rectangle en mm
    
    # La FWHM d'une fonction rectangulaire est égale à sa largeur totale
    fwhm = width
    fwhm_values.append(fwhm)

# Tracé du graphique
plt.figure(figsize=(10, 6))
plt.plot(f2_values, fwhm_values, 'b-', linewidth=2)
plt.xlabel('Distance focale f2 (mm)', fontsize=12)
plt.ylabel('Résolution (mm)', fontsize=12)
plt.title('Impact de f2 sur la résolution spectrale\n(f1 = 50 mm fixe)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xlim(0, 160)
plt.tight_layout()
plt.show()















# Fonction FWHM de U2
def fwhm_U2(f1, f2, a):
    return (f2 * a) / f1

# Paramètres fixes
a = 0.1  # largeur de fente en mm

# Gammes de f1 et f2 pour la carte
f1_values = np.linspace(0, 120, 200)
f2_values = np.linspace(0, 160, 300)

# Création de la grille
F1, F2 = np.meshgrid(f1_values, f2_values)

# Calcul de la FWHM
FWHM = fwhm_U2(F1, F2, a)

# Tracé de la carte de chaleur
plt.figure(figsize=(12, 7))
im = plt.imshow(FWHM, extent=[f1_values[0], f1_values[-1], f2_values[0], f2_values[-1]],
                origin='lower', aspect='auto', cmap='viridis')
plt.colorbar(im, label='FWHM (mm)')
plt.xlabel('f1 (mm)')
plt.ylabel('f2 (mm)')
plt.title('Carte de chaleur 2D : Résolution de U2 en fonction de f1 et f2')

# Points spécifiques à afficher avec annotations f1, f2 et FWHM
points = [
    (100, 100), (100, 75), (100, 50), (100, 25), (100, 10),
    (75, 100), (50, 100), (25, 100), (10, 100), (50, 30), (50,20), (50,10), (10,10), (30,50), (20,50),(10,50), (5,5), (20,20), (30,30),
    (40,40), (50,50), (60,60), (50,60), (60,50), (70,70), (80,80), (90,90), (80,50), (50,80)
]

for f1, f2 in points:
    fwhm_val = fwhm_U2(f1, f2, a)
    plt.plot(f1, f2, 'ro')  # point rouge
    # Annotation avec f1, f2 et FWHM
    plt.text(f1 + 1, f2 + 1, f"({f1},{f2})\n R={fwhm_val:.3f}", 
             color='white', fontsize=7, weight='bold')

plt.tight_layout()
plt.show()


