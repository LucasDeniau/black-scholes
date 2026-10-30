import numpy as np


def _payoff(S_T, K, option_type):
    if option_type == "call":
        return np.maximum(S_T - K, 0)
    if option_type == "put":
        return np.maximum(K - S_T, 0)
    raise ValueError("option_type doit être 'call' ou 'put'")


def _simulate_ST(S, T, r, sigma, Z):
    """Prix final sous la probabilité risque-neutre (mouvement brownien géométrique)."""
    return S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)


def _summary(samples):
    """Prix, erreur standard et intervalle de confiance à 95 % d'un échantillon de prix actualisés."""
    price = samples.mean()
    std_error = samples.std(ddof=1) / np.sqrt(len(samples))
    return price, std_error, (price - 1.96 * std_error, price + 1.96 * std_error)


def monte_carlo_price(S, K, T, r, sigma, option_type="call",
                      n_simulations=100_000, seed=42, method="standard"):
    """
    Pricing Monte Carlo d'une option européenne.

    method :
      - "standard"    : tirages indépendants Z ~ N(0,1)
      - "antithetic"  : chaque tirage Z est associé à −Z (variables antithétiques)
      - "control"     : variable de contrôle X = e^(−rT)·S_T, d'espérance connue S

    Retourne (prix, erreur standard, intervalle de confiance à 95 %).
    Toutes les méthodes utilisent n_simulations trajectoires au total.
    """
    rng = np.random.default_rng(seed)
    discount = np.exp(-r * T)

    if method == "standard":
        Z = rng.standard_normal(n_simulations)
        Y = discount * _payoff(_simulate_ST(S, T, r, sigma, Z), K, option_type)
        return _summary(Y)

    if method == "antithetic":
        Z = rng.standard_normal(n_simulations // 2)
        Y_plus = discount * _payoff(_simulate_ST(S, T, r, sigma, Z), K, option_type)
        Y_minus = discount * _payoff(_simulate_ST(S, T, r, sigma, -Z), K, option_type)
        # On moyenne chaque paire : ce sont les paires qui sont indépendantes
        return _summary((Y_plus + Y_minus) / 2)

    if method == "control":
        Z = rng.standard_normal(n_simulations)
        S_T = _simulate_ST(S, T, r, sigma, Z)
        Y = discount * _payoff(S_T, K, option_type)
        X = discount * S_T                       # E[X] = S sous la probabilité risque-neutre
        b = np.cov(Y, X)[0, 1] / np.var(X, ddof=1)   # coefficient optimal
        return _summary(Y - b * (X - S))

    raise ValueError("method doit être 'standard', 'antithetic' ou 'control'")
