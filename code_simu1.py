import numpy as np
import matplotlib.pyplot as plt

def rect(x):
    return np.where(np.abs(x) <= 0.5, 1.0, 0.0)

def U0(x, y=0, a=50e-6):
    """Champ incident au plan objet : fente de largeur a."""
    return rect(x / a)

def fourier_transform(func, nu, x_min=-1e-4, x_max=1e-4, N=10000):
    """
    Implémentation numérique de la transformée de Fourier.
    Calcule ∫ func(x) exp(-i 2π nu x) dx approximativement par somme de Riemann.
    nu peut être un scalaire ou un tableau numpy.
    """
    x = np.linspace(x_min, x_max, N)
    dx = x[1] - x[0]
    values = func(x)
    # nu = np.atleast_1d(nu)  # Assure que nu est un tableau 1D
    exp_term = np.exp(-1j * 2 * np.pi * nu[:, None] * x[None, :])
    ft_values = np.sum(values[None, :] * exp_term, axis=1) * dx
    if len(ft_values) == 1:
        return ft_values[0]
    return ft_values

def M(x, Lambda=1e-6, N=100, beta=0.0):
    """
    Modélisation du réseau de diffraction blazé (1D en x).
    M(x) = [comb(x/Λ) ∗ (rect(x/Λ) e^{i β x})] * rect(x / (N Λ))
    Implémenté comme somme sur k des contributions des rainures.
    x peut être un scalaire ou un tableau numpy.
    """
    m = np.zeros_like(x, dtype=complex)
    k_min = -int(N // 2)
    k_max = int(N // 2)
    for k in range(k_min, k_max + 1):
        shifted_x = x - k * Lambda
        rect_val = rect(shifted_x / Lambda)
        phase = np.exp(1j * beta * shifted_x)
        m += rect_val * phase
    overall_rect = rect(x / (N * Lambda))
    m *= overall_rect
    if len(m) == 1:
        return m[0]
    return m

def U1(x1, y1=0, a=50e-6, lambda_=500e-9, f=0.1, Lambda=1e-6, N=100, beta=0.0):
    """
    Champ au centre du corrélateur 4F (plan de Fourier) avec masque M (1D en x).
    U1(x1) ∝ M(x1) * F{U0}(x1 / (λ f))
    λ et f sont des valeurs par défaut typiques (500 nm, focale 10 cm).
    Ajout des paramètres pour le réseau : Λ (pas), N (nombre de périodes), β (paramètre de blaze).
    """
    nu = x1 / (lambda_ * f)
    ft = fourier_transform(lambda x: U0(x, y=0, a=a), nu)
    m_val = M(x1, Lambda=Lambda, N=N, beta=beta)
    return m_val * ft

def U2(x2, y2=0, a=50e-6, lambda_=500e-9, f=0.1, Lambda=1e-6, N=100, beta=0.0):
    """
    Champ en sortie du corrélateur 4F (1D en x).
    U2(x2) ∝ F{U1}(x2 / (λ f))
    λ et f sont des valeurs par défaut typiques (500 nm, focale 10 cm).
    Ajout des paramètres pour le réseau : Λ (pas), N (nombre de périodes), β (paramètre de blaze).
    Utilise une plage plus large pour x1 car le plan de Fourier a une échelle différente.
    """
    nu = x2 / (lambda_ * f)
    x1_min = -5e-3  # -5 mm à 5 mm pour capturer la diffusion au plan de Fourier
    x1_max = 5e-3
    N_points = 20000  # Plus de points pour une meilleure précision
    return fourier_transform(
        lambda x1: U1(x1, y1=0, a=a, lambda_=lambda_, f=f, Lambda=Lambda, N=N, beta=beta),
        nu,
        x_min=x1_min,
        x_max=x1_max,
        N=N_points
    )


# Axe x2 dans le plan de sortie
x2 = np.linspace(-1e-3, 1e-3, 2000)  # 2 mm centré sur l'axe

# Calculer le champ U2
U2_values = U2(x2, a=50e-6, lambda_=500e-9, f=0.1, Lambda=1e-6, N=100, beta=0.0)

# Tracer l'intensité |U2|^2
plt.figure(figsize=(8,4))
plt.plot(x2*1e3, np.abs(U2_values)**2)  # x2 en mm
plt.xlabel("x2 (mm)")
plt.ylabel("Intensité |U2|^2")
plt.title("Champ en sortie du corrélateur 4F")
plt.grid(True)
plt.show()
