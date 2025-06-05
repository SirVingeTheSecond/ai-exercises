"""
Lab 08 ▸ Homework — Car-Fault Bayesian Network
============================================
Calculate P(FTL=true | HC=true)
"""

from bn_template import Variable, BayesianNetwork

# Prior Probabilities ---------------------------------------------------- #
P_DT = {(): (0.3, 0.7)}  # P(DT=true)=0.3, P(DT=false)=0.7
P_EM = {(): (0.3, 0.7)}  # P(EM=true)=0.3, P(EM=false)=0.7
P_FTL = {(): (0.2, 0.8)}  # P(FTL=true)=0.2, P(FTL=false)=0.8

# Conditional Probability Tables ----------------------------------------- #
# P(V | DT)
P_V = {
    ("true",): (0.7, 0.3),  # P(V=true|DT=true)=0.7
    ("false",): (0.1, 0.9),  # P(V=true|DT=false)=0.1
}

# P(SMS | DT, EM)
P_SMS = {
    ("true", "true"): (0.05, 0.95),  # P(SMS=true|DT=T,EM=T)=0.05
    ("true", "false"): (0.6, 0.4),  # P(SMS=true|DT=T,EM=F)=0.6
    ("false", "true"): (0.3, 0.7),  # P(SMS=true|DT=F,EM=T)=0.3
    ("false", "false"): (0.7, 0.3),  # P(SMS=true|DT=F,EM=F)=0.7
}

# P(HC | DT, FTL, EM)
P_HC = {
    ("true", "true", "true"): (0.9, 0.1),  # P(HC=T|DT=T,FTL=T,EM=T)=0.9
    ("true", "true", "false"): (0.8, 0.2),  # P(HC=T|DT=T,FTL=T,EM=F)=0.8
    ("true", "false", "true"): (0.3, 0.7),  # P(HC=T|DT=T,FTL=F,EM=T)=0.3
    ("true", "false", "false"): (0.2, 0.8),  # P(HC=T|DT=T,FTL=F,EM=F)=0.2
    ("false", "true", "true"): (0.6, 0.4),  # P(HC=T|DT=F,FTL=T,EM=T)=0.6
    ("false", "true", "false"): (0.5, 0.5),  # P(HC=T|DT=F,FTL=T,EM=F)=0.5
    ("false", "false", "true"): (0.1, 0.9),  # P(HC=T|DT=F,FTL=F,EM=T)=0.1
    ("false", "false", "false"): (0.01, 0.99),  # P(HC=T|DT=F,FTL=F,EM=F)=0.01
}

# the nodes ----------------------------------------------- #
DT = Variable("DT", ("true", "false"), P_DT)
EM = Variable("EM", ("true", "false"), P_EM)
FTL = Variable("FTL", ("true", "false"), P_FTL)

V = Variable("V", ("true", "false"), P_V, [DT])
SMS = Variable("SMS", ("true", "false"), P_SMS, [DT, EM])
HC = Variable("HC", ("true", "false"), P_HC, [DT, FTL, EM])

# create Bayesian Network ------------------------------------------------ #
net = BayesianNetwork([DT, EM, FTL, V, SMS, HC])

# calculate P(FTL=true | HC=true) --------------------------------------- #
if __name__ == "__main__":
    # Question 21: What is P(FTL=true | HC=true)?
    evidence = {"HC": "true"}
    p_ftl_given_hc = net.query("FTL", "true", evidence)

    print("Question 21: Bayesian Network")
    print(f"P(FTL=true | HC=true) = {p_ftl_given_hc:.4f}")
    print(f"P(FTL=true | HC=true) ≈ {p_ftl_given_hc * 100:.0f}%")