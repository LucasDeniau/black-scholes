import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes, greeks

def plot_price_vs_spot(K=100, T=1, r=0.05, sigma=0.2):
    """Prix call et put en fonction du prix spot."""
    spots = np.linspace(50, 150, 300)

    call_prices = [black_scholes(s, K, T, r, sigma, "call") for s in spots]
    put_prices  = [black_scholes(s, K, T, r, sigma, "put")  for s in spots]

    plt.figure(figsize=(8, 4))
    plt.plot(spots, call_prices, label="Call", color="steelblue")
    plt.plot(spots, put_prices,  label="Put",  color="tomato")
    plt.axvline(K, linestyle="--", color="gray", alpha=0.6, label=f"Strike K={K}")
    plt.xlabel("Prix du sous-jacent S")
    plt.ylabel("Prix de l'option")
    plt.title("Prix Black-Scholes en fonction du spot")
    plt.legend()
    plt.tight_layout()
    plt.savefig("price_vs_spot.png", dpi=150)
    plt.show()

def plot_delta_vs_spot(K=100, T=1, r=0.05, sigma=0.2):
    """Delta en fonction du spot — montre la convergence vers 0 ou 1."""
    spots = np.linspace(50, 150, 300)

    call_deltas = [greeks(s, K, T, r, sigma, "call")["delta"] for s in spots]
    put_deltas  = [greeks(s, K, T, r, sigma, "put")["delta"]  for s in spots]

    plt.figure(figsize=(8, 4))
    plt.plot(spots, call_deltas, label="Delta Call", color="steelblue")
    plt.plot(spots, put_deltas,  label="Delta Put",  color="tomato")
    plt.axvline(K, linestyle="--", color="gray", alpha=0.6, label=f"Strike K={K}")
    plt.axhline(0, linestyle=":",  color="black", alpha=0.3)
    plt.xlabel("Prix du sous-jacent S")
    plt.ylabel("Delta")
    plt.title("Delta en fonction du spot")
    plt.legend()
    plt.tight_layout()
    plt.savefig("delta_vs_spot.png", dpi=150)
    plt.show()

def plot_price_vs_volatility(S=100, K=100, T=1, r=0.05):
    """Prix en fonction de la volatilité — montre que vega est toujours positif."""
    vols = np.linspace(0.05, 0.6, 300)

    call_prices = [black_scholes(S, K, T, r, v, "call") for v in vols]
    put_prices  = [black_scholes(S, K, T, r, v, "put")  for v in vols]

    plt.figure(figsize=(8, 4))
    plt.plot(vols * 100, call_prices, label="Call", color="steelblue")
    plt.plot(vols * 100, put_prices,  label="Put",  color="tomato")
    plt.xlabel("Volatilité σ (%)")
    plt.ylabel("Prix de l'option")
    plt.title("Prix en fonction de la volatilité")
    plt.legend()
    plt.tight_layout()
    plt.savefig("price_vs_vol.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    plot_price_vs_spot()
    plot_delta_vs_spot()
    plot_price_vs_volatility()