import z3

# Parse .sy file
parsed_sygus = z3.parse_smt2_file("sygusInput.sy")

# Define the functions
mov_avgerage = z3.Function('mov_avg', z3.ArraySort(z3.IntSort(), z3.RealSort()), z3.IntSort(), z3.RealSort())
compare_ma = z3.Function('compare_ma', z3.RealSort(), z3.RealSort(), z3.RealSort(), z3.IntSort())

# Simplify
mov_avgerage_simp = z3.simplify(z3.And(parsed_sygus[0]))
compare_ma_simp = z3.simplify(z3.And(parsed_sygus[1]))

#solver
solver = z3.SolverFor("QF_AUFLIRA")
solver.set("produce-models", True)
solver.add(mov_avgerage_simp)
solver.add(compare_ma_simp)

#model
assert solver.check() == z3.sat
model = solver.model()


# test input
prices = [100.0, 101.0, 120.0, 130.0, 104.0, 150.0, 106.0, 107.0, 180.0, 120.0, 100.0]
days = 5
threshold = 2.0
shortma = 4
longma = 6


# Z3 array to test 
prices_array = z3.Array('prices', z3.IntSort(), z3.RealSort())
for i in range(len(prices)):
    prices_array = z3.Store(prices_array, z3.IntVal(i), z3.RealVal(prices[i]))

# run - should return numeric?
mov_average_value = model.evaluate(mov_avgerage(prices_array, z3.IntVal(days)))
compare_ma_value = model.evaluate(compare_ma(z3.RealVal(shortma), z3.RealVal(longma), z3.RealVal(threshold)))
print("mov_avgerage:", mov_average_value)
print("compare_ma:", compare_ma_value)



