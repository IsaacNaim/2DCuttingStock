from ortools.linear_solver import pywraplp

def cutting_stock_or_tools(stud_dict):
    results = {}
    
    for key, items in stud_dict.items():
        # Extract lengths and quantities
        w = [item[0] for item in items]
        q = [item[1] for item in items]
        
        # Determine the standard stud length
        standard_length = int(key.split('x')[-1]) * 12
        
        print(f"\nProcessing {key} with standard length {standard_length}")

        # Initialize the solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            raise Exception("Solver not created.")
        
        # Create variables
        x = []
        for i in range(len(w)):
            x.append(solver.IntVar(0, q[i], f'x[{i}]'))
        
        # Create the objective function
        objective = solver.Objective()
        for i in range(len(w)):
            objective.SetCoefficient(x[i], 1)
        objective.SetMinimization()
        
        # Create constraints
        for i in range(len(w)):
            constraint = solver.Constraint(q[i], solver.infinity())
            constraint.SetCoefficient(x[i], w[i])
        
        # Create the width constraint
        width_constraint = solver.Constraint(0, standard_length)
        for i in range(len(w)):
            width_constraint.SetCoefficient(x[i], w[i])
        
        # Solve the problem
        status = solver.Solve()
        
        if status != pywraplp.Solver.OPTIMAL:
            print(f"No feasible solution found for {key}.")
            continue
        
        # Collect results
        rolls = []
        for i in range(len(w)):
            if x[i].solution_value() > 0:
                roll = sorted([w[i]] * int(x[i].solution_value()))
                rolls.append(roll)
        
        rolls.sort()
        results[key] = rolls
    
    return results
