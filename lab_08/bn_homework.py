"""
Lab 08 ▸ Homework — Car-Fault Bayesian Network
============================================
CPTs from Lab 08.pdf (note SMS true-prob = 0.95 when DT ∧ EM).
Posterior with evidence V∧SMS∧¬HC:
    P(DT=true)  ≈ 0.6561
    P(EM=true)  ≈ 0.0340
    P(FTL=true) ≈ 0.1806
"""

from bn_template import Variable, BayesianNetwork

# ── Priors ----------------------------------------------------------------- #
P_DT  = {(): (0.3, 0.7)}
P_EM  = {(): (0.3, 0.7)}
P_FTL = {(): (0.2, 0.8)}

# ── Conditionals ----------------------------------------------------------- #
P_V = {
    ("true",):  (0.7, 0.3),
    ("false",): (0.1, 0.9),
}
P_SMS = {
    ("true", "true"):  (0.95, 0.05),   # DT=T, EM=T <- 0.95 per PDF
    ("true", "false"): (0.60, 0.40),
    ("false","true"):  (0.30, 0.70),
    ("false","false"): (0.70, 0.30),
}
P_HC = {
    ("true","true","true"):   (0.90, 0.10),
    ("true","true","false"):  (0.80, 0.20),
    ("true","false","true"):  (0.30, 0.70),
    ("true","false","false"): (0.20, 0.80),
    ("false","true","true"):  (0.60, 0.40),
    ("false","true","false"): (0.50, 0.50),
    ("false","false","true"): (0.10, 0.90),
    ("false","false","false"):(0.01, 0.99),
}

# ── Nodes (topological order) --------------------------------------------- #
DT  = Variable("DT",  ("true","false"), P_DT)
EM  = Variable("EM",  ("true","false"), P_EM)
FTL = Variable("FTL", ("true","false"), P_FTL)

V   = Variable("V",   ("true","false"), P_V,   [DT])
SMS = Variable("SMS", ("true","false"), P_SMS, [DT, EM])
HC  = Variable("HC",  ("true","false"), P_HC,  [DT, FTL, EM])

net = BayesianNetwork([DT, EM, FTL, V, SMS, HC])

# ── Posterior demo --------------------------------------------------------- #
if __name__ == "__main__":
    evidence = {"V":"true", "SMS":"true", "HC":"false"}
    for var in ("DT", "EM", "FTL"):
        p = net.query(var, "true", evidence)
        print(f"P({var}=true | V∧SMS∧¬HC) = {p:.4f}")
