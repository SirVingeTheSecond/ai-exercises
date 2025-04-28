import functools
import itertools


def multiply_vector_elements(vector):
    """Return the product of the vector elements."""
    def mult(x, y):
        return x * y
    return functools.reduce(mult, vector, 1)


class Variable(object):
    """Node in the network. Represents a binary random variable."""

    def __init__(self, name, assignments, probability_table, parents=None, children=None):
        """
        name:             string, e.g. 'DT'
        assignments:      tuple of possible values, e.g. ('T','F')
        probability_table:
          dict mapping parent‐assignment tuples → tuple of P(this='T'),P(this='F')
        parents:  list of parent Variable objects
        children: list of child  Variable objects (optional, for book‐keeping)
        """
        self.name = name
        # map value → index in the CPT rows
        self.assignments = { a: i for i, a in enumerate(assignments) }
        # validate
        for key, val in probability_table.items():
            if len(val) != len(assignments):
                raise ValueError(f"CPT row {key} has wrong length")
        self.probability_table = probability_table

        self.parents = parents[:] if parents else []
        self.children = children[:] if children else []

        # for caching marginals
        self.marginal_probabilities = [0.0] * len(assignments)
        self.ready = False

    def get_probability(self, value, parents_values):
        """P(this = value | parents = parents_values)."""
        row = self.probability_table[parents_values]
        return row[self.assignments[value]]

    def calculate_marginal_probability(self):
        """
        Compute and cache P(this = each possible value) by summing
        over all parent configurations.
        """
        if self.ready:
            return

        # ensure parents are ready first
        for p in self.parents:
            p.calculate_marginal_probability()

        # zero out
        for i in range(len(self.marginal_probabilities)):
            self.marginal_probabilities[i] = 0.0

        if not self.parents:
            # no parents: single entry
            probs = next(iter(self.probability_table.values()))
            for i, p in enumerate(probs):
                self.marginal_probabilities[i] = p
        else:
            # sum over every parent assignment
            for parent_vals, probs in self.probability_table.items():
                p_parents = 1.0
                for p_node, p_val in zip(self.parents, parent_vals):
                    p_parents *= p_node.get_marginal_probability(p_val)
                for i, p in enumerate(probs):
                    self.marginal_probabilities[i] += p * p_parents

        self.ready = True

    def get_marginal_probability(self, value):
        return self.marginal_probabilities[self.assignments[value]]

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parents.append(parent)

    def is_child_of(self, node):
        return node in self.parents


class BayesianNetwork(object):
    """Simple Bayesian network."""

    def __init__(self):
        self.variables = []
        self.varsMap = {}
        self.ready = False

    def set_variables(self, var_list):
        self.variables = var_list[:]
        self.varsMap = { v.name: v for v in var_list }
        self.ready = False

    def calculate_marginal_probabilities(self):
        for v in self.variables:
            v.calculate_marginal_probability()
        self.ready = True

    def get_marginal_probability(self, var_name, val):
        return self.varsMap[var_name].get_marginal_probability(val)

    def sub_vals(self, var, values):
        """Helper: build the tuple of parent‐values for `var` from `values` dict."""
        return tuple(values[p.name] for p in var.parents)

    def get_joint_probability(self, values):
        """
        P(all varName=values[varName]) = ∏ P(varName | its parents),
        using only those vars that appear in `values`.
        """
        p = 1.0
        for name, val in values.items():
            var = self.varsMap[name]
            pv = self.sub_vals(var, values)
            p *= var.get_probability(val, pv)
        return p

    def get_conditional_probability(self, query, evidence):
        """
        Compute P(query | evidence) by full enumeration.
        - query:    dict of exactly one variable → value, e.g. {'DT':'T'}
        - evidence: dict of observed vars → values
        """
        # only single‐variable queries supported here
        var = next(iter(query))
        if len(query) != 1:
            raise ValueError("Only single‐variable queries are supported")

        # Q[x_val] = sum_{all hidden vars} P(var=x_val, evidence)
        Q = {}
        for x_val in ('T','F'):
            ext = evidence.copy()
            ext[var] = x_val
            # which vars remain unassigned?
            missing = [v.name for v in self.variables if v.name not in ext]
            total = 0.0
            for combo in itertools.product(('T','F'), repeat=len(missing)):
                full = ext.copy()
                for name, val in zip(missing, combo):
                    full[name] = val
                total += self.get_joint_probability(full)
            Q[x_val] = total

        Z = Q['T'] + Q['F']
        return Q[query[var]] / Z


def print_marginal_probabilities(net):
    print("Marginal probabilities:")
    for v in net.variables:
        for a in v.assignments:
            print(f"  P({v.name}={a}) = {v.get_marginal_probability(a):.4f}")


def car_fault_network():
    # 1) CPTs for binary vars ('T','F')
    P_DT  = {():          (0.3,  0.7)}
    P_EM  = {():          (0.3,  0.7)}
    P_FTL = {():          (0.2,  0.8)}

    P_V   = {
        ('T',):         (0.7,  0.3),
        ('F',):         (0.1,  0.9),
    }

    P_SMS = {
        ('T','T'):      (0.05, 0.95),
        ('T','F'):      (0.6,  0.4),
        ('F','T'):      (0.3,  0.7),
        ('F','F'):      (0.7,  0.3),
    }

    P_HC  = {
        ('T','T','T'):  (0.9,  0.1),
        ('T','T','F'):  (0.8,  0.2),
        ('T','F','T'):  (0.3,  0.7),
        ('T','F','F'):  (0.2,  0.8),
        ('F','T','T'):  (0.6,  0.4),
        ('F','T','F'):  (0.5,  0.5),
        ('F','F','T'):  (0.1,  0.9),
        ('F','F','F'):  (0.01, 0.99),
    }

    # 2) Create the six nodes
    DT  = Variable('DT',  ('T','F'), P_DT)
    EM  = Variable('EM',  ('T','F'), P_EM)
    FTL = Variable('FTL', ('T','F'), P_FTL)

    V   = Variable('V',   ('T','F'), P_V,   parents=[DT])
    SMS = Variable('SMS', ('T','F'), P_SMS, parents=[DT, EM])
    HC  = Variable('HC',  ('T','F'), P_HC,  parents=[DT, EM, FTL])

    # 3) (optional) hook up children lists
    DT.add_child(V);   DT.add_child(SMS);  DT.add_child(HC)
    EM.add_child(SMS); EM.add_child(HC)
    FTL.add_child(HC)

    # 4) Build the BN in topological order
    net = BayesianNetwork()
    net.set_variables([DT, EM, FTL, V, SMS, HC])

    # 5) Precompute all marginals
    net.calculate_marginal_probabilities()

    # 6) Print them
    print_marginal_probabilities(net)
    print()

    # 7) Compute posteriors P(root=T | V=T, SMS=T, HC=F)
    obs = {'V':'T', 'SMS':'T', 'HC':'F'}
    for cause in ['DT','EM','FTL']:
        p = net.get_conditional_probability({cause:'T'}, obs)
        print(f"P({cause}=T | V=T, SMS=T, HC=F) = {p:.4f}")


if __name__ == '__main__':
    car_fault_network()
