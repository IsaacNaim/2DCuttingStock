from ortools.linear_solver import pywraplp

def or_cuttingstock(stud_dict):
    results = {}

    for key, items in stud_dict.items():
        # Extract lengths and quantities
        lengths = [item[0] for item in items]
        quantities = [item[1] for item in items]
        
        # Determine the standard stud length
        standard_length = int(key.split('x')[-1]) * 12
        print(f"\nProcessing {key} with standard length {standard_length}")

        num_items = len(lengths)
        num_patterns = 100  # Set a high enough number of patterns to generate
        
        # Initialize the solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            raise Exception('Solver not created.')

        print("Solver created successfully")

        # Create variables for patterns
        pattern_vars = []
        for i in range(num_patterns):
            pattern_vars.append(solver.IntVar(0, solver.infinity(), f'pattern_{i}'))
            print(f"Pattern variable created: pattern_{i}")

        # Constraints to ensure all required quantities are met
        for i in range(num_items):
            constraint = solver.Constraint(quantities[i], solver.infinity())
            for j in range(num_patterns):
                constraint.SetCoefficient(pattern_vars[j], lengths[i])
            print(f"Constraint added for item {i} with length {lengths[i]} and quantity {quantities[i]}")

        # Constraints to ensure patterns are within the standard length
        for j in range(num_patterns):
            pattern_length = solver.Sum(pattern_vars[j] * lengths[i] for i in range(num_items))
            constraint = solver.Constraint(0, standard_length)
            constraint.SetCoefficient(pattern_length, 1)
            print(f"Constraint added for pattern {j} with total length <= {standard_length}")

        # Objective: Minimize the number of patterns used
        solver.Minimize(solver.Sum(pattern_vars))
        print("Objective set to minimize the number of patterns used")

        # Solve the problem
        print("Starting solver...")
        status = solver.Solve()
        print(f"Solve status: {status}")

        if status == pywraplp.Solver.OPTIMAL:
            print('Optimal Solution found:')
            patterns = [pattern_vars[i].solution_value() for i in range(num_patterns)]
            used_patterns = [i for i, p in enumerate(patterns) if p > 0]
            print(f"Patterns used: {used_patterns}")
            results[key] = used_patterns
        else:
            print(f'No optimal solution found for {key}. Status: {status}')

    return results
