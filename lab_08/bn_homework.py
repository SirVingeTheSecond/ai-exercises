"""
Lab 08 ▸ Homework — Car-Fault Bayesian Network
============================================
Calculate P(FTL=true | HC=true)
"""

from bn_template import Variable, BayesianNetwork

# root ----------------------------------------------------------- #
P_FLU  = {(): (0.4, 0.6)}
P_COLD = {(): (0.043, 0.957)}

# conditionals ---------------------------------------------------------- #
# FEVER depends on FLU
P_FEVER = {
    ("true",):  (0.5, 0.5),   # FLU = true
    ("false",): (0.06, 0.94), # FLU = false
}

# COUGH  and FATIGUE depend on (FLU, COLD)
P_COUGH = {
    ("false", "false"): (0.1, 0.9),
    ("false", "true"):  (0.6, 0.4),
    ("true",  "false"): (0.3, 0.7),
    ("true",  "true"):  (0.99, 0.01),
}
P_FATIGUE = {
    ("false", "false"): (0.5, 0.5),
    ("false", "true"):  (0.3, 0.7),
    ("true",  "false"): (0.6, 0.4),
    ("true",  "true"):  (0.83, 0.17),
}

# nodes ----------------------------------------------------------------- #
FLU     = Variable("FLU",     ("true", "false"), P_FLU)
COLD    = Variable("COLD",    ("true", "false"), P_COLD)
FEVER   = Variable("FEVER",   ("true", "false"), P_FEVER,  [FLU])
COUGH   = Variable("COUGH",   ("true", "false"), P_COUGH,  [FLU, COLD])
FATIGUE = Variable("FATIGUE", ("true", "false"), P_FATIGUE,[FLU, COLD])

# network --------------------------------------------------------------- #
net = BayesianNetwork([FLU, COLD, FEVER, COUGH, FATIGUE])

# run ----------------------------------------------------------------- #
if __name__ == "__main__":
    evidence = {"FEVER": "true", "COUGH": "false"}
    p = net.query("FLU", "true", evidence)
    print(f"P(FLU = true | FEVER = T, COUGH = F) = {p:.4f}")
