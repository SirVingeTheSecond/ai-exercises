from csp_south_america import create_sa_csp
csp = create_sa_csp()
solution = csp.backtracking_search(forward_check=True, use_ac3=True)

# quick check
assert all(
    solution[A] != solution[B]
    for A in csp.N
    for B in csp.N[A]
), "Invalid colouring!"

print("Looks good:", solution)
