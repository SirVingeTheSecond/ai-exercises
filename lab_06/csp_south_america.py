"""
Lab 06 ▸ Homework & Challenge — South-America Map-Colouring CSP
==============================================================
Run:
    python csp_south_america.py                 # plain backtracking
    python csp_south_america.py --fc            # + Forward-Checking
    python csp_south_america.py --fc --ac3      # + AC-3 preprocessing
"""

import argparse
from constraints_template import CSP, adj_constraint

countries = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador",
    "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela",
    "French_Guiana", "Falkland_Islands", "Sur_round"   # dummy to keep 15 vars
]

colours = ["R", "G", "B", "Y"]  # four-colour theorem

neigh = {
    "Argentina": ["Bolivia", "Brazil", "Chile", "Paraguay", "Uruguay"],
    "Bolivia":   ["Argentina", "Brazil", "Chile", "Paraguay", "Peru"],
    "Brazil":    ["Argentina", "Bolivia", "Colombia", "Guyana",
                  "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela",
                  "French_Guiana"],
    "Chile":     ["Argentina", "Bolivia", "Peru"],
    "Colombia":  ["Brazil", "Ecuador", "Peru", "Venezuela"],
    "Ecuador":   ["Colombia", "Peru"],
    "Guyana":    ["Brazil", "Suriname", "Venezuela"],
    "Paraguay":  ["Argentina", "Bolivia", "Brazil"],
    "Peru":      ["Bolivia", "Brazil", "Chile", "Colombia", "Ecuador"],
    "Suriname":  ["Brazil", "Guyana", "French_Guiana"],
    "Uruguay":   ["Argentina", "Brazil"],
    "Venezuela": ["Brazil", "Colombia", "Guyana"],
    "French_Guiana": ["Brazil", "Suriname"],
    "Falkland_Islands": [],     # no neighbours
    "Sur_round": []             # dummy isolated node to keep variable count
}

domains = {c: colours[:] for c in countries}

def create_sa_csp() -> CSP:
    return CSP(countries, domains, neigh, adj_constraint)

# ---------------------------------------------------------------------------
def solve(fc=False, ac3=False):
    csp = create_sa_csp()
    sol = csp.backtracking_search(forward_check=fc, use_ac3=ac3)
    print("Solution:", sol)
    print("Nodes expanded:", csp.steps)

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--fc", action="store_true", help="Enable Forward-Checking")
    p.add_argument("--ac3", action="store_true", help="Enable AC-3 preprocessing")
    args = p.parse_args()
    solve(fc=args.fc, ac3=args.ac3)
