import numpy as np
from black_scholes import black_scholes, greeks
from monte_carlo import monte_carlo_price

# Paramètres
S, K, T, r, sigma = 100, 100, 1, 0.05, 0.20

# ── PRIX ANALYTIQUES ─────────────────────────────────────
call = black_scholes(S, K, T, r, sigma, "call")
put = black_scholes(S, K, T, r, sigma, "put")
print(f"\n── Black-Scholes (S={S}, K={K}, T={T}, r={r:.0%}, σ={sigma:.0%}) ──")
print(f"  Call : {call:.4f}")
print(f"  Put  : {put:.4f}")

# ── PARITÉ CALL-PUT : C − P = S − K·e^(−rT) ─────────────
lhs, rhs = call - put, S - K * np.exp(-r * T)
print(f"\n── Parité call-put ──")
print(f"  C − P          : {lhs:.6f}")
print(f"  S − K·e^(−rT)  : {rhs:.6f}")
print(f"  Écart          : {abs(lhs - rhs):.2e}")

# ── GREEKS ───────────────────────────────────────────────
g_call, g_put = greeks(S, K, T, r, sigma, "call"), greeks(S, K, T, r, sigma, "put")
print(f"\n── Greeks ──")
print(f"  {'':<7}{'Call':>10}{'Put':>10}")
for name in ["delta", "gamma", "theta", "vega", "rho"]:
    print(f"  {name:<7}{g_call[name]:>10.4f}{g_put[name]:>10.4f}")

# ── VÉRIFICATION DES GREEKS PAR DIFFÉRENCES FINIES ───────
h = 1e-4
bs = lambda **kw: black_scholes(**{**dict(S=S, K=K, T=T, r=r, sigma=sigma, option_type="call"), **kw})
fd = {
    "delta": (bs(S=S + h) - bs(S=S - h)) / (2 * h),
    "gamma": (bs(S=S + 1e-2) - 2 * call + bs(S=S - 1e-2)) / 1e-4,
    "theta": -(bs(T=T + h) - bs(T=T - h)) / (2 * h) / 365,   # le temps restant diminue
    "vega": (bs(sigma=sigma + h) - bs(sigma=sigma - h)) / (2 * h) / 100,
    "rho": (bs(r=r + h) - bs(r=r - h)) / (2 * h) / 100,
}
print(f"\n── Vérification des Greeks du call (différences finies) ──")
print(f"  {'':<7}{'Formule':>10}{'Num.':>10}")
for name, value in fd.items():
    print(f"  {name:<7}{g_call[name]:>10.4f}{value:>10.4f}")

# ── MONTE CARLO ET RÉDUCTION DE VARIANCE ─────────────────
N = 100_000
for option_type, exact in [("call", call), ("put", put)]:
    print(f"\n── Monte Carlo — {option_type} ({N:,} trajectoires, prix exact {exact:.4f}) ──")
    print(f"  {'Méthode':<12}{'Prix':>9}{'Err. std':>10}{'IC 95 %':>20}{'Dans IC':>9}")
    for method in ["standard", "antithetic", "control"]:
        price, se, (lo, hi) = monte_carlo_price(S, K, T, r, sigma, option_type, N, method=method)
        inside = "oui" if lo <= exact <= hi else "non"
        print(f"  {method:<12}{price:>9.4f}{se:>10.4f}   [{lo:.4f} ; {hi:.4f}]{inside:>6}")
