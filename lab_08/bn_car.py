from bn_template import Variable, BayesianNetwork

# ── priors ───────────────────────────────────────────────────────────────
P_DT  = {(): (0.3, 0.7)}   # Damaged Tire
P_EM  = {(): (0.3, 0.7)}   # Electronics Malfunction
P_FTL = {(): (0.2, 0.8)}   # Fuel-Tank Leak

# ── CPTs ─────────────────────────────────────────────────────────────────

# Vibrations
P_V = {
    ("true",):  (0.7, 0.3),   # DT = T
    ("false",): (0.1, 0.9),   # DT = F
}
# Slow Max Speed
P_SMS = {
    ("true",  "true"):  (0.05, 0.95),
    ("true",  "false"): (0.6,  0.4),
    ("false", "true"):  (0.3,  0.7),
    ("false", "false"): (0.7,  0.3),
}
# High Consumption
P_HC = {
    ("true",  "true",  "true"):  (0.9,  0.1),
    ("true",  "true",  "false"): (0.8,  0.2),
    ("true",  "false", "true"):  (0.3,  0.7),
    ("true",  "false", "false"): (0.2,  0.8),
    ("false", "true",  "true"):  (0.6,  0.4),
    ("false", "true",  "false"): (0.5,  0.5),
    ("false", "false", "true"):  (0.1,  0.9),
    ("false", "false", "false"): (0.01, 0.99),
}

# ── nodes ────────────────────────────────────────────────────────────────
DT  = Variable("DT",  ("true", "false"), P_DT)
EM  = Variable("EM",  ("true", "false"), P_EM)
FTL = Variable("FTL", ("true", "false"), P_FTL)

V   = Variable("V",   ("true", "false"), P_V,   [DT])
SMS = Variable("SMS", ("true", "false"), P_SMS, [DT, EM])
HC  = Variable("HC",  ("true", "false"), P_HC,  [DT, FTL, EM])

car_bn = BayesianNetwork([DT, EM, FTL, V, SMS, HC])

# ── run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    evidence = {"V": "true", "SMS": "true", "HC": "false"}
    for var in ("DT", "EM", "FTL"):
        p = car_bn.query(var, "true", evidence)
        print(f"P({var}=T | evidence) = {p:.3f}")
