import numpy as np

def monte_carlo_price(S, K, T, r, sigma, option_type="call", n_simulations=100_000, seed=42):
    """
    Pricing Monte Carlo d'une option européenne.
    
    n_simulations : nombre de trajectoires simulées
    seed          : pour la reproductibilité
    """
    rng = np.random.default_rng(seed)

    # Tirage de n variables normales standard
    Z = rng.standard_normal(n_simulations)

    # Prix final simulé pour chaque trajectoire
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Payoff à maturité
    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - S_T, 0)
    else:
        raise ValueError("option_type doit être 'call' ou 'put'")

    # Actualisation et moyenne
    price = np.exp(-r * T) * np.mean(payoffs)

    # Intervalle de confiance à 95%
    std_error = np.std(payoffs) / np.sqrt(n_simulations)
    ci_lower  = np.exp(-r * T) * (np.mean(payoffs) - 1.96 * std_error)
    ci_upper  = np.exp(-r * T) * (np.mean(payoffs) + 1.96 * std_error)

    return price, (ci_lower, ci_upper)