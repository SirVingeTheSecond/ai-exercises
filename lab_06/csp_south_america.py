from random import shuffle

class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[variable]

        return None

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True

def create_south_america_csp():
    # List of South American countries
    variables = [
        'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa Rica',
        'Ecuador', 'Guyana', 'Guyane', 'Panama', 'Paraguay', 'Peru', 'Suriname',
        'Uruguay', 'Venezuela'
    ]

    # Possible colors
    values = ['Red', 'Green', 'Blue', 'Yellow']

    # Assigning domains for each country
    domains = {country: values[:] for country in variables}

    # Neighbors of each country
    neighbours = {
        'Argentina': ['Bolivia', 'Brazil', 'Chile', 'Paraguay', 'Uruguay'],
        'Bolivia': ['Argentina', 'Brazil', 'Chile', 'Paraguay', 'Peru'],
        'Brazil': ['Argentina', 'Bolivia', 'Colombia', 'Guyana', 'Guyane', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'],
        'Chile': ['Argentina', 'Bolivia', 'Peru'],
        'Colombia': ['Brazil', 'Ecuador', 'Peru', 'Venezuela'],
        'Costa Rica': ['Panama'],
        'Ecuador': ['Colombia', 'Peru'],
        'Guyana': ['Brazil', 'Suriname', 'Venezuela'],
        'Guyane': ['Brazil', 'Suriname'],
        'Panama': ['Colombia'],
        'Paraguay': ['Argentina', 'Bolivia', 'Brazil'],
        'Peru': ['Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador'],
        'Suriname': ['Brazil', 'Guyana', 'Guyane'],
        'Uruguay': ['Argentina', 'Brazil'],
        'Venezuela': ['Brazil', 'Colombia', 'Guyana']
    }

    # Constraint: No two neighboring countries can have the same color
    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    # Assign the constraint to every country
    constraints = {country: constraint_function for country in variables}

    return CSP(variables, domains, neighbours, constraints)

if __name__ == '__main__':
    south_america = create_south_america_csp()
    result = south_america.backtracking_search()
    if result:
        for country, color in sorted(result.items()):
            print(f"{country}: {color}")
    else:
        print("No solution found.")
