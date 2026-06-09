from black_scholes import black_scholes, greeks
from monte_carlo import monte_carlo_price

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

for opt in ["call", "put"]:
    bs_price            = black_scholes(S, K, T, r, sigma, opt)
    mc_price, (lo, hi)  = monte_carlo_price(S, K, T, r, sigma, opt)
    g                   = greeks(S, K, T, r, sigma, opt)

    print(f"\n── {opt.upper()} ──")
    print(f"  Black-Scholes : {bs_price:.4f}")
    print(f"  Monte Carlo   : {mc_price:.4f}  [IC 95%: {lo:.4f} – {hi:.4f}]")
    print(f"  Erreur        : {abs(bs_price - mc_price):.6f}")
    print(f"  Delta  : {g['delta']:.4f}")
    print(f"  Gamma  : {g['gamma']:.4f}")
    print(f"  Theta  : {g['theta']:.4f}  (par jour)")
    print(f"  Vega   : {g['vega']:.4f}   (pour +1% de vol)")
    print(f"  Rho    : {g['rho']:.4f}   (pour +1% de taux)")