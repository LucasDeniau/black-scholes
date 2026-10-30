# Black-Scholes Option Pricing Engine

> Analytical pricing of European options with full Greeks, numerical validation, and Monte Carlo pricing with variance reduction.

---

## Overview

For my first quantitative finance project, I implemented the Black-Scholes model from scratch in Python, the cornerstone of derivatives pricing. Everything is built manually: closed-form pricing of European calls and puts, the five Greeks, and a Monte Carlo engine with variance reduction techniques.

Every result is cross-checked: put-call parity, finite-difference Greeks, and Monte Carlo confidence intervals against the analytical prices.

---

## Theory

### Model

Under the risk-neutral measure, the underlying follows a **Geometric Brownian Motion**:

$$S_T = S_0 \cdot \exp\left(\left(r - \frac{\sigma^2}{2}\right)T + \sigma\sqrt{T}\,Z\right), \quad Z \sim \mathcal{N}(0,1)$$

Because the option can be replicated by a continuously rebalanced portfolio of the underlying and cash, its price does not depend on the expected return of the stock: it is the discounted expected payoff under the risk-neutral measure.

### Black-Scholes Formula

$$C = S \cdot N(d_1) - K e^{-rT} N(d_2), \qquad P = K e^{-rT} N(-d_2) - S \cdot N(-d_1)$$

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)\,T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

$N(d_2)$ is the risk-neutral probability that the call ends in the money, and $N(d_1)$ is the call delta.

Prices satisfy **put-call parity**: $C - P = S - K e^{-rT}$.

### Greeks

| Greek       | Measures sensitivity to   | Formula (call)                                    |
|-------------|---------------------------|---------------------------------------------------|
| **Δ Delta** | Underlying price S        | N(d₁)                                             |
| **Γ Gamma** | Rate of change of Delta   | N'(d₁) / (S·σ·√T)                                 |
| **Θ Theta** | Time decay (per day)      | [−S·N'(d₁)·σ/(2√T) − r·K·e^(−rT)·N(d₂)] / 365     |
| **V Vega**  | Volatility σ (per +1 pt)  | S·N'(d₁)·√T / 100                                 |
| **ρ Rho**   | Interest rate r (per +1 pt)| K·T·e^(−rT)·N(d₂) / 100                          |

The Greeks are linked by the Black-Scholes PDE: $\Theta + \frac{1}{2}\sigma^2 S^2 \Gamma + rS\Delta - rC = 0$ — a long-gamma position pays for its convexity through time decay.

### Monte Carlo & Variance Reduction

The price is estimated by averaging discounted payoffs over N simulated values of $S_T$:

$$\hat{C} = e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \max(S_T^{(i)} - K,\ 0)$$

By the Central Limit Theorem, the standard error decreases as $O(1/\sqrt{N})$, and a 95% confidence interval is $\hat{C} \pm 1.96 \cdot \text{SE}$. Two variance reduction techniques are implemented:

- **Antithetic variates**: each draw $Z$ is paired with $-Z$, which induces negative correlation between paired payoffs.
- **Control variate**: $X = e^{-rT} S_T$ has a known expectation $S_0$; the estimator $\bar{Y} - b(\bar{X} - S_0)$, with optimal $b = \text{Cov}(Y,X)/\text{Var}(X)$, removes the part of the noise explained by the underlying.

---

## Results

Parameters: **S = 100, K = 100, T = 1y, r = 5%, σ = 20%**

### Analytical Prices

| Option | Price       |
|--------|-------------|
| Call   | **10.4506** |
| Put    | **5.5735**  |

Put-call parity check: $C - P = S - Ke^{-rT} = 4.877058$ (difference < $10^{-10}$).

### Greeks

| Greek     | Call    | Put     | Interpretation                                   |
|-----------|---------|---------|--------------------------------------------------|
| **Delta** | +0.6368 | −0.3632 | Call gains ≈ 0.64 per +1 on the underlying       |
| **Gamma** | 0.0188  | 0.0188  | Delta increases by ≈ 0.019 per +1 on S           |
| **Theta** | −0.0176 | −0.0045 | Call loses ≈ 1.8 cents per day (time decay)      |
| **Vega**  | +0.3752 | +0.3752 | Both gain ≈ 0.38 per +1 volatility point         |
| **Rho**   | +0.5323 | −0.4189 | Call gains ≈ 0.53 per +1 interest rate point     |

All closed-form Greeks match central finite-difference approximations to 4 decimal places.

### Monte Carlo (100,000 paths)

**Call** (exact price 10.4506)

| Method          | Price   | Std. error | 95% CI               |
|-----------------|---------|------------|----------------------|
| Standard        | 10.4205 | 0.0468     | [10.3289 ; 10.5122]  |
| Antithetic      | 10.4673 | 0.0331     | [10.4025 ; 10.5321]  |
| Control variate | 10.4668 | 0.0179     | [10.4318 ; 10.5019]  |

**Put** (exact price 5.5735)

| Method          | Price  | Std. error | 95% CI             |
|-----------------|--------|------------|--------------------|
| Standard        | 5.6122 | 0.0275     | [5.5583 ; 5.6661]  |
| Antithetic      | 5.5797 | 0.0210     | [5.5384 ; 5.6209]  |
| Control variate | 5.5898 | 0.0179     | [5.5548 ; 5.6248]  |

The analytical price lies within every 95% confidence interval. For the call, the control variate divides the standard error by **2.6** — equivalent to running about **7× more simulations** at the same cost.

### Sensitivity Analysis

![Price vs Spot](price_vs_spot.png)
*Call and put prices as a function of the underlying spot price.*

![Delta vs Spot](delta_vs_spot.png)
*Call delta → 1 deep in-the-money, → 0 deep out-of-the-money.*

![Price vs Volatility](price_vs_vol.png)
*Both call and put prices increase with volatility — Vega is always positive.*

### Limitations

- **Constant volatility**: market implied volatility varies with strike and maturity (smile / skew); local or stochastic volatility models (e.g. Heston) address this.
- **No jumps**: crashes create discontinuous moves not captured by a Brownian motion.
- **Continuous, frictionless hedging**: in practice, delta hedging is discrete and incurs transaction costs.
- **European exercise only**: American options require binomial trees or finite-difference methods.

---

## Project Structure

```
black-scholes/
├── black_scholes.py   # Closed-form pricing + Greeks
├── monte_carlo.py     # Monte Carlo pricing: standard, antithetic, control variate
├── plots.py           # Sensitivity visualizations
└── main.py            # Prices, parity check, Greeks validation, Monte Carlo comparison
```

---

## Usage

```bash
# Install dependencies
pip install numpy scipy matplotlib

# Run pricing, checks and Monte Carlo comparison
python main.py

# Generate sensitivity plots
python plots.py
```

---

## References

- Black, F. & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities*. Journal of Political Economy.
- Hull, J. (2022). *Options, Futures, and Other Derivatives* (11th ed.). Pearson.
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
