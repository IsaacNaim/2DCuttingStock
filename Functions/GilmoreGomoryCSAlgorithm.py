import gurobipy as gp
from gurobipy import GRB, Model, Column, quicksum

EPS = 1e-6

def ggcutting_stock_algorithm(stud_dict):
    results = {}

    for key, items in stud_dict.items():
        # Extract lengths and quantities
        w = [item[0] for item in items]
        q = [item[1] for item in items]
        
        # Determine the standard stud length
        standard_length = int(key.split('x')[-1]) * 12000

        print(f"\nProcessing {key} with standard length {standard_length}")

        # Initialize the master problem
        master = Model("master")
        master.setParam('OutputFlag', 0)
        
        orders = []
        for i in range(len(w)):
            var = master.addVar(vtype="I", name=f"x[{i}]")
            orders.append(master.addConstr(quicksum(w[i] * var for i in range(len(w))) >= q[i], f"order[{i}]"))

        master.setObjective(quicksum(master.getVars()), GRB.MINIMIZE)
        master.update()

        t = []
        K = 0
        x = {}

        while True:
            relax = master.relax()
            relax.optimize()
            pi = [c.Pi for c in relax.getConstrs()]
            knapsack = Model("KP")
            knapsack.setParam('OutputFlag', 0)
            knapsack.ModelSense = -1
            y = {}

            for i in range(len(w)):
                y[i] = knapsack.addVar(ub=q[i], vtype="I", name=f"y[{i}]")
            knapsack.update()
            knapsack.addConstr(quicksum(w[i] * y[i] for i in range(len(w))) <= standard_length, "width")
            knapsack.setObjective(quicksum(pi[i] * y[i] for i in range(len(w))), GRB.MAXIMIZE)
            knapsack.optimize()

            if knapsack.status != GRB.Status.OPTIMAL:
                print(f"Knapsack problem not solved optimally for {key}. Status: {knapsack.status}")
                break

            if knapsack.ObjVal < 1 + EPS:
                print(f"No feasible pattern found for {key} with standard length {standard_length}")
                break

            pat = [int(y[i].X + 0.5) for i in y]
            print(f"Pattern found: {pat}")
            t.append(pat)
            col = Column()
            for i in range(len(w)):
                if t[K][i] > 0:
                    col.addTerms(t[K][i], orders[i])
            x[K] = master.addVar(obj=1, vtype="I", name=f"x[{K}]", column=col)
            master.update()
            K += 1

        master.optimize()
        if master.status != GRB.Status.OPTIMAL:
            print(f"Master problem not solved optimally for {key}. Status: {master.status}")
            continue

        rolls = []
        for k in x:
            for j in range(int(x[k].X + .5)):
                roll = sorted([w[i] for i in range(len(w)) if t[k][i] > 0 for _ in range(t[k][i])])
                rolls.append(roll)
        
        rolls.sort()
        results[key] = rolls

    return results
