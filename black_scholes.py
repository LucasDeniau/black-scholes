import numpy as np
from scipy.stats import norm

def d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1, d2 = d1_d2(S, K, T, r, sigma)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type doit être 'call' ou 'put'")

    return price

def greeks(S, K, T, r, sigma, option_type="call"):
    d1, d2 = d1_d2(S, K, T, r, sigma)

    # N'(d1) — la densité, pas la répartition
    nprime_d1 = norm.pdf(d1)

    # Delta
    if option_type == "call":
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1

    # Gamma (identique call/put)
    gamma = nprime_d1 / (S * sigma * np.sqrt(T))

    # Theta (on divise par 365 pour avoir par jour)
    if option_type == "call":
        theta = (- S * nprime_d1 * sigma / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    else:
        theta = (- S * nprime_d1 * sigma / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

    # Vega (identique call/put) — on divise par 100 : sensibilité à 1% de vola
    vega = S * nprime_d1 * np.sqrt(T) / 100

    # Rho — on divise par 100 : sensibilité à 1% de taux
    if option_type == "call":
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega":  vega,
        "rho":   rho
    }