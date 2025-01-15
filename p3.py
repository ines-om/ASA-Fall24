from pulp import *

def solve_toy_distribution():
    try:
        # Read initial parameters
        n, m, t = map(int, input().strip().split())
        if n <= 0 or m <= 0 or t <= 0:
            print(-1)
            return

        # Create problem
        prob = LpProblem("toy_distribution", LpMaximize)
        
        # Read factory data
        factory_stock = {}
        factory_country = {}
        for _ in range(n):
            f_id, c_id, stock = map(int, input().strip().split())
            if stock < 0:
                print(-1)
                return
            factory_stock[f_id] = stock
            factory_country[f_id] = c_id

        # Read country constraints
        country_max_export = {}
        country_min_dist = {}
        for _ in range(m):
            c_id, max_exp, min_dist = map(int, input().strip().split())
            if min_dist < 0 or max_exp < 0:
                print(-1)
                return
            country_max_export[c_id] = max_exp
            country_min_dist[c_id] = min_dist

        # Decision variables for children
        x = LpVariable.dicts("child", range(1, t+1), 0, 1, LpInteger)
        
        # Track running sums for constraints
        factory_used = {f_id: 0 for f_id in factory_stock}
        country_exports = {c_id: 0 for c_id in country_max_export}
        country_dist = {c_id: 0 for c_id in country_min_dist}
        children_per_country = {}

        # Objective function
        prob += lpSum(x[k] for k in range(1, t+1))

        # Process children requests
        for k in range(1, t+1):
            request = list(map(int, input().strip().split()))
            if len(request) < 3:
                print(-1)
                return
            
            child_id, country_id = request[0], request[1]
            toy_requests = request[2:]
            
            # Validate toy requests
            if not toy_requests or not all(f_id in factory_stock for f_id in toy_requests):
                print(-1)
                return

            # Count children per country
            children_per_country[country_id] = children_per_country.get(country_id, 0) + 1
            
            # Create and add child's assignment constraints
            child_assignments = []
            for f_id in toy_requests:
                var = LpVariable(f"assign_{k}_{f_id}", 0, 1, LpInteger)
                child_assignments.append(var)
                
                # Update usage trackers
                factory_used[f_id] += var
                if factory_country[f_id] != country_id:
                    country_exports[factory_country[f_id]] += var
                country_dist[country_id] += var

            # Add child constraints
            if child_assignments:
                prob += lpSum(child_assignments) <= 1
                prob += lpSum(child_assignments) == x[k]

        # Add factory constraints
        for f_id, usage in factory_used.items():
            prob += usage <= factory_stock[f_id]

        # Add country export constraints
        for c_id, exports in country_exports.items():
            prob += exports <= country_max_export[c_id]

        # Add minimum distribution constraints
        for c_id, dist in country_dist.items():
            num_children = children_per_country.get(c_id, 0)
            min_req = min(country_min_dist[c_id], num_children)
            prob += dist >= min_req

        # Solve and output result
        status = prob.solve(PULP_CBC_CMD(msg=False))
        print(sum(1 for k in range(1, t+1) if value(x[k]) > 0.5) if status == LpStatusOptimal else -1)
            
    except Exception:
        print(-1)

if __name__ == "__main__":
    solve_toy_distribution()